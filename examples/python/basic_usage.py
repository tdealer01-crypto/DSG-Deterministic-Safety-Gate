from dsg.gate import DSGGate, DSGRequest


def main() -> None:
    gate = DSGGate()
    request = DSGRequest(
        agent="agent-demo",
        state_next={
            "value": 10.0,
            "is_grounded": True,
            "intent_score": 1,
            "is_api_clean": True,
            "source_verified": True,
            "compute_cost": 100,
            "has_audit_trail": True,
            "nonce_lock": True,
        },
        signals=[0.9, 0.9, 0.9],
        nonce="example-nonce-001",
    )

    result = gate.process_request(request)
    print(result.model_dump())


if __name__ == "__main__":
    main()
