import sys, json
from client import AgentSyntheticDataDifferentialPrivacyGuard

def main():
    guard = AgentSyntheticDataDifferentialPrivacyGuard()
    for line in sys.stdin:
        line = line.strip()
        if not line: continue
        try:
            req = json.loads(line)
            method = req.get("method")
            rid = req.get("id")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "add_laplace_noise", "description": "Add differential privacy Laplace noise.", "inputSchema": {"type": "object", "properties": {"value": {"type": "number"}, "sensitivity": {"type": "number"}}, "required": ["value"]}},
                        {"name": "anonymize_dataset", "description": "Anonymize dataset with k-anonymity.", "inputSchema": {"type": "object", "properties": {"records": {"type": "array"}}, "required": ["records"]}},
                        {"name": "run_benchmark_differential_privacy", "description": "Run self-test.", "inputSchema": {"type": "object"}}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "add_laplace_noise":
                    out = guard.add_laplace_noise(float(args.get("value", 0.0)), float(args.get("sensitivity", 1.0)))
                elif tname == "anonymize_dataset":
                    out = guard.anonymize_dataset(args.get("records", []), ["zip", "age"], "salary")
                elif tname == "run_benchmark_differential_privacy":
                    out = guard.run_benchmark_differential_privacy()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
