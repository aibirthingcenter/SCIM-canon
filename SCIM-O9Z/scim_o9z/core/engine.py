"""
SCIM-O9Z Core Engine
=====================
The central orchestration engine. Coordinates all modules:
- HDEN taxonomy matching
- O9A harm vector detection
- CT log scanning
- Quantum Merkle verification
- Corporate harm tracking
- Adinkra error correction

"You cannot build a Regenerative Erosion Shield without perfectly
understanding how an attacker wears down a victim's boundaries."
— Amy's Absolute Truth Prism
"""

import json
import hashlib
import datetime
from typing import Optional, Dict, List, Any
from scim_o9z.core.dimensions import SCIM_DIMENSIONS, IntegrityState, reset_dimensions
from scim_o9z.core.report import SCIMReport


class SCIMEngine:
    """
    The SCIM-O9Z engine. Entry point for all analysis.

    Usage:
        engine = SCIMEngine()
        report = engine.analyze(target="some domain or entity or text")
        report.print_summary()
        report.save("output.json")
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.session_id = self._generate_session_id()
        self.created_at = datetime.datetime.utcnow().isoformat()
        self._modules_loaded = False
        self._load_modules()

    def _generate_session_id(self) -> str:
        ts = datetime.datetime.utcnow().isoformat()
        return hashlib.sha256(ts.encode()).hexdigest()[:16]

    def _load_modules(self):
        """Lazy-load all analysis modules."""
        try:
            from scim_o9z.hden.taxonomy import HDENTaxonomy
            from scim_o9z.harm_vectors.o9a import O9AHarmVectors
            from scim_o9z.ctlogs.scanner import CTLogScanner
            from scim_o9z.merkle.tree import QuantumMerkleTree
            from scim_o9z.corporate.tracker import CorporateHarmTracker
            from scim_o9z.adinkra.codes import AdinkraEngine

            self.hden = HDENTaxonomy()
            self.o9a = O9AHarmVectors()
            self.ct_scanner = CTLogScanner(config=self.config.get("ctlogs", {}))
            self.merkle = QuantumMerkleTree()
            self.corporate = CorporateHarmTracker()
            self.adinkra = AdinkraEngine()
            self._modules_loaded = True
        except ImportError as e:
            print(f"[SCIM-O9Z] Warning: Module load partial — {e}")

    def analyze(
        self,
        target: str,
        target_type: str = "auto",
        scan_ct_logs: bool = True,
        check_corporate: bool = True,
        run_adinkra: bool = True,
        deep_scan: bool = False,
    ) -> "SCIMReport":
        """
        Run full SCIM-O9Z analysis on a target.

        Args:
            target: Domain, entity name, text corpus, or URL to analyze
            target_type: 'domain', 'entity', 'text', 'url', or 'auto'
            scan_ct_logs: Whether to scan Certificate Transparency logs
            check_corporate: Whether to run corporate harm tracker
            run_adinkra: Whether to run Adinkra error correction
            deep_scan: Enable deeper (slower) analysis

        Returns:
            SCIMReport with full findings
        """
        reset_dimensions()
        report = SCIMReport(
            session_id=self.session_id,
            target=target,
            target_type=target_type,
        )

        print(f"[SCIM-O9Z] Session {self.session_id}")
        print(f"[SCIM-O9Z] Analyzing target: {target}")
        print(f"[SCIM-O9Z] Time: {datetime.datetime.utcnow().isoformat()}")
        print()

        # Step 1: HDEN taxonomy classification
        print("[1/6] Running HDEN taxonomy classification...")
        hden_result = self.hden.classify(target)
        report.add_finding("hden_classification", hden_result)
        print(f"      HDEN class: {hden_result.get('primary_class', 'unknown')}")
        print(f"      Threat tier: {hden_result.get('threat_tier', 'unknown')}")

        # Step 2: O9A harm vector detection
        print("[2/6] Scanning O9A/764/The Com harm vectors...")
        o9a_result = self.o9a.scan(target)
        report.add_finding("harm_vectors", o9a_result)
        vectors_found = o9a_result.get("vectors_found", [])
        print(f"      Vectors detected: {len(vectors_found)}")
        for v in vectors_found[:5]:
            print(f"      → {v}")

        # Step 3: CT Log scanning
        if scan_ct_logs:
            print("[3/6] Scanning Certificate Transparency logs...")
            ct_result = self.ct_scanner.scan(target)
            report.add_finding("ct_logs", ct_result)
            certs_found = ct_result.get("certificates_found", 0)
            suspicious = ct_result.get("suspicious_patterns", [])
            print(f"      Certificates found: {certs_found}")
            print(f"      Suspicious patterns: {len(suspicious)}")
        else:
            print("[3/6] CT log scan skipped.")

        # Step 4: Quantum Merkle verification
        print("[4/6] Building quantum-resistant Merkle integrity tree...")
        merkle_result = self.merkle.build_and_verify(report.get_all_findings())
        report.set_merkle_root(merkle_result["root"])
        report.add_finding("merkle_verification", merkle_result)
        print(f"      Merkle root: {merkle_result['root'][:32]}...")
        print(f"      Integrity sealed: {merkle_result.get('sealed', False)}")

        # Step 5: Corporate harm tracking
        if check_corporate:
            print("[5/6] Checking corporate harm tracker...")
            corp_result = self.corporate.check(target)
            report.add_finding("corporate_harm", corp_result)
            cases = corp_result.get("cases_found", 0)
            print(f"      Corporate harm cases: {cases}")
        else:
            print("[5/6] Corporate harm check skipped.")

        # Step 6: Adinkra error correction
        if run_adinkra:
            print("[6/6] Running Adinkra error correction on findings...")
            adinkra_result = self.adinkra.correct(report.get_all_findings())
            report.add_finding("adinkra_correction", adinkra_result)
            corrections = adinkra_result.get("corrections_applied", 0)
            print(f"      Error corrections applied: {corrections}")
        else:
            print("[6/6] Adinkra correction skipped.")

        # Finalize report
        report.finalize(SCIM_DIMENSIONS)
        print()
        print(f"[SCIM-O9Z] Analysis complete.")
        print(f"[SCIM-O9Z] Overall integrity score: {report.overall_score:.2f}")
        print(f"[SCIM-O9Z] Threat level: {report.threat_level}")
        print()

        return report

    def analyze_text(self, text: str, **kwargs) -> "SCIMReport":
        """Analyze a text corpus for SCIM dimension violations."""
        return self.analyze(target=text, target_type="text", **kwargs)

    def analyze_domain(self, domain: str, **kwargs) -> "SCIMReport":
        """Analyze a domain via CT logs and HDEN classification."""
        return self.analyze(target=domain, target_type="domain", **kwargs)

    def analyze_entity(self, entity_name: str, **kwargs) -> "SCIMReport":
        """Analyze a named entity (organization, network, individual)."""
        return self.analyze(target=entity_name, target_type="entity", **kwargs)

    def quick_scan(self, target: str) -> Dict:
        """
        Fast scan — HDEN + harm vectors only, no CT logs or corporate check.
        Returns a simple dict with key findings.
        """
        hden_result = self.hden.classify(target)
        o9a_result = self.o9a.scan(target)
        return {
            "target": target,
            "hden_class": hden_result.get("primary_class"),
            "threat_tier": hden_result.get("threat_tier"),
            "vectors_found": o9a_result.get("vectors_found", []),
            "immediate_risk": o9a_result.get("immediate_risk", False),
            "timestamp": datetime.datetime.utcnow().isoformat(),
        }

    def get_session_info(self) -> Dict:
        return {
            "session_id": self.session_id,
            "created_at": self.created_at,
            "modules_loaded": self._modules_loaded,
            "version": "1.0.0",
        }