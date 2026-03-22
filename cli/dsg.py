#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import secrets
from pathlib import Path

from sdk_python_shim import get_client
from validator_shim import load_policy_file, validate_policy


def main() -> None:
    parser = argparse.ArgumentParser(prog="dsg")
    parser.add_argument(
        "command",
        choices=["health", "metrics", "ledger", "execute", "generate-api-key", "validate-policy"],
    )
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("--agent-id")
    parser.add_argument("--action")
    parser.add_argument("--payload", default="{}")
    parser.add_argument("--path")
    args = parser.parse_args()

    if args.command == "generate-api-key":
        print(secrets.token_hex(32))
        return

    if args.command == "validate-policy":
        if not args.path:
            raise SystemExit("--path is required for validate-policy")
        policy = load_policy_file(Path(args.path))
        errors = validate_policy(policy)
        if errors:
            print(json.dumps({"valid": False, "errors": errors}, indent=2))
            raise SystemExit(1)
        print(json.dumps({"valid": True}, indent=2))
        return

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
