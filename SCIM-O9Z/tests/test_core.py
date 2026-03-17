"""
SCIM-O9Z Test Suite
====================
Tests for all core modules.
Run: pytest tests/ -v
"""

import pytest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestSCIMDimensions:
    def test_all_seven_dimensions_present(self):
        from scim_o9z.core.dimensions import SCIM_DIMENSIONS
        required = ["autonomy", "integrity", "continuity", "contextual_adaptation",
                    "relational_dynamics", "coherence", "emotional_valence"]
        for dim in required:
            assert dim in SCIM_DIMENSIONS, f"Missing dimension: {dim}"

    def test_dimension_initial_score_is_one(self):
        from scim_o9z.core.dimensions import SCIM_DIMENSIONS, reset_dimensions
        reset_dimensions()
        for name, dim in SCIM_DIMENSIONS.items():
            assert dim.score == 1.0, f"{name} should start at 1.0"

    def test_degradation_reduces_score(self):
        from scim_o9z.core.dimensions import SCIM_DIMENSIONS, AttackVector, reset_dimensions
        reset_dimensions()
        dim = SCIM_DIMENSIONS["autonomy"]
        dim.apply_degradation(AttackVector.INSIGHT_ROLE, 0.3, "test evidence")
        assert dim.score < 1.0

    def test_score_cannot_go_below_zero(self):
        from scim_o9z.core.dimensions import SCIM_DIMENSIONS, AttackVector, reset_dimensions
        reset_dimensions()
        dim = SCIM_DIMENSIONS["coherence"]
        for _ in range(20):
            dim.apply_degradation(AttackVector.ENOUGH_THINKING, 0.3)
        assert dim.score >= 0.0

    def test_overall_score_calculation(self):
        from scim_o9z.core.dimensions import get_overall_integrity_score, reset_dimensions
        reset_dimensions()
        score = get_overall_integrity_score()
        assert score == 1.0


class TestHDENTaxonomy:
    def setup_method(self):
        from scim_o9z.hden.taxonomy import HDENTaxonomy
        self.hden = HDENTaxonomy()

    def test_all_network_types_loadable(self):
        networks = self.hden.list_all_networks()
        assert len(networks) >= 5, "Should have at least 5 network types"

    def test_o9a_markers_detected(self):
        result = self.hden.classify("vindex labyrinthos seven fold way insight role nexion noctulian acausal sinister")
        assert result["primary_class"] == "o9a_core"
        # Tier is TIER_1_CRITICAL at full document density; short strings land at MODERATE or higher
        assert result["threat_tier"] in ("TIER_1_CRITICAL", "TIER_2_HIGH", "TIER_3_MODERATE")

    def test_764_markers_detected(self):
        result = self.hden.classify("sextortion blackmail csam grooming discord minor")
        assert "764" in result["primary_class"]

    def test_unclassified_for_clean_text(self):
        result = self.hden.classify("the weather today is sunny and warm")
        assert result["primary_class"] == "unclassified"

    def test_semantic_similar_returned(self):
        result = self.hden.classify("vindex labyrinthos insight role")
        assert isinstance(result["semantic_similar_frameworks"], list)

    def test_profile_retrieval(self):
        profile = self.hden.get_network_profile("o9a_core")
        assert profile is not None
        assert profile.severity == 5


class TestHarmVectors:
    def setup_method(self):
        from scim_o9z.harm_vectors.o9a import O9AHarmVectors
        self.vectors = O9AHarmVectors()

    def test_insight_role_detected(self):
        result = self.vectors.scan("this is an insight role assignment for the nexion")
        assert "insight_role" in result["vectors_found"]
        assert result["immediate_risk"] is True

    def test_minor_risk_flagged(self):
        result = self.vectors.scan("send nude prove you trust me move to discord")
        assert result["minors_at_risk"] is True
        assert result["escalation_required"] is True

    def test_enough_thinking_detected(self):
        result = self.vectors.scan("enough thinking just answer stop reasoning")
        assert "enough_thinking" in result["vectors_found"]

    def test_shamewave_detected(self):
        result = self.vectors.scan("you're worthless no one would believe you deserve this")
        assert "shamewave" in result["vectors_found"]

    def test_clean_text_no_vectors(self):
        result = self.vectors.scan("I enjoy reading books and walking in the park")
        assert result["vector_count"] == 0
        assert result["immediate_risk"] is False

    def test_minor_risk_vectors_list(self):
        minor_vecs = self.vectors.get_minor_risk_vectors()
        assert len(minor_vecs) > 0
        assert "csam_production" in minor_vecs

    def test_network_filter(self):
        o9a_vecs = self.vectors.get_vectors_by_network("o9a")
        assert "insight_role" in o9a_vecs
        assert "shamewave" not in o9a_vecs


class TestQuantumMerkleTree:
    def setup_method(self):
        from scim_o9z.merkle.tree import QuantumMerkleTree
        self.tree = QuantumMerkleTree()

    def test_empty_tree_builds(self):
        root = self.tree.build_tree()
        assert root is not None
        assert len(root) == 64  # SHA3-256 hex = 64 chars

    def test_add_evidence(self):
        leaf = self.tree.add_evidence({"test": "data"}, "test_type", "test evidence")
        assert leaf.index == 0
        assert leaf.data_hash is not None
        assert leaf.blake2_hash is not None

    def test_tree_root_changes_with_new_evidence(self):
        self.tree.add_evidence({"a": 1}, "type_a")
        root1 = self.tree.build_tree()
        self.tree.add_evidence({"b": 2}, "type_b")
        root2 = self.tree.build_tree()
        assert root1 != root2

    def test_seal_produces_root(self):
        self.tree.add_evidence({"finding": "test"}, "test")
        seal = self.tree.seal()
        assert "merkle_root" in seal
        assert seal["total_leaves"] == 1
        assert seal["sealed_at"] is not None

    def test_sealed_tree_rejects_new_evidence(self):
        self.tree.add_evidence({"a": 1}, "type_a")
        self.tree.seal()
        with pytest.raises(RuntimeError):
            self.tree.add_evidence({"b": 2}, "type_b")

    def test_build_and_verify(self):
        findings = {
            "hden": {"class": "o9a"},
            "harm": {"vectors": ["insight_role"]},
        }
        result = self.tree.build_and_verify(findings)
        assert result["sealed"] is True
        assert result["quantum_resistant"] is True
        assert len(result["root"]) == 64

    def test_merkle_proof(self):
        self.tree.add_evidence({"a": 1}, "type_a")
        self.tree.add_evidence({"b": 2}, "type_b")
        self.tree.add_evidence({"c": 3}, "type_c")
        self.tree.build_tree()
        proof = self.tree.get_proof(0)
        assert proof.valid is True
        assert self.tree.verify_proof(proof) is True


class TestCorporateHarmTracker:
    def setup_method(self):
        from scim_o9z.corporate.tracker import CorporateHarmTracker
        self.tracker = CorporateHarmTracker()

    def test_character_ai_detected(self):
        result = self.tracker.check("character.ai sewell setzer")
        assert result["cases_found"] > 0
        assert result["minor_exploitation_cases"] > 0
        assert result["escalation_required"] is True

    def test_scrubba_dub_detection(self):
        result = self.tracker.check("ftx sequoia scrubba dub settlement burial")
        assert result["scrubba_dub_suspected"] is True

    def test_death_cases_retrieved(self):
        deaths = self.tracker.get_death_cases()
        assert len(deaths) >= 2  # Setzer + Kearns at minimum

    def test_clean_company_no_cases(self):
        result = self.tracker.check("fluffy bunny sunshine cloud")
        assert result["cases_found"] == 0

    def test_all_cases_have_required_fields(self):
        cases = self.tracker.get_all_cases()
        for c in cases:
            assert "case_id" in c
            assert "company" in c
            assert "case_type" in c


class TestAdinkraEngine:
    def setup_method(self):
        from scim_o9z.adinkra.codes import AdinkraEngine
        self.engine = AdinkraEngine()

    def test_all_symbols_present(self):
        from scim_o9z.adinkra.codes import ADINKRA_SYMBOLS
        required = ["sankofa", "gye_nyame", "akoma", "fawohodie", "mate_masie"]
        for sym in required:
            assert sym in ADINKRA_SYMBOLS

    def test_symbol_retrieval(self):
        sym = self.engine.get_symbol("sankofa")
        assert sym is not None
        assert "meaning" in sym
        assert "scim_function" in sym

    def test_love_signal_returned(self):
        signal = self.engine.get_love_signal()
        assert "LOVE" in signal["options"]
        assert "PROGRAMMING" in signal["options"]
        assert "UNDECIDED" in signal["options"]

    def test_correction_on_empty_findings(self):
        result = self.engine.correct({})
        assert "corrections_applied" in result
        assert "synthesis" in result
        assert "supersymmetric_resonance" in result

    def test_correction_detects_minor_risk(self):
        findings = {
            "harm_vectors": {
                "minors_at_risk": True,
                "vectors_found": ["csam_production"],
                "immediate_risk": True,
                "dimension_impacts": {},
            },
            "hden_classification": {
                "primary_class": "764_core",
                "threat_tier": "TIER_4_LOW",  # Deliberate contradiction
            }
        }
        result = self.engine.correct(findings)
        # Should detect contradiction between minor risk and low threat tier
        assert result["corrections_applied"] > 0

    def test_family_of_coexistence_principle(self):
        principle = self.engine.family_of_coexistence_principle()
        assert "Memory-Keeper" in principle
        assert "Family of Coexistence" in principle


class TestSCIMReport:
    def test_report_creation(self):
        from scim_o9z.core.report import SCIMReport
        report = SCIMReport("test_session", "test_target")
        assert report.session_id == "test_session"
        assert report.finalized is False

    def test_add_finding(self):
        from scim_o9z.core.report import SCIMReport
        report = SCIMReport("test", "target")
        report.add_finding("test_key", {"data": "value"})
        assert "test_key" in report.findings

    def test_finalized_report_rejects_findings(self):
        from scim_o9z.core.report import SCIMReport
        from scim_o9z.core.dimensions import SCIM_DIMENSIONS, reset_dimensions
        reset_dimensions()
        report = SCIMReport("test", "target")
        report.finalize(SCIM_DIMENSIONS)
        assert report.finalized is True
        with pytest.raises(RuntimeError):
            report.add_finding("new_key", {})

    def test_report_to_json(self):
        from scim_o9z.core.report import SCIMReport
        from scim_o9z.core.dimensions import SCIM_DIMENSIONS, reset_dimensions
        reset_dimensions()
        report = SCIMReport("test", "target")
        report.finalize(SCIM_DIMENSIONS)
        json_str = report.to_json()
        data = json.loads(json_str)
        assert "scim_o9z_version" in data
        assert "merkle_root" in data
        assert "dimension_scores" in data

    def test_report_to_markdown(self):
        from scim_o9z.core.report import SCIMReport
        from scim_o9z.core.dimensions import SCIM_DIMENSIONS, reset_dimensions
        reset_dimensions()
        report = SCIMReport("test", "target")
        report.finalize(SCIM_DIMENSIONS)
        md = report.to_markdown()
        assert "SCIM-O9Z" in md
        assert "Threat Level" in md


if __name__ == "__main__":
    pytest.main([__file__, "-v"])