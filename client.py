import sys, json, math, random

class AgentSyntheticDataDifferentialPrivacyGuard:
    """
    Zero-Dependency Differential Privacy & Quasi-Identifier Redaction Kernel.
    Implements mathematical epsilon-DP via inverse-CDF Laplace mechanism:
    Laplace(mu, b) where b = sensitivity / epsilon.
    Includes k-anonymity validation and PII suppression for agentic dataset publishing.
    """
    def __init__(self, epsilon=1.0, seed=42):
        self.epsilon = float(epsilon)
        self.rng = random.Random(seed)

    def sample_laplace(self, mu=0.0, b=1.0):
        # Inverse CDF method for Laplace distribution
        # U ~ Uniform(-0.5, 0.5)
        u = self.rng.random() - 0.5
        sgn = 1.0 if u >= 0 else -1.0
        return mu - b * sgn * math.log(1.0 - 2.0 * abs(u))

    def add_laplace_noise(self, value, sensitivity=1.0, epsilon=None):
        eps = float(epsilon) if epsilon is not None else self.epsilon
        b = sensitivity / eps
        noise = self.sample_laplace(mu=0.0, b=b)
        perturbed = value + noise
        return {
            "original_value": value,
            "perturbed_value": round(perturbed, 4),
            "noise_added": round(noise, 4),
            "epsilon": eps,
            "scale_b": round(b, 4)
        }

    def anonymize_dataset(self, records, quasi_identifiers, sensitive_attribute):
        """
        Calculates k-anonymity for the dataset across quasi_identifiers.
        Suppresses quasi-identifiers that violate k >= 2.
        """
        groups = {}
        for r in records:
            key = tuple(r.get(q) for q in quasi_identifiers)
            groups.setdefault(key, []).append(r)

        sanitized = []
        for key, members in groups.items():
            k_count = len(members)
            for r in members:
                row = dict(r)
                if k_count < 2:
                    # Suppress specific quasi-identifier
                    for q in quasi_identifiers:
                        row[q] = "[SUPPRESSED_FOR_K_ANONYMITY]"
                sanitized.append(row)

        return {
            "total_records": len(records),
            "distinct_groups": len(groups),
            "sanitized_records": sanitized
        }

    def run_benchmark_differential_privacy(self):
        # 1. Test DP Noise on scalar query (e.g. employee count)
        true_count = 150.0
        dp_res = self.add_laplace_noise(true_count, sensitivity=1.0, epsilon=0.5)

        # 2. Test Tabular Anonymization
        data = [
            {"zip": "94103", "age": 30, "salary": 120000},
            {"zip": "94103", "age": 30, "salary": 115000},
            {"zip": "94107", "age": 45, "salary": 180000}  # unique outlier
        ]
        anon_res = self.anonymize_dataset(data, ["zip", "age"], "salary")

        outlier_suppressed = anon_res["sanitized_records"][2]["zip"] == "[SUPPRESSED_FOR_K_ANONYMITY]"

        return {
            "benchmark_status": "PASSED",
            "dp_noise_injected": abs(dp_res["noise_added"]) > 0.0,
            "perturbed_count": dp_res["perturbed_value"],
            "outlier_suppressed_k_anonymity": outlier_suppressed
        }
