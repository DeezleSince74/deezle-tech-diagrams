"""Convert the infra-diagrams icon sets into Whiteboard-ready data URIs.

Build tooling only: this file is never shipped in the plugin. It writes
plugin/skills/whiteboard-diagram/icons/<set>.json, one icon per line, so a
skill can find an icon with a plain text search (grep for "aws:amazon-rds").

Whiteboard images accept only g, path, rect, circle, ellipse, line, polyline
and polygon, with single-quoted attributes, '#' written as %23, and no style
attribute. Icons that can't be made to fit are left out and listed in the
report, and the skill falls back to a plain shape for them.

Usage: python3 -I tools/build_icons.py <path to Mermaid-Figma-Infra-Plugin/icons>
"""
import json
import os
import re
import sys

SRC = sys.argv[1]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "plugin", "skills", "whiteboard-diagram", "icons")
SETS = ["generic", "open", "data"]  # vendor sets are imported by each user, never shipped
ALLOWED = {"g", "path", "rect", "circle", "ellipse", "line", "polyline", "polygon"}
MAX_URI = 100_000
CHUNK = 240_000


def _hex(c):
    c = c.strip().lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) if re.fullmatch(r"[0-9a-fA-F]{6}", c) else None


def flatten_gradients(body):
    """Swap each gradient for the average of its stop colors, and drop clip paths.

    The board has no gradients or clipping, so this is the closest flat look.
    """
    colors = {}
    for m in re.finditer(r'<(linearGradient|radialGradient)\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</\1>', body, flags=re.S):
        stops = [_hex(s) for s in re.findall(r'stop-color="([^"]+)"', m.group(3))]
        stops = [s for s in stops if s]
        if stops:
            avg = tuple(round(sum(s[i] for s in stops) / len(stops)) for i in range(3))
            colors[m.group(2)] = "#%02x%02x%02x" % avg
    # A gradient can borrow its stops from another one with href="#id" and no stops of its own.
    for m in re.finditer(r'<(?:linearGradient|radialGradient)\b([^>]*)>', body):
        gid = re.search(r'\bid="([^"]+)"', m.group(1))
        ref = re.search(r'\b(?:xlink:)?href="#([^"]+)"', m.group(1))
        if gid and ref and gid.group(1) not in colors and ref.group(1) in colors:
            colors[gid.group(1)] = colors[ref.group(1)]
    if not colors and "<clipPath" not in body:
        return body
    body = re.sub(r"<defs>.*?</defs>", "", body, flags=re.S)
    body = re.sub(r"<(linearGradient|radialGradient)\b.*?</\1>", "", body, flags=re.S)
    body = re.sub(r"<clipPath\b.*?</clipPath>", "", body, flags=re.S)
    body = re.sub(r'\sclip-path="[^"]*"', "", body)
    body = re.sub(r'url\(#([^)]+)\)', lambda m: colors.get(m.group(1), "url(#%s)" % m.group(1)), body)
    return body


def convert(body, w, h):
    """Return (data URI, None) or (None, reason it can't be used)."""
    body = flatten_gradients(body)
    body = re.sub(r"<title>.*?</title>", "", body, flags=re.S)
    body = re.sub(r"<desc>.*?</desc>", "", body, flags=re.S)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    tags = set(re.findall(r"</?([A-Za-z][\w:-]*)", body))
    bad = tags - ALLOWED
    if bad:
        return None, "uses " + ", ".join(sorted(bad))
    if re.search(r"\sstyle=", body):
        return None, "uses a style attribute"
    if re.search(r"url\(", body):
        return None, "uses url() references"
    body = re.sub(r'\s(id|class|data-[\w-]+)="[^"]*"', "", body)
    depth = max_depth = 0
    for m in re.finditer(r"<(/?)g\b[^>]*?(/?)>", body):
        if m.group(1):
            depth -= 1
        elif not m.group(2):
            depth += 1
            max_depth = max(max_depth, depth)
    if max_depth >= 5:
        return None, f"nests {max_depth} groups"
    if len(re.findall(r"opacity=", body)) > 64:
        return None, "too many opacity attributes"
    body = re.sub(r"\s+", " ", body).strip()
    body = re.sub(r"></(path|rect|circle|ellipse|line|polyline|polygon)>", "/>", body)
    if "'" in body:
        return None, "contains a single quote"
    body = body.replace('"', "'")
    look = "" if body.count("currentColor") else " data-look='clean'"
    svg = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}'{look}>{body}</svg>"
    svg = svg.replace("%", "%25").replace("#", "%23")
    uri = "data:image/svg+xml," + svg
    if len(uri) > MAX_URI:
        return None, "over 100 KB"
    return uri, None


def main():
    os.makedirs(OUT, exist_ok=True)
    for old in os.listdir(OUT):
        if old.endswith(".json"):
            os.remove(os.path.join(OUT, old))
    report = ["# Icon conversion report", ""]
    total_ok = 0
    for name in SETS:
        data = json.load(open(os.path.join(SRC, f"{name}.json")))
        lines, skipped = [], []
        for key in sorted(data["icons"]):
            ic = data["icons"][key]
            w = ic.get("width", data.get("width", 24))
            h = ic.get("height", data.get("height", 24))
            uri, why = convert(ic["body"], w, h)
            if uri:
                lines.append(json.dumps({"ref": f"{name}:{key}", "w": w, "h": h, "src": uri},
                                        separators=(",", ":")))
            else:
                skipped.append((key, why))
        # Keep every file under the directory's 256 KiB inspection limit.
        chunks, cur, size = [], [], 0
        for line in lines:
            if cur and size + len(line) > CHUNK:
                chunks.append(cur)
                cur, size = [], 0
            cur.append(line)
            size += len(line) + 2
        chunks.append(cur)
        for i, chunk in enumerate(chunks, 1):
            fname = f"{name}.json" if len(chunks) == 1 else f"{name}-{i}.json"
            with open(os.path.join(OUT, fname), "w") as f:
                f.write("[\n" + ",\n".join(chunk) + "\n]\n")
        total_ok += len(lines)
        report.append(f"## {name}: {len(lines)} converted, {len(skipped)} left out")
        for key, why in skipped:
            report.append(f"- `{name}:{key}`: {why}")
        report.append("")
    with open(os.path.join(SRC, "aliases.json")) as f:
        aliases = json.load(f)
    with open(os.path.join(OUT, "aliases.json"), "w") as f:
        json.dump(aliases, f, indent=0, sort_keys=True)
    with open(os.path.join(ROOT, "tools", "icon-report.md"), "w") as f:
        f.write("\n".join(report))
    print(f"{total_ok} icons converted")
    print("\n".join(l for l in report if l.startswith("## ")))


if __name__ == "__main__":
    main()
