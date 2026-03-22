#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from app.main import app


def main() -> None:
    output = app.openapi()
    out_path = Path("protocol/openapi.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
