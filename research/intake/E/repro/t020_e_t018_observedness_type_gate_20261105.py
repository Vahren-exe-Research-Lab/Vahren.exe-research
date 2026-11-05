"""T018/T020: E 22:44 evidence-kind/observed-value admission regression.

Owner E; historical ID E-OFFLINE-UNSYNCED-20261020-2244-CNB02-EVIDENCE-CLASS-01.
Pure synthetic metadata validation. No original-game/native result or Golden/READY.
"""
import unittest

SITES = ("VS_toono", "VS_inyume", "yaju_VS_ton", "inyume_dead_to_win")


def review_evidence(record):
    """Fail closed: a NOT_RUN predicate cannot silently become observed truth.

    Input: {'evidence_kind': str, 'read_sites': {site_name: bool | None}}.
    Empty/absent values are not observations. DYNAMIC labels require independent
    source/run attestation unavailable to this pure-Python diagnostic.
    """
    result = {"classification": "INVALID_METADATA", "actual_golden_pass": False,
              "strict_match": False, "ready": False}
    if type(record) is not dict or set(record) != {"evidence_kind", "read_sites"}:
        return result
    kind, sites = record["evidence_kind"], record["read_sites"]
    if type(kind) is not str or kind not in ("NOT_RUN", "SYNTHETIC", "DYNAMIC"):
        return result
    if type(sites) is not dict or not set(sites).issubset(SITES):
        return result
    if any(type(site) is not str for site in sites):
        return result
    if any(value is not None and type(value) is not bool for value in sites.values()):
        return result
    observed = any(type(value) is bool for value in sites.values())
    if kind == "NOT_RUN":
        result["classification"] = "PROVENANCE_CONFLICT_NOT_RUN_WITH_VALUES" if observed else "NOT_RUN_UNOBSERVED"
    elif kind == "SYNTHETIC":
        result["classification"] = "SYNTHETIC_PREDICATES_ONLY" if observed else "SYNTHETIC_NO_PREDICATES"
    else:
        result["classification"] = "DYNAMIC_WITNESS_UNVERIFIED"
    return result


class HistoricalEvidenceClassRegression(unittest.TestCase):
    def check(self, kind, sites, expected):
        result = review_evidence({"evidence_kind": kind, "read_sites": sites})
        self.assertEqual(result["classification"], expected)
        self.assertIs(result["actual_golden_pass"], False)
        self.assertIs(result["strict_match"], False)
        self.assertIs(result["ready"], False)

    def test_01_historical_not_run_zero_filled(self):
        self.check("NOT_RUN", {"VS_toono": True}, "PROVENANCE_CONFLICT_NOT_RUN_WITH_VALUES")

    def test_02_false_is_observed_value_too(self):
        self.check("NOT_RUN", {"VS_toono": False}, "PROVENANCE_CONFLICT_NOT_RUN_WITH_VALUES")

    def test_03_null_not_run(self):
        self.check("NOT_RUN", {"VS_toono": None}, "NOT_RUN_UNOBSERVED")

    def test_04_empty_not_run(self):
        self.check("NOT_RUN", {}, "NOT_RUN_UNOBSERVED")

    def test_05_four_null_sites_not_run(self):
        self.check("NOT_RUN", dict.fromkeys(SITES), "NOT_RUN_UNOBSERVED")

    def test_06_mixed_null_and_true_conflict(self):
        self.check("NOT_RUN", {"VS_toono": None, "VS_inyume": True}, "PROVENANCE_CONFLICT_NOT_RUN_WITH_VALUES")

    def test_07_false_in_death_epoch_conflict(self):
        self.check("NOT_RUN", {"inyume_dead_to_win": False}, "PROVENANCE_CONFLICT_NOT_RUN_WITH_VALUES")

    def test_08_synthetic_true_never_observation(self):
        self.check("SYNTHETIC", {"VS_toono": True}, "SYNTHETIC_PREDICATES_ONLY")

    def test_09_synthetic_false_not_run(self):
        self.check("SYNTHETIC", {"VS_toono": False}, "SYNTHETIC_PREDICATES_ONLY")

    def test_10_synthetic_null(self):
        self.check("SYNTHETIC", {"VS_toono": None}, "SYNTHETIC_NO_PREDICATES")

    def test_11_synthetic_independent_epochs(self):
        self.check("SYNTHETIC", {"VS_toono": True, "VS_inyume": False}, "SYNTHETIC_PREDICATES_ONLY")

    def test_12_dynamic_self_claim_not_golden(self):
        self.check("DYNAMIC", {"VS_toono": True}, "DYNAMIC_WITNESS_UNVERIFIED")

    def test_13_dynamic_null_not_golden(self):
        self.check("DYNAMIC", {}, "DYNAMIC_WITNESS_UNVERIFIED")

    def test_14_bool_not_a_kind(self):
        self.check(True, {}, "INVALID_METADATA")

    def test_15_typo_kind(self):
        self.check("NOTRUN", {}, "INVALID_METADATA")

    def test_16_unknown_epoch(self):
        self.check("NOT_RUN", {"invented_site": True}, "INVALID_METADATA")

    def test_17_int_is_not_bool(self):
        self.check("NOT_RUN", {"VS_toono": 1}, "INVALID_METADATA")

    def test_18_nonbool_string(self):
        self.check("NOT_RUN", {"VS_toono": "false"}, "INVALID_METADATA")

    def test_19_forged_extra_metadata(self):
        r = review_evidence({"evidence_kind":"DYNAMIC", "read_sites":{},"native_verified":True})
        self.assertEqual(r["classification"], "INVALID_METADATA")

    def test_20_nonobject_record(self):
        self.assertEqual(review_evidence(None)["classification"], "INVALID_METADATA")

    def test_21_nonobject_sites(self):
        self.check("SYNTHETIC", [], "INVALID_METADATA")

    def test_22_all_four_synthetic_conflicting_conditions_not_native(self):
        self.check("SYNTHETIC", dict(zip(SITES, (True, False, True, False))), "SYNTHETIC_PREDICATES_ONLY")

    def test_23_bools_rejected_as_site_key(self):
        self.check("NOT_RUN", {True: True}, "INVALID_METADATA")

    def test_24_other_evidence_kind_not_admitted(self):
        self.check("STATIC", {"VS_toono": True}, "INVALID_METADATA")


if __name__ == "__main__":
    unittest.main(verbosity=2)
