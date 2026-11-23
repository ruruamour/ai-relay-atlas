#!/usr/bin/env python3
"""Parse the independently published daily relay directory data files.

The parser only reads decoded text supplied by its caller.  It never fetches
the listed sites or follows registration links.  The navigation CSV is kept
out of ``LIST_SOURCES`` because its only URL field is an affiliate-oriented
registration link rather than an official-site field.
"""

import ipaddress
import json
import re
from urllib.parse import urlsplit


ZHONGZHUAN_SOURCE = "1sh1ro/ai-api-zhongzhuan"
ZHONGZHUAN_RAW_URL = (
    "https://raw.githubusercontent.com/1sh1ro/ai-api-zhongzhuan/main/data/sites.json"
)

GONGYI_SOURCE = "bubblevv/ai-api-gongyi-nav"
GONGYI_RAW_URL = (
    "https://raw.githubusercontent.com/bubblevv/ai-api-gongyi-nav/main/ai-api-sites-table.csv"
)

# This source has a registration-link column, not an official-site column.
# Its current rows use affiliate or invitation paths, and one row is a
# community bot.  Keeping the reason next to the source makes the omission
# visible to the caller without retaining any of those outbound links.
OMITTED_SOURCES = {
    GONGYI_SOURCE: (
        GONGYI_RAW_URL,
        "omitted because the feed exposes only registration links, mostly "
        "affiliate or invitation links, and no unambiguous official-site field",
    ),
}

_RELAY_TAGS = frozenset({"api-relay", "api-gateway"})
_EXCLUDED_TAGS = frozenset(
    {
        "affiliate",
        "community",
        "community-link",
        "directory",
        "docs",
        "documentation",
        "marketing",
        "official",
        "official-upstream",
        "promo",
        "promotion",
        "provider",
        "redirect",
        "search",
        "upstream",
        "vendor",
    }
)
_HOST_LABEL = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")
_RESERVED_HOSTS = frozenset(
    {
        "example.com",
        "example.net",
        "example.org",
        "localhost",
    }
)
_RESERVED_SUFFIXES = (".example", ".invalid", ".localhost", ".test")


def _hostname_from_official_url(value):
    """Return a clean HTTPS hostname from one direct site URL."""
    if not isinstance(value, str):
        return None

    value = value.strip()
    if not value or any(character.isspace() for character in value):
        return None

    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError:
        return None

    if parsed.scheme.lower() != "https" or not parsed.netloc:
        return None
    if parsed.username is not None or parsed.password is not None:
        return None
    if port not in (None, 443) or parsed.query or parsed.fragment or parsed.path not in ('', '/', '/zh', '/zh/'):
        return None

    host = parsed.hostname
    if not host:
        return None
    try:
        host = host.encode("idna").decode("ascii").lower().rstrip(".")
        ipaddress.ip_address(host)
    except (UnicodeError, ValueError):
        pass
    else:
        return None

    if (
        host in _RESERVED_HOSTS
        or host.endswith(_RESERVED_SUFFIXES)
        or len(host) > 253
        or "." not in host
    ):
        return None

    labels = host.split(".")
    if any(not _HOST_LABEL.fullmatch(label) for label in labels):
        return None
    return host


def _tags(value):
    if not isinstance(value, list):
        return None
    return {
        tag.strip().casefold()
        for tag in value
        if isinstance(tag, str) and tag.strip()
    }


def parse_zhongzhuan_sites(text):
    """Return relay host/evidence pairs from ``data/sites.json``.

    Only the row's ``homepage`` field is considered a site URL.  A row must
    carry an explicit relay or gateway tag and must not carry an
    exclusion tag.  Malformed JSON and schema drift produce an empty result.
    """
    if not isinstance(text, str):
        return []
    try:
        document = json.loads(text)
    except (TypeError, ValueError):
        return []
    if not isinstance(document, dict) or not isinstance(document.get("sites"), list):
        return []

    pairs = []
    for row in document["sites"]:
        if not isinstance(row, dict):
            continue
        tags = _tags(row.get("tags"))
        if not tags or not tags.intersection(_RELAY_TAGS) or tags.intersection(_EXCLUDED_TAGS):
            continue
        host = _hostname_from_official_url(row.get("homepage"))
        if host:
            pairs.append((host, ZHONGZHUAN_RAW_URL))
    return pairs


LIST_SOURCES = {
    ZHONGZHUAN_SOURCE: (ZHONGZHUAN_RAW_URL, parse_zhongzhuan_sites),
}
