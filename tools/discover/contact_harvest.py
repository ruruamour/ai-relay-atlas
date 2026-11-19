#!/usr/bin/env python3
"""从联系人/邮件清单里提取候选域名。

输入是每行一个邮箱地址（例如某次群发邮件的收件人清单），只输出域名线索：
不保存邮箱地址、发件人、标题、正文或邮件头。免费邮箱域名不算站点；
可选地把免费邮箱地址里像域名的 local part（如 `vipapi.online@qq.com`）也当线索。

用法：
  python3 tools/discover/contact_harvest.py /tmp/recipients.txt \
      --out /tmp/contact-harvest.jsonl --domains /tmp/contact-domains.txt
"""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

# 公共邮箱服务商：这些域名的地址只能说明"有人"，不能说明有站。
FREEMAIL = {
    'qq.com', 'foxmail.com', '163.com', '126.com', 'yeah.net', 'sina.com', 'sina.cn',
    'gmail.com', 'googlemail.com', 'outlook.com', 'hotmail.com', 'live.com', 'msn.com',
    'yahoo.com', 'ymail.com', 'icloud.com', 'me.com', 'tuta.io', 'tuta.com', 'proton.me',
    'protonmail.com', 'gmx.com', 'mail.ru', 'yandex.com', 'zoho.com', 'aol.com',
    '88.com', '88.ltd', '139.com', 'wo.cn', '21cn.com', 'aliyun.com', 'sohu.com',
}

ROLE = {'abuse', 'admin', 'administrator', 'support', 'sales', 'service', 'services',
        'contact', 'hello', 'hi', 'info', 'help', 'team', 'office', 'feedback', 'billing',
        'partner', 'partners', 'marketing', 'postmaster', 'root', 'webmaster', 'api',
        'official', 'customer-services', 'customerservice', 'noreply', 'no-reply'}

EMAIL = re.compile(r'[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}')
# local part 里像域名的片段：label(.label)+.tld，且 tld 是常见后缀
LOCAL_DOMAIN = re.compile(r'^(?:[a-z0-9](?:[a-z0-9\-]*[a-z0-9])?\.)+'
                          r'(?:com|net|org|cn|io|ai|dev|app|cc|me|co|xyz|top|vip|shop|work|cloud|one|us|id|link|inc|tech|online|site|fun|pro|win|bond|help)$')


def clean_host(value):
    host = (value or '').strip().lower().strip('.')
    if host.startswith('www.'):
        host = host[4:]
    return host


def harvest(lines):
    rows = defaultdict(set)          # domain -> source labels
    kinds = defaultdict(set)         # domain -> role/personal
    for raw in lines:
        for email in EMAIL.findall(raw.lower()):
            local, _, host = email.partition('@')
            host = clean_host(host)
            if not host:
                continue
            bucket = 'role' if local in ROLE else 'personal'
            if host in FREEMAIL:
                # 免费邮箱只提供 owner 线索，不提供站点线索；可选 local part 提示。
                if LOCAL_DOMAIN.match(local):
                    rows[local].add('contact-localpart')
                    kinds[local].add(bucket)
                continue
            rows[host].add('contact-list')
            kinds[host].add(bucket)
    return rows, kinds


def main():
    ap = argparse.ArgumentParser(description='从联系人/邮件清单提取候选域名')
    ap.add_argument('input', nargs='+', help='邮箱清单文本（每行一个地址，可有其他文字）')
    ap.add_argument('--out', default='/tmp/contact-harvest.jsonl')
    ap.add_argument('--domains', default='/tmp/contact-domains.txt')
    args = ap.parse_args()

    lines = []
    for path in args.input:
        with open(path, encoding='utf-8', errors='replace') as fh:
            lines.extend(fh)

    rows, kinds = harvest(lines)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', encoding='utf-8') as fh:
        for domain in sorted(rows):
            fh.write(json.dumps({
                'domain': domain,
                'source_files': sorted(rows[domain]),
                'contact_kind': sorted(kinds[domain]),
            }, ensure_ascii=False) + '\n')
    Path(args.domains).write_text(''.join(d + '\n' for d in sorted(rows)), encoding='utf-8')
    print('候选域名 %d 个（其中 local-part 线索 %d 个）' % (
        len(rows), sum(1 for v in rows.values() if 'contact-localpart' in v)))


if __name__ == '__main__':
    main()
