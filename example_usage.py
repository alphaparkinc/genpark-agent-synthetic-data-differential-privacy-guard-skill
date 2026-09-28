from client import AgentSyntheticDataDifferentialPrivacyGuard
import json

def main():
    guard = AgentSyntheticDataDifferentialPrivacyGuard()
    res = guard.run_benchmark_differential_privacy()
    print("Differential Privacy Guard Benchmark Result:")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
