#!/usr/bin/env python3
"""共享工具：路径、CSV 读写、模型名归一、域名归一。"""
import csv
import os
import re
import sys

csv.field_size_limit(sys.maxsize)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def path(*p):
    return os.path.join(ROOT, *p)


RELAYS = path('data', 'relays', 'relays.csv')
MODELS = path('data', 'relays', 'relay-models.csv')
ALIASES = path('data', 'relays', 'aliases.csv')
SOURCES = path('data', 'raw', 'sources')

RELAY_COLS = ['domain', 'api_host', 'name', 'system', 'discovered_via', 'veridrop_score', 'n_models', 'families',
              'aliases', 'backend_group', 'http_status', 'latency_ms', 'last_checked', 'notes']
MODEL_COLS = ['domain', 'model', 'model_base', 'billing', 'input_usd_m', 'output_usd_m', 'call_usd',
              'group', 'group_ratio', 'model_ratio', 'source', 'flag', 'last_checked']
ALIAS_COLS = ['alias', 'canonical', 'reason', 'discovered_via']


def read_csv(p):
    if not os.path.exists(p):
        return []
    with open(p, newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def write_csv(p, cols, rows):
    tmp = p + '.tmp'
    with open(tmp, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction='ignore', lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow(r)
    os.replace(tmp, p)


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def fmt(v):
    """数字转紧凑字符串（不用科学计数法），None -> ''。"""
    if v is None or v == '':
        return ''
    try:
        x = float(v)
    except (TypeError, ValueError):
        return str(v)
    if x == 0:
        return '0'
    s = ('%.6g' % x) if 1e-4 <= abs(x) < 1e15 else ('%.10f' % x)
    return s.rstrip('0').rstrip('.') if '.' in s and 'e' not in s else s


# ---------------- 模型名 ----------------
_FAMILY_KW = re.compile(r'(chatgpt|gpt|claude|gemini|gemma|grok|mimo|deepseek|qwen|qwq|glm|kimi|moonshot|'
                        r'doubao|minimax|abab|llama|mistral|ernie|hunyuan)')
_BRACKETS = re.compile(r'[\[\(（【][^\]\)）】]*[\]\)）】]')
_DROP = {'high', 'low', 'medium', 'xhigh', 'minimal', 'none', 'auto', 'thinking', 'nothinking',
         'maxthinking', 'think', 'nothink', 'reasoning', 'free', 'official', 'latest', 'all', 'feed',
         'bl', 'cc', 'cli', 'gcp', 'vertex', 'aistudio', 'anti', 'antigravity', 'search', 'count', 'token'}
_DATE = [re.compile(r'-\d{8}$'), re.compile(r'-2[0-9](0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])$'), re.compile(r'-\d{4}-\d{2}-\d{2}$'), re.compile(r'-\d{2}-\d{2}$'),
         re.compile(r'-\d{4}$'), re.compile(r'-(thinking|think)-\d+k?$'), re.compile(r'-\d+(\.\d+)?k$')]


def model_base(name):
    """把渠道标签、思考档位、日期等去掉，得到用于分组的基础模型名。原名仍保留在 model 列。"""
    s = (name or '').strip().lower()
    s = _BRACKETS.sub('', s)
    s = s.split('/')[-1]
    s = re.sub(r'[\s_]+', '-', s)
    m = _FAMILY_KW.search(s)
    if m and m.start() > 0:
        s = s[m.start():]
    while True:
        old = s
        for rx in _DATE:
            s = rx.sub('', s)
        parts = s.rsplit('-', 1)
        if len(parts) == 2 and parts[1] in _DROP and parts[0]:
            s = parts[0]
        if s == old:
            break
    if s.startswith('claude'):
        s = re.sub(r'(\d)\.(\d)', r'\1-\2', s)
    s = re.sub(r'-{2,}', '-', s).strip('-.')
    return s or (name or '').strip().lower()


FAMILIES = [  # (code, 显示名, 正则) —— 顺序即判定优先级
    ('openai', 'OpenAI', re.compile(r'^(gpt|chatgpt|o\d|dall-e|sora|tts-|whisper|text-embedding|codex|omni-moderation|computer-use|davinci|babbage)')),
    ('claude', 'Claude', re.compile(r'^claude')),
    ('gemini', 'Gemini', re.compile(r'^(gemini|nano-banana|imagen|veo)')),
    ('grok', 'Grok', re.compile(r'^grok')),
    ('mimo', 'MiMo', re.compile(r'^mimo')),
    ('deepseek', 'DeepSeek', re.compile(r'^deepseek')),
    ('qwen', 'Qwen', re.compile(r'^(qwen|qwq|qvq|wan\d|wanx)')),
    ('glm', 'GLM', re.compile(r'^(glm|chatglm|cogview|cogvideo)')),
    ('kimi', 'Kimi', re.compile(r'^(kimi|moonshot)')),
    ('doubao', '豆包', re.compile(r'^(doubao|seed)')),
    ('minimax', 'MiniMax', re.compile(r'^(minimax|abab|hailuo|speech-\d)')),
    ('hunyuan', '混元', re.compile(r'^(hunyuan|hy\d)')),
    ('llama', 'Llama', re.compile(r'^(llama|meta-llama|codellama)')),
    ('media', '图像/视频/音频', re.compile(r'^(flux|midjourney|mj[-_]|suno|kling|vidu|pixverse|happyhorse|runway|luma|'
                                     r'stable-diffusion|sd3|sdxl|recraft|ideogram|z-image|seedance|jimeng|udio|elevenlabs)')),
]
FAMILY_NAME = {c: n for c, n, _ in FAMILIES}
FAMILY_NAME['other'] = '其他'
FAMILY_ORDER = [c for c, _, _ in FAMILIES] + ['other']


def family(base):
    for code, _, rx in FAMILIES:
        if rx.match(base or ''):
            return code
    return 'other'


# 疑似密钥：个别站把 API Key 误填进模型名/分组名，入库前丢弃
SECRET_RX = re.compile(r'sk-[A-Za-z0-9]{32,}|sk-ant-[A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{35}|gh[pousr]_[A-Za-z0-9]{30,}|'
                       r'github_pat_[A-Za-z0-9_]{30,}|xai-[A-Za-z0-9]{30,}|AKIA[A-Z0-9]{16}|'
                       r'eyJ[A-Za-z0-9_-]{20,}\.eyJ[A-Za-z0-9_-]{20,}', re.I)


def has_secret(*vals):
    return any(SECRET_RX.search(v or '') for v in vals)


PROMO_RX = re.compile(r'福利|特价|特惠|免费|free|公益|限时|体验|白嫖|award|活动|赠送|测试|test|试用', re.I)


# ---------------- 域名 ----------------
IP_RE = re.compile(r'^\d{1,3}(\.\d{1,3}){3}(:\d+)?$')
GEN_PREFIX = {'api', 'new', 'sub', 'vip', 'ai', 'www', 'cn', 'hk', 'gw', '2api', 'api2', 'api3', 'us', 'sg',
              'hk2', 'jp', 'tw', 'v2', 'v3', 'relay', 'llm', 'proxy', 'gw2', 'openai', 'claude', 'gemini',
              'grok', 'gpt', 'ai2', 'mirror'}
_EXT = None


def _ext():
    global _EXT
    if _EXT is None:
        import tldextract
        _EXT = tldextract.TLDExtract(suffix_list_urls=(), cache_dir=None)  # 离线，用内置后缀表
    return _EXT


def registered(d):
    """可注册域（eTLD+1）。IP 原样返回。"""
    if IP_RE.match(d):
        return d
    h = d.split(':')[0]
    r = _ext()(h)
    rd = getattr(r, 'top_domain_under_public_suffix', None) or r.registered_domain
    return rd or h


def base_host(d):
    """去掉 api./www./cn. 等通用前缀后的主机名，用于判断是否同一站。"""
    if IP_RE.match(d):
        return d
    h = d.split(':')[0]
    n_rd = len(registered(d).split('.'))
    labels = h.split('.')
    while len(labels) > n_rd and labels[0] in GEN_PREFIX:
        labels = labels[1:]
    return '.'.join(labels)


def brand(d):
    """品牌名：可注册域的第一段（openlux.ai / openlux.top -> openlux）。"""
    if IP_RE.match(d):
        return d
    return registered(d).split('.')[0]
