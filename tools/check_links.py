#!/usr/bin/env python3
"""Check relative Markdown links and heading fragments in the atlas."""
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = (
    '*.md', '.github/**/*.md', 'docs/**/*.md', 'reports/**/*.md',
    'tools/**/*.md', 'data/**/*.md',
)
FENCE = re.compile(r'^ {0,3}(`{3,}|~{3,})(.*)$')
INLINE_LINK = re.compile(r'\]\(\s*(?:<([^>]+)>|((?:[^()\s]|\([^()]*\))+))(?=\s|\))')
HEADING = re.compile(r'^ {0,3}#{1,6}\s+(.*?)\s*#*\s*$')
ANCHOR = re.compile(r'<a\s+[^>]*?\b(?:id|name)=["\']([^"\']+)["\']')


def read_markdown(file):
    links = []
    anchors = set()
    headings = Counter()
    fence = ''
    for lineno, line in enumerate(file.read_text(encoding='utf-8').splitlines(), 1):
        marker = FENCE.match(line)
        if fence:
            if marker and marker[1].startswith(fence) and not marker[2].strip():
                fence = ''
            continue
        if marker:
            fence = marker[1]
            continue
        text = re.sub(r'`[^`]*`', '', line)
        anchors.update(ANCHOR.findall(text))
        heading = HEADING.match(line)
        if heading:
            slug = re.sub(r'[^\w -]', '', heading[1].lower()).replace(' ', '-')
            count = headings[slug]
            anchors.add(f'{slug}-{count}' if count else slug)
            headings[slug] += 1
        links.extend((lineno, m[1] or m[2]) for m in INLINE_LINK.finditer(text))
    return links, anchors


def check(root):
    root = root.resolve()
    read = lru_cache(maxsize=None)(read_markdown)
    documents = sorted({file for pattern in DOCUMENTS for file in root.glob(pattern) if file.is_file()})
    errors = []
    for source in documents:
        links, _ = read(source)
        for line, link in links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            name = unquote(parsed.path)
            target = (source.parent / name).resolve() if name else source
            location = f'{source.relative_to(root)}:{line}'
            if not target.is_relative_to(root) or not target.exists():
                errors.append(f'{location}: 找不到路径 {link}')
                continue
            if target.is_dir():
                target = target / 'README.md'
            if parsed.fragment and target.suffix.lower() == '.md':
                if not target.is_file() or unquote(parsed.fragment) not in read(target)[1]:
                    errors.append(f'{location}: 找不到锚点 {link}')
    return len(documents), errors


def main():
    count, errors = check(ROOT)
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'文档链接检查通过（{count} 个 Markdown 文件）')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
