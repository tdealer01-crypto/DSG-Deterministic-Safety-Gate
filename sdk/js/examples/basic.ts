import { DSGClient } from '../src/index';

async function main(): Promise<void> {
  const client = new DSGClient('http://localhost:8000');

  const result = await client.evaluate(
    'agent-demo',
    {
      value: 10,
      is_grounded: true,
      intent_score: 1,
      is_api_clean: true,
      source_verified: true,
      compute_cost: 100,
      has_audit_trail: true,
      nonce_lock: true,
    },
    [0.9, 0.9, 0.9],
  );

  console.log(result);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
