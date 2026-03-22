#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from sdk_python_shim import get_client


def main() -> None:
    parser = argparse.ArgumentParser(prog="dsg")
    parser.add_argument("command", choices=["health", "metrics", "ledger", "execute"])
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("--agent-id")
    parser.add_argument("--action")
    parser.add_argument("--payload", default="{}")
    args = parser.parse_args()

    client = get_client(args.base_url)

    if args.command == "health":
        print(json.dumps(client.health(), indent=2))
    elif args.command == "metrics":
        print(json.dumps(client.metrics(), indent=2))
    elif args.command == "ledger":
        print(json.dumps(client.ledger(), indent=2))
    elif args.command == "execute":
        if not args.agent_id or not args.action:
            raise SystemExit("--agent-id and --action are required for execute")
        payload = json.loads(args.payload)
        print(json.dumps(client.execute(args.agent_id, args.action, payload), indent=2))


if __name__ == "__main__":
    main()
