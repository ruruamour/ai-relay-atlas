# 用 FOFA / ZoomEye / Shodan 找自建卡网

聚合站（OpenPrice、水獭、AI号探）只能看到**主动入驻**的店，上限就在 400 多家。要再往上，只能绕过聚合站，直接在全网找"自己搭发卡系统"的站——这就是 FOFA 这类网络空间测绘引擎的用途。

## 一、为什么有效

这类引擎常年爬全网 HTTP 响应，把**页面正文、标题、HTTP 头、证书、图标哈希**都建了索引。所以你可以直接搜"谁的页面里有 `dujiaoka`"，而不依赖任何目录站收录。

对本项目最关键的三个事实：

| 事实 | 含义 |
|---|---|
| 独角数卡 / 异次元发卡 的源码里有固定字符串（`dujiaoka`、`acg-faka`、`/assets/dujiaoka`） | 可以按源码指纹精确搜，命中即基本确定系统 |
| 卡网页一定有"自动发货""卡密""寄售"这类词 | 系统改过也能用通用词捞 |
| 卖 AI 的卡网一定出现 ChatGPT/Claude/Gemini/Grok | 两个条件叠加，噪声大幅下降 |

## 二、平台对比

| 平台 | 中国站点覆盖 | 免费额度 | 付费 | 语法风格 |
|---|---|---|---|---|
| **FOFA**（fofa.info） | 最好，国内站最全 | 注册送少量条数，免费账号每日有限额 | 会员按年，API 按条计费 | `body="x" && country="CN"` |
| **ZoomEye**（zoomeye.org） | 好 | 有免费额度 | 按年 | `app:"x" && body:"y"` |
| **Shodan** | 一般（国内站偏少） | 免费只能看前几页 | 一次性会员 | `http.html:"x" http.title:"y"` |
| **Quake**（360） | 好 | 有免费额度 | 按年 | `body:"x"` |
| **Hunter**（奇安信） | 好 | 有免费额度 | 按年 | `body="x"` |
| **Censys** | 一般 | 有限 | 按量 | `services.http.response.body: "x"` |

**优先顺序：FOFA → Quake → ZoomEye → Shodan**。国内卡网绝大多数托管在国内或香港，FOFA/Quake 的覆盖率明显更高。

## 三、查询串

脚本里已经准备好，直接生成：

```bash
python3 tools/discover/faka_fofa.py queries --platform fofa
python3 tools/discover/faka_fofa.py queries --platform shodan
python3 tools/discover/faka_fofa.py queries --platform zoomeye
```

### 按系统指纹（最准）

```
body="dujiaoka"                 独角数卡
body="/assets/dujiaoka"         独角数卡（资源路径，改过标题也能中）
body="acg-faka"                 异次元发卡
body="异次元发卡"                异次元发卡（中文名）
body="zfaka"                    ZFAKA
body="萌次元"                    萌次元
body="aceyun"                   ACE 云寄售
body="catfk"                    云猫寄售
```

### 系统指纹 + AI 关键词（推荐主用）

```
(body="dujiaoka" || body="acg-faka") && (body="ChatGPT" || body="Claude" || body="Gemini")
```

### 系统未知时，用通用词兜底

```
(body="自动发货" || body="卡密") && (body="ChatGPT" || body="Claude" || body="Gemini" || body="Grok")
(body="寄售" || body="虚拟商品") && (body="ChatGPT" || body="Claude")
title="发卡" || title="卡网" || title="发卡网"
```

### 无标题的单页商城（我们识别出的"购物模板"同源站）

```
title="购物 -" && (body="ChatGPT" || body="Claude" || body="Gemini")
```

### 收窄到中国大陆

FOFA 加 `&& country="CN"`；但要留意很多站挂 CDN 或在香港，加国家会漏，建议先不加，结果里按 IP 归属再筛。

## 四、实操流程

```bash
# 1. 网页版或 API 搜索，导出结果（FOFA 支持导出 JSON/CSV）
# 2. 解析导出文件，自动去掉 IP、源码仓库、聚合站自己、已收录的站
python3 tools/discover/faka_fofa.py parse ~/Downloads/fofa.json
#    → data/raw/sources/fofa-candidates.txt

# 3. 看这些站卖不卖我们要的模型（New-API/Sub2API 的会直接出价）
python3 tools/scan.py data/raw/sources/fofa-candidates.txt /tmp/fofa.json

# 4. 纯卡网（不发 API）的，做一次指纹确认 + 人工看品类
# 5. 确认后补进 data/shops/（走 normalize_shops 或直接改原始数据再重建）

# GitHub / CT 候选也可先做首页指纹筛选（不保存正文）
cat /tmp/github-harvest-10k-live.txt /tmp/crt-signal-live.txt | sort -u > /tmp/shop-candidates.txt
python3 tools/discover/shop_fingerprint.py /tmp/shop-candidates.txt \
  --out data/raw/sources/shop-fingerprint-candidates.jsonl --workers 16
# 只把 high/medium 且人工确认在售的站点补入 data/shops；不要把候选自动当成商品店
```

有 API Key 时可以一条命令跑：

```bash
export FOFA_API_KEY=你的key
python3 tools/discover/faka_fofa.py api
```

> 脚本不内置任何 Key。免费额度按条计费，**先用网页版试查询串**，确认命中率再花额度。

## 五、成本粗算

| 做法 | 成本 | 预计新增 |
|---|---|---|
| 网页版手动翻前几页，只抄域名 | 0 | 几十家 |
| FOFA 会员 + 手动导出（1000 条/次） | 会员年费 | 数百家（含大量非 AI 站，需筛） |
| API 批量跑多组查询串 | 按条计费，几千条量级 | 同上，但可自动化 |

真正决定收益的不是条数，而是**筛选**：1000 条里可能只有 10%–20% 是卖 AI 的。所以先用 `body + AI 关键词` 叠加，把命中率做上去再拉量。

## 六、合规边界

这条线是**只读公开页面**，和项目其他部分一致，但有几条要守住：

- 只查测绘引擎已收录的公开 banner，**不主动扫描**目标站，不爆破、不绕登录、不试探漏洞。
- 遵守各平台 ToS 与配额，别用多账号刷免费额度。
- 不把结果里的 IP、端口、证书等基础设施信息写进仓库；仓库里只留域名和公开价格。
- 发现站点含明显违法内容（如批量卖被盗账号），不收录、不引用。

## 七、已知的坑

| 坑 | 说明 |
|---|---|
| **favicon 指纹不可靠** | 实测 82 个自建站，独角数卡 26 个站里最常见的 hash 也只出现 2 次——店主基本都会换图标。别指望 `icon_hash` |
| **只索引首页** | 商品在二级页的，正文里可能没有 `ChatGPT` 字样，会漏 |
| **CDN 挡在前面** | 返回的是 CDN IP，看不到真实主机；`host` 字段仍能拿到域名，够用 |
| **伪静态 / 改版** | 系统被改过的，源码指纹失效，只能靠通用词 |
| **误报** | 发卡系统官方演示站、源码仓库、教程文章都会命中，`parse` 已过滤常见的一批 |
| **同一站多域名** | 结果里会有 `a.com` / `www.a.com` / `api.a.com`，交给 `dedupe.py` 合并 |

## 八、目前进度

- 已用聚合站：430 家店（自建 83 家）
- Veridrop / GitHub / GitLab / CT / urlscan / npm / Docker Hub / Hugging Face / Bing / 公开目录首页指纹已筛出 190 个中高置信候选；其中 3 个已浏览器确认首页商品标记，仍未自动并入商品店表
- FOFA 这条路**尚未执行**（当前浏览器未登录），查询串与解析脚本已就绪
- 预期：完成人工确认后再把自建站和纯卡网分别入库，避免把 API 网关误算成商品店
