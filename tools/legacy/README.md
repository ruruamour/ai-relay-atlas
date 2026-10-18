# legacy/ · 已停用

早期针对单个模型（Gemini / MiMo / Grok / Argon）的一次性扫描与提取脚本，以及首次建库用的 `normalize.py`。

保留仅供追溯 `data/raw/` 里各文件是怎么来的；**不在当前流程里**，部分脚本依赖作者本机路径。
`normalize.py` 会用 `data/raw/` 覆盖现有中转站表，已加 `--init` 保护。

现在的流程见 [../README.md](../README.md)。
