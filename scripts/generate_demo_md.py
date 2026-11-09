#!/usr/bin/env python3
"""Run 3 example Q&As per fictional customer and write DEMO.md."""

from __future__ import annotations

import json
import os
import sys
from importlib import reload
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DB = ROOT / "data" / "demo_transcript.db"
if DB.exists():
    DB.unlink()
os.environ["DATABASE_URL"] = f"sqlite:///{DB}"
os.environ.pop("OPENAI_API_KEY", None)
os.environ.pop("LLM_API_KEY", None)

import app.config as config

reload(config)
import app.db as dbmod

reload(dbmod)

from app.chat import handle_chat
from app.config import USE_LLM
from app.db import Base, SessionLocal, engine
from app.seed import seed

QUESTIONS = [
    "Which posts drove the most engagement last month?",
    "What are the total engagement totals last month?",
    "Show platform breakdown for the last 30 days",
]

CUSTOMERS = [
    ("cust_aurora", "Aurora Trail Co. (FICTIONAL)"),
    ("cust_nimbus", "Nimbus Bean Roasters (FICTIONAL)"),
    ("cust_pixelpine", "Pixel Pine Studio (FICTIONAL)"),
]


def main() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    seed()

    lines: list[str] = []
    lines.append("# Demo transcript (screenshot-free)")
    lines.append("")
    lines.append(
        "Generated locally against **fictional** seeded data. "
        f"Answer mode: **{'LLM' if USE_LLM else 'deterministic fallback'}**."
    )
    lines.append("")
    lines.append("This is an illustration of the chatbot, not a client deliverable.")
    lines.append("")

    with SessionLocal() as session:
        for cid, name in CUSTOMERS:
            lines.append(f"## {name} (`{cid}`)")
            lines.append("")
            for i, q in enumerate(QUESTIONS, start=1):
                out = handle_chat(
                    session,
                    customer_id=cid,
                    session_id=f"demo-{cid}",
                    message=q,
                )
                lines.append(f"### Q{i}. {q}")
                lines.append("")
                lines.append(f"**Query kind:** `{out['query_kind']}` · **Mode:** `{out['mode']}`")
                lines.append("")
                lines.append("**Answer:**")
                lines.append("")
                lines.append("```")
                lines.append(out["answer"])
                lines.append("```")
                lines.append("")
                if out["rows"]:
                    lines.append("<details><summary>Structured rows (truncated)</summary>")
                    lines.append("")
                    lines.append("```json")
                    lines.append(json.dumps(out["rows"][:3], indent=2))
                    lines.append("```")
                    lines.append("")
                    lines.append("</details>")
                    lines.append("")

    out_path = ROOT / "DEMO.md"
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
