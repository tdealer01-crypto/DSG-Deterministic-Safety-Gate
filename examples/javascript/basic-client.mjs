import { DSGClient } from '../../sdk-js/index.js'

const client = new DSGClient('http://localhost:8000')

console.log(await client.health())
console.log(await client.execute('agt_demo', 'scan', { target: 'node-1' }))
