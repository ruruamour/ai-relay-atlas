#!/usr/bin/env bash
# 提交前检查：仓库里不能出现疑似密钥（API Key / Token）。build.sh 末尾会自动运行。
set -uo pipefail
cd "$(dirname "$0")/.."
RX='sk-[A-Za-z0-9]{32,}|sk-ant-[A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{35}|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|xai-[A-Za-z0-9]{30,}|AKIA[A-Z0-9]{16}|eyJ[A-Za-z0-9_-]{20,}\.eyJ[A-Za-z0-9_-]{20,}'
hits=$(grep -rnoIE "$RX" --exclude-dir=.git --exclude=check_secrets.sh --exclude=common.py . | sed -E 's/(:[^:]{8})[^:]*$/\1…/')
if [ -n "$hits" ]; then
  echo "✗ 发现疑似密钥，禁止提交："; echo "$hits"; exit 1
fi
echo "✓ 未发现疑似密钥"
