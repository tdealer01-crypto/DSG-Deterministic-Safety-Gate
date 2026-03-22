from dsg import DSGClient

client = DSGClient(base_url="http://localhost:8000")

print(client.health())
print(client.execute("agt_demo", "scan", {"target": "node-1"}))
