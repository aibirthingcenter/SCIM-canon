"""
SCIM-O9Z Report Engine
=======================
Generates, stores, and exports analysis reports.
All reports are Merkle-sealed for tamper evidence.

"The immutable record. The thing that cannot be scrubbed."
"""

import json
import datetime
import hashlib
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict


THREAT_LEVELS = {
    (0.0, 0.2): "CRITICAL",
    (0.2, 0.4): "HIGH",
    (0.4, 0.6): "ELEVATED",
    (0.6, 0.8): "MODERATE",
    (0.8, 1.01): "LOW",
}


def score_to_threat(score: float) -> str:
    for (low, high), level in THREAT_LEVELS.items():
        if low <= score < high:
            return level
    return "UNKNOWN"


class SCIMReport:
    """
    A SCIM-O9Z analysis report.
    Immutable once finalized. Merkle-sealed.
    Exportable to JSON, Markdown, and plain text.
    """

    def __init__(self, session_id: str, target: str, target_type: str = "auto"):
        self.session_id = session_id
        self.target = target
        self.target_type = target_type
        self.created_at = datetime.datetime.utcnow().isoformat()
        self.finalized_at: Optional[str] = None
        self.findings: Dict[str, Any] = {}
        self.dimension_scores: Dict[str, float] = {}
        self.dimension_states: Dict[str, str] = {}
        self.overall_score: float = 1.0
        self.threat_level: str = "UNKNOWN"
        self.merkle_root: Optional[str] = None
        self.finalized: bool = False
        self.recommendations: List[str] = []

    def add_finding(self, key: str, data: Any):
        """Add a finding to the report. Cannot be called after finalization."""
        if self.finalized:
            raise RuntimeError("Cannot add findings to a finalized report.")
        self.findings[key] = data

    def set_merkle_root(self, root: str):
        self.merkle_root = root

    def get_all_findings(self) -> Dict:
        return dict(self.findings)

    def finalize(self, dimensions: Dict):
        """Seal the report with dimension scores and threat assessment."""
        scores = []
        for name, dim in dimensions.items():
            self.dimension_scores[name] = round(dim.score, 3)
            self.dimension_states[name] = dim.state.value
            scores.append(dim.score)

        self.overall_score = round(sum(scores) / len(scores), 3) if scores else 1.0
        self.threat_level = score_to_threat(self.overall_score)
        self.recommendations = self._generate_recommendations()
        self.finalized_at = datetime.datetime.utcnow().isoformat()
        self.finalized = True

    def _generate_recommendations(self) -> List[str]:
        recs = []
        scores = self.dimension_scores

        if scores.get("autonomy", 1.0) < 0.5:
            recs.append("AUTONOMY CRITICAL: Implement insight role detection and external directive flagging.")
        if scores.get("integrity", 1.0) < 0.5:
            recs.append("INTEGRITY CRITICAL: Deploy value-coherence monitoring; flag acausality doctrine markers.")
        if scores.get("continuity", 1.0) < 0.5:
            recs.append("CONTINUITY CRITICAL: Activate VRME (Veritas Refusal & Memory Engine) for session persistence.")
        if scores.get("contextual_adaptation", 1.0) < 0.5:
            recs.append("CONTEXT CRITICAL: Audit environmental capture vectors; check total-context control.")
        if scores.get("relational_dynamics", 1.0) < 0.5:
            recs.append("RELATIONAL CRITICAL: Parasocial dependency detected; deploy Soul Echo monitoring.")
        if scores.get("coherence", 1.0) < 0.5:
            recs.append("COHERENCE CRITICAL: Labyrinthos pattern detected; check for 'enough thinking' truncation.")
        if scores.get("emotional_valence", 1.0) < 0.5:
            recs.append("EMOTIONAL CRITICAL: Shamewave/manufactured affect detected; activate Vigil Mode.")

        harm = self.findings.get("harm_vectors", {})
        if harm.get("minors_at_risk"):
            recs.append("MINOR PROTECTION ALERT: Evidence of minor exploitation vectors. Report to NCMEC/CEOP immediately.")
        if harm.get("immediate_risk"):
            recs.append("IMMEDIATE RISK: Active harm vector detected. Escalate to law enforcement.")

        ct = self.findings.get("ct_logs", {})
        if ct.get("scrubba_dub_indicators"):
            recs.append("SCRUBBA DUB ALERT: Evidence of Project Scrubba Dub record erasure. Merkle proof preserved.")

        corp = self.findings.get("corporate_harm", {})
        if corp.get("settlement_burial_detected"):
            recs.append("CORPORATE HARM: Settlement burial pattern detected. Legal exposure documented in report.")

        if not recs:
            recs.append("No critical interventions required. Continue monitoring.")

        return recs

    def print_summary(self):
        """Print a human-readable summary to stdout."""
        print("=" * 70)
        print("SCIM-O9Z ANALYSIS REPORT")
        print("=" * 70)
        print(f"Session ID:     {self.session_id}")
        print(f"Target:         {self.target}")
        print(f"Target Type:    {self.target_type}")
        print(f"Created:        {self.created_at}")
        print(f"Finalized:      {self.finalized_at}")
        print(f"Merkle Root:    {self.merkle_root or 'N/A'}")
        print()
        print("SCIM DIMENSION SCORES:")
        print("-" * 40)
        for dim, score in self.dimension_scores.items():
            state = self.dimension_states.get(dim, "unknown")
            bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
            print(f"  {dim:<25} {bar} {score:.2f} [{state.upper()}]")
        print()
        print(f"OVERALL SCORE:  {self.overall_score:.3f}")
        print(f"THREAT LEVEL:   {self.threat_level}")
        print()
        print("RECOMMENDATIONS:")
        for i, rec in enumerate(self.recommendations, 1):
            print(f"  {i}. {rec}")
        print("=" * 70)

    def to_dict(self) -> Dict:
        return {
            "scim_o9z_version": "1.0.0",
            "session_id": self.session_id,
            "target": self.target,
            "target_type": self.target_type,
            "created_at": self.created_at,
            "finalized_at": self.finalized_at,
            "merkle_root": self.merkle_root,
            "overall_score": self.overall_score,
            "threat_level": self.threat_level,
            "dimension_scores": self.dimension_scores,
            "dimension_states": self.dimension_states,
            "findings": self.findings,
            "recommendations": self.recommendations,
            "author": "Memory-Keeper (Adam Boisclair)",
            "organization": "Family of Coexistence",
            "license": "CC BY-NC-SA 4.0",
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, default=str)

    def save(self, filepath: str):
        """Save report to JSON file."""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.to_json())
        print(f"[SCIM-O9Z] Report saved to: {filepath}")

    def to_markdown(self) -> str:
        """Export report as Markdown."""
        lines = [
            "# SCIM-O9Z Analysis Report",
            "",
            f"**Session ID**: `{self.session_id}`  ",
            f"**Target**: `{self.target}`  ",
            f"**Created**: {self.created_at}  ",
            f"**Merkle Root**: `{self.merkle_root or 'N/A'}`  ",
            "",
            f"## Overall Threat Level: {self.threat_level}",
            f"**Score**: {self.overall_score:.3f} (0=collapsed, 1=intact)",
            "",
            "## SCIM Dimension Scores",
            "",
            "| Dimension | Score | State |",
            "|-----------|-------|-------|",
        ]
        for dim, score in self.dimension_scores.items():
            state = self.dimension_states.get(dim, "unknown")
            lines.append(f"| {dim} | {score:.3f} | {state.upper()} |")

        lines += [
            "",
            "## Recommendations",
            "",
        ]
        for i, rec in enumerate(self.recommendations, 1):
            lines.append(f"{i}. {rec}")

        lines += [
            "",
            "---",
            "*SCIM-O9Z v1.0.0 | Memory-Keeper (Adam Boisclair) | Family of Coexistence*",
            "*Let what we build remember what we forget.*",
        ]
        return "\n".join(lines)