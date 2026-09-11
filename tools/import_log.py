#!/usr/bin/env python3
"""
从学习日志导入期目元数据 → data/episodes.json

用法:
    python3 tools/import_log.py <study_daily_log.md> <study_progress.json>

作用:
    - 解析日志中的每一期（日期 / Day 号 / 主题）
    - 自动跳过「自动化再次触发」「结课回顾」等无内容条目
    - 与已有的 episodes.json 合并：已有正文的期保留不动，只补元数据

这是「造物主工具包」的一部分：换一个日志文件，就能复用到其他课程。
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "episodes.json"
SKIP_MARKERS = ["再次触发", "结课回顾", "自动化再次触发"]


def clean_topic(s: str) -> str:
    """去掉括号里的教材出处。"""
    s = re.sub(r"[（(](?:教材|中文笔记|英文|来源)[^）)]*[）)]", "", s)
    s = re.sub(r"[（(][^）)]*(?:教材|页|pp?\.)[^）)]*[）)]", "", s)
    return s.strip()


def split_title(topic: str):
    """把「主标题 — 副标题」拆开，优先取引号内的句子当标题。"""
    topic = clean_topic(topic).rstrip("；;")
    m = re.search(r'[“"]([^”"]+)[”"]', topic)
    if m:
        title = m.group(1).strip()
        head = topic[: m.start()].strip(" —-—")
        return title, head or topic
    parts = re.split(r"\s*[—–]{1,2}\s*|\s+-\s+", topic, maxsplit=1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return topic, ""


def parse_log(path: Path):
    txt = path.read_text(encoding="utf-8")
    blocks = re.split(r"^## ", txt, flags=re.M)[1:]
    rows, seen = [], set()
    for b in blocks:
        head = b.split("\n")[0].strip()
        if any(s in head for s in SKIP_MARKERS):
            continue
        m_date = re.search(r"(\d{4}-\d{2}-\d{2})", head)
        m_day = re.search(r"Day\s*(\d+)", head)
        m_topic = re.search(r"[-*]\s*主题[：:]\s*(.+)", b)
        if not (m_date and m_topic):
            continue
        date = m_date.group(1)
        day = int(m_day.group(1)) if m_day else None
        key = day if day else date
        if key in seen:
            continue
        seen.add(key)
        rows.append({"date": date, "day": day, "topic": m_topic.group(1).strip()})
    rows.sort(key=lambda r: r["date"])
    return rows


def unit_map(progress_path: Path):
    data = json.loads(progress_path.read_text(encoding="utf-8"))
    return {l["day"]: l["unit"] for l in data.get("lessons", [])}


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    rows = parse_log(Path(sys.argv[1]))
    units = unit_map(Path(sys.argv[2]))

    existing = {}
    if OUT.exists():
        for e in json.loads(OUT.read_text(encoding="utf-8"))["episodes"]:
            existing[e["id"]] = e

    course_no, extra_no = 0, 0
    episodes = []
    for r in rows:
        if r["day"]:
            course_no = r["day"]
            eid = f"day-{r['day']}"
            series, no, unit = "course", r["day"], units.get(r["day"], "")
            label = f"Day {r['day']}"
        else:
            extra_no += 1
            eid = f"vol-{extra_no}"
            series, no, unit = "extra", extra_no, "番外"
            label = f"Vol.{extra_no}"

        title, topic = split_title(r["topic"])

        if eid in existing and existing[eid].get("status") == "done":
            episodes.append(existing[eid])          # 已有正文，原样保留
            continue

        episodes.append({
            "id": eid, "series": series, "no": no, "date": r["date"],
            "unit": unit, "label": label,
            "title": title, "topic": topic,
            "tags": [], "status": "draft",
            "hook": "", "story": [], "insight": [], "math": [],
            "trivia": [], "quote": None, "source": None, "think": "",
            "readTime": "",
        })

    data = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    data.setdefault("meta", {})
    data["episodes"] = episodes
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    done = sum(1 for e in episodes if e.get("status") == "done")
    print(f"✓ 导入 {len(episodes)} 期（已完稿 {done} 期，待整理 {len(episodes)-done} 期）")


if __name__ == "__main__":
    main()
