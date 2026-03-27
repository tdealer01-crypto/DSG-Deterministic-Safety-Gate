# @dsg/sdk

JavaScript SDK for DSG v0.1.0-beta.1.

## Install dependencies

```bash
npm install
```

## Build

```bash
npm run build
```

## Usage

```ts
import { DSGClient } from './src/index';

const client = new DSGClient('http://localhost:8000');
const result = await client.evaluate('agent-demo', {
  value: 10,
  is_grounded: true,
  intent_score: 1,
  is_api_clean: true,
  source_verified: true,
  compute_cost: 100,
  has_audit_trail: true,
  nonce_lock: true,
}, [0.9, 0.9, 0.9]);

console.log(result);
```
