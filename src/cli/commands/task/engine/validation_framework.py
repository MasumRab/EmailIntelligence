import yaml
from typing import Dict, Any

class Validator:
    """Natural Language Validation Layer for Branch Clustering"""

    ALLOWED_CONDITIONS = {"branch_contains", "branch_not_contains", "path_contains", "has_tag", "has_import"}
    ALLOWED_ASSERTIONS = {"target", "confidence_min"}

    def __init__(self, rules_file: str):
        with open(rules_file, 'r') as f:
            self.rules = yaml.safe_load(f)

        # Fail fast on load if unknown keys exist in schema
        for rule in self.rules.get("rules", []):
            cond_keys = set(rule.get("condition", {}).keys())
            assert_keys = set(rule.get("assert", {}).keys())
            invalid_cond = cond_keys - self.ALLOWED_CONDITIONS
            invalid_assert = assert_keys - self.ALLOWED_ASSERTIONS
            if invalid_cond:
                raise ValueError(f"Rule '{rule.get('name')}' has invalid condition keys: {invalid_cond}")
            if invalid_assert:
                raise ValueError(f"Rule '{rule.get('name')}' has invalid assert keys: {invalid_assert}")

    def validate(self, clustering_results: Dict[str, Any]) -> bool:
        """Translates NL rules to assertions against the output JSON."""
        assignments = clustering_results.get("assignments", {})
        all_passed = True

        print("\n--- Running Natural Language Validations ---")
        for rule in self.rules.get("rules", []):
            name = rule.get("name")
            label = rule.get("label", "heuristic_proposed")
            provenance = rule.get("provenance", "No evidence source provided")

            print(f"Validating Rule: {name}")
            print(f"  Label: [{label}] -> {provenance}")

            condition = rule.get("condition", {})
            assertion = rule.get("assert", {})

            for branch, data in assignments.items():
                if self._matches_condition(branch, data, condition):
                    passed = self._check_assertion(data, assertion)
                    if not passed:
                        print(f"    ❌ FAILED for branch '{branch}'")
                        target = data.get('target')
                        confidence = data.get('confidence', 0)
                        print(f"       Expected {assertion}, got {target} (Conf: {confidence})")
                        all_passed = False
                    else:
                        print(f"    ✅ PASSED for branch '{branch}'")

        return all_passed

    def _matches_condition(self, branch: str, data: Dict[str, Any], condition: Dict[str, Any]) -> bool:
        # Schema validation is guaranteed during init, so we just evaluate
        if "branch_contains" in condition:
            if condition["branch_contains"] not in branch:
                return False

        if "branch_not_contains" in condition:
            if condition["branch_not_contains"] in branch:
                return False

        if "path_contains" in condition:
            files = data.get("metrics", {}).get("files_changed", [])
            if not any(condition["path_contains"] in f for f in files):
                return False

        if "has_tag" in condition:
            if condition["has_tag"] not in data.get("tags", []):
                return False

        if "has_import" in condition:
            imports = data.get("metrics", {}).get("imports", [])
            if not any(condition["has_import"] in i for i in imports):
                return False

        return True

    def _check_assertion(self, data: Dict[str, Any], assertion: Dict[str, Any]) -> bool:
        if "target" in assertion and data.get("target") != assertion["target"]:
            return False

        if "confidence_min" in assertion and data.get("confidence", 0) < assertion["confidence_min"]:
            return False

        return True
