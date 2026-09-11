#!/usr/bin/env python3
"""
人话线性代数 — 静态站点生成器

用法:
    python3 build.py

输入:  data/episodes.json   (唯一数据源)
输出:  docs/                (GitHub Pages 根目录)
"""

import hashlib
import json
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "episodes.json"
TPL = ROOT / "templates"
OUT = ROOT / "docs"


def cell_color(ep: dict) -> str:
    """由 id 确定性生成格子颜色；课程期=靛蓝系，番外=紫系。
    待整理的期用淡色，完稿的用饱和色——矩阵墙本身就是一张进度图。"""
    seed = int(hashlib.md5(ep["id"].encode()).hexdigest()[:8], 16)
    if ep["series"] == "course":
        hue = 218 + (seed % 26) - 13
        sat = 46 + (seed // 26) % 28
    else:
        hue = 262 + (seed % 30) - 15
        sat = 40 + (seed // 26) % 28
    if ep.get("status") == "draft":
        return f"hsl({hue} 34% 90%)"
    light = 50 + (seed // 52) % 24
    return f"hsl({hue} {sat}% {light}%)"


def load():
    raw = json.loads(DATA.read_text(encoding="utf-8"))
    meta = raw["meta"]

    eps = []
    for e in raw["episodes"]:
        e = dict(e)
        e.setdefault("tags", [])
        e.setdefault("insight", [])
        e.setdefault("math", [])
        e.setdefault("trivia", [])
        e.setdefault("think", "")
        e.setdefault("readTime", "3 min")
        if e["series"] == "course":
            e["label"] = f"Day {e['no']}"
            e["sort"] = (0, e["no"])
        else:
            e["label"] = f"Vol.{e['no']}"
            e["sort"] = (1, e["no"])
        e["color"] = cell_color(e)
        eps.append(e)

    eps.sort(key=lambda x: x["sort"])
    return meta, eps


def build():
    meta, eps = load()

    env = Environment(
        loader=FileSystemLoader(str(TPL)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "ep").mkdir(parents=True)
    shutil.copytree(ROOT / "assets", OUT / "assets")

    course_eps = [e for e in eps if e["series"] == "course"]
    extra_eps = [e for e in eps if e["series"] == "extra"]
    done_n = sum(1 for e in eps if e.get("status") == "done")

    # 首页
    html = env.get_template("index.html").render(
        meta=meta, root="",
        episodes=eps, course_eps=course_eps, extra_eps=extra_eps,
        total=len(eps), course_n=len(course_eps), extra_n=len(extra_eps),
        done_n=done_n,
    )
    (OUT / "index.html").write_text(html, encoding="utf-8")

    # 单期内页
    tpl_ep = env.get_template("episode.html")
    for i, e in enumerate(eps):
        html = tpl_ep.render(
            meta=meta, root="../", ep=e,
            prev=eps[i - 1] if i > 0 else None,
            next=eps[i + 1] if i < len(eps) - 1 else None,
        )
        (OUT / "ep" / f"{e['id']}.html").write_text(html, encoding="utf-8")

    # .nojekyll 让 GitHub Pages 原样发布（不跑 Jekyll）
    (OUT / ".nojekyll").write_text("", encoding="utf-8")

    print(f"✓ 生成 {len(eps)} 期 + 首页 → {OUT}")
    print(f"  课程日 {len(course_eps)} 期 / 番外 {len(extra_eps)} 期 · 已完稿 {done_n} 期")


if __name__ == "__main__":
    build()
