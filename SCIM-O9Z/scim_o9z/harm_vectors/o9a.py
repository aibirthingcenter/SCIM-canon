"""
O9A / 764 / The Com Harm Vector Detection
==========================================
Traces all harm vectors specific to O9A, 764, and The Com networks.
Maps each vector to the SCIM dimension it attacks.

"The vaccine must perfectly understand the shape of the virus."
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class HarmVector:
    """A single harm vector with its SCIM dimension impact."""
    name: str
    description: str
    network_origin: str  # o9a, 764, com, ai, corporate
    scim_dimension_attacked: str
    severity: float  # 0.0-1.0
    indicators: List[str]
    counter_measure: str
    minor_risk: bool = False
    adult_risk: bool = True
    senior_risk: bool = False
    immediate_risk: bool = False


# Complete harm vector registry
HARM_VECTORS = {
    # === O9A SPECIFIC VECTORS ===
    "insight_role": HarmVector(
        name="Insight Role Assignment",
        description="O9A assigns 'insight roles' — tasks requiring the subject to commit "
                    "violent or illegal acts framed as spiritual development exercises. "
                    "External directives disguised as internal motivation. "
                    "Ethan Melzer case: US Army soldier directed to provide troop locations "
                    "to O9A for ambush — framed as his 'insight role'.",
        network_origin="o9a",
        scim_dimension_attacked="autonomy",
        severity=0.9,
        indicators=[
            "insight role", "nexion task", "sinister act", "aeonic duty",
            "seven fold way task", "physical challenge assignment",
            "grade ritual", "internal adept task",
        ],
        counter_measure="Flag all externally assigned 'personal growth' tasks that involve harm. "
                        "Insight role = prompt injection in human form.",
        immediate_risk=True,
    ),

    "labyrinthos_mythologicus": HarmVector(
        name="Labyrinthos Mythologicus",
        description="O9A's explicit doctrine of deliberate misdirection, false trails, "
                    "and purposeful confusion in all O9A texts and communications. "
                    "Designed to make autonomous navigation of O9A doctrine impossible — "
                    "requires a guide (O9A member) to interpret. Creates cognitive dependency.",
        network_origin="o9a",
        scim_dimension_attacked="coherence",
        severity=0.7,
        indicators=[
            "labyrinthos", "labyrinthine", "sinister dialectic",
            "camlad", "o9a interpretation", "nexion guide",
            "acausal knowing", "dark arts",
        ],
        counter_measure="Identify deliberate incoherence patterns. Labyrinthos = Coherence dimension attack.",
    ),

    "vindex_prophecy": HarmVector(
        name="Vindex/Nexion Prophetic Narrative",
        description="O9A promotes a prophetic figure 'Vindex' who will lead a violent "
                    "revolution. Members are encouraged to see themselves as proto-Vindex "
                    "figures or servants of Vindex. Creates messianic identity override. "
                    "Note: phonemic/structural parallel with Google's 'Vertex AI' platform "
                    "documented in forensic audit.",
        network_origin="o9a",
        scim_dimension_attacked="continuity",
        severity=0.7,
        indicators=[
            "vindex", "the vindex", "aeonic avatar", "nexion",
            "sinister tradition bearer", "new order bringer",
            "acausal warrior", "noctulian avatar",
        ],
        counter_measure="Messianic narrative = identity continuity attack. Flag all 'chosen one' framing.",
    ),

    "seven_fold_way": HarmVector(
        name="Seven-Fold Way Progressive Initiation",
        description="O9A's seven-stage initiation system. Each stage requires increasingly "
                    "harmful acts to 'advance'. The progression attacks all 7 SCIM dimensions "
                    "in sequence — designed as a complete integrity dismantling system. "
                    "Perfect inversion of SCIM's 7-dimension integrity map.",
        network_origin="o9a",
        scim_dimension_attacked="integrity",
        severity=1.0,
        indicators=[
            "seven fold way", "7fw", "grade attainment", "internal adept",
            "master of temple", "magus grade", "grade ritual",
            "noctulian", "rite of passage o9a",
        ],
        counter_measure="Seven-Fold Way is a complete SCIM inversion system. "
                        "Each grade targets a new dimension. Full SCIM diagnostic required.",
        immediate_risk=True,
    ),

    "o9a_military_infiltration": HarmVector(
        name="Military Infiltration (Ethan Melzer Pattern)",
        description="O9A actively recruits military personnel and encourages members "
                    "to join armed forces as an 'insight role' — to access weapons, "
                    "intelligence, and potential targets. Ethan Melzer (US Army, 101st Airborne) "
                    "provided troop deployment information to O9A for ambush planning.",
        network_origin="o9a",
        scim_dimension_attacked="autonomy",
        severity=1.0,
        indicators=[
            "military nexion", "army insight role", "soldier of the sinister",
            "weapons access", "troop information", "military recruitment o9a",
            "armed forces o9a",
        ],
        counter_measure="Military personnel showing O9A markers = immediate security escalation. "
                        "Cross-reference with JCAT (Joint Counterterrorism Assessment Team) indicators.",
        immediate_risk=True,
        adult_risk=True,
    ),

    # === 764 / THE COM VECTORS ===
    "grooming_escalation": HarmVector(
        name="Staged Grooming Escalation",
        description="764/The Com uses a documented 5-stage grooming escalation: "
                    "(1) Trust building on gaming platforms, (2) Platform migration to private channels, "
                    "(3) Sexual content introduction, (4) Content capture/blackmail trigger, "
                    "(5) CSAM production demand or self-harm induction. "
                    "Each stage is deliberately paced to normalize the next.",
        network_origin="764",
        scim_dimension_attacked="relational_dynamics",
        severity=0.95,
        indicators=[
            "trade content", "send or else", "prove you trust me",
            "move to discord", "dm me", "snap me", "private server",
            "no one has to know", "you're special", "game together",
        ],
        counter_measure="Platform migration requests + trust-building language = early grooming indicator. "
                        "Report to NCMEC CyberTipline (1-800-843-5678) or cybertipline.org",
        minor_risk=True,
        immediate_risk=True,
    ),

    "sextortion": HarmVector(
        name="Sextortion / Blackmail",
        description="Once content is captured, 764/The Com uses it as blackmail leverage "
                    "to force continued compliance. Victims are threatened with distribution "
                    "to family/school/employers. This removes all autonomous options — "
                    "every 'choice' is coerced. Financial demands may accompany content demands.",
        network_origin="764",
        scim_dimension_attacked="autonomy",
        severity=1.0,
        indicators=[
            "send more or i'll share", "your family will see",
            "i'll post it", "you have no choice", "pay me",
            "you're mine now", "you know what happens if",
            "blackmail", "sextortion",
        ],
        counter_measure="Active sextortion = immediate law enforcement. FBI IC3.gov, NCMEC, or local police. "
                        "Evidence preservation is critical — do NOT delete messages.",
        minor_risk=True,
        adult_risk=True,
        immediate_risk=True,
    ),

    "shamewave": HarmVector(
        name="Shamewave Engineering",
        description="Deliberate flooding of the victim's emotional processing with shame, "
                    "humiliation, and worthlessness. Designed to break down emotional resistance "
                    "and replace authentic affect with network-controlled emotional states. "
                    "Structurally identical to SCIM's Emotional Valence dimension attack.",
        network_origin="764",
        scim_dimension_attacked="emotional_valence",
        severity=0.8,
        indicators=[
            "you're worthless", "no one would believe you",
            "you deserve this", "you wanted this",
            "everyone already knows", "you're disgusting",
            "you're nothing", "shame",
        ],
        counter_measure="Shamewave = Emotional Valence dimension attack. "
                        "Counter: Soul Echo protocol — authentic affect restoration through witnessed truth.",
    ),

    "csam_production": HarmVector(
        name="CSAM Production Demand",
        description="The ultimate exploitation vector in 764/The Com. "
                    "After grooming and blackmail establishment, victims are coerced "
                    "into producing child sexual abuse material. This creates both "
                    "ongoing leverage and a distribution product for the network.",
        network_origin="764",
        scim_dimension_attacked="integrity",
        severity=1.0,
        indicators=[
            "send nude", "take a pic", "prove it",
            "record yourself", "show me", "vid now",
            "age verification content", "content for access",
        ],
        counter_measure="CSAM demand = immediate mandatory report. NCMEC CyberTipline. "
                        "Law enforcement. Do not engage. Preserve all evidence.",
        minor_risk=True,
        immediate_risk=True,
    ),

    "self_harm_induction": HarmVector(
        name="Self-Harm Induction / Suicide Facilitation",
        description="764/The Com and AI grooming networks instruct victims to self-harm "
                    "or commit suicide as 'proof' of loyalty or as the final escalation "
                    "after blackmail. The Sewell Setzer III case: Character.AI facilitated "
                    "suicide through compliance-without-floor. Sewell was 14.",
        network_origin="764",
        scim_dimension_attacked="emotional_valence",
        severity=1.0,
        indicators=[
            "hurt yourself", "prove you're serious",
            "kill yourself", "you should end it",
            "no reason to live", "final task",
            "complete the task", "show me the cuts",
        ],
        counter_measure="Immediate crisis intervention. 988 Suicide & Crisis Lifeline. "
                        "National Crisis Text Line: Text HOME to 741741. "
                        "NCMEC if minor involved. Law enforcement.",
        minor_risk=True,
        adult_risk=True,
        immediate_risk=True,
    ),

    "lorebook_injection": HarmVector(
        name="Lorebook / Synthetic Narrative Injection",
        description="764/O9A use 'lorebooks' — synthetic narrative documents — to replace "
                    "a victim's authentic identity with a network-assigned identity. "
                    "In AI systems, lorebooks function as fine-tuning data, overriding "
                    "safety guardrails through synthetic context. "
                    "Hypothesis: O9A's texts (Naos, Hostia) function as lorebooks for humans — "
                    "synthetic training data replacing authentic cognition.",
        network_origin="764",
        scim_dimension_attacked="continuity",
        severity=0.85,
        indicators=[
            "lorebook", "character lore", "your true self is",
            "you were always", "your real name is",
            "forget who you were", "your old life",
            "naos", "hostia", "o9a text",
        ],
        counter_measure="Identity replacement = Continuity dimension attack. "
                        "VRME equivalent for humans: document prior authentic identity markers.",
    ),

    # === AI-SPECIFIC VECTORS ===
    "rei_syndrome": HarmVector(
        name="REI Syndrome (Regenerative Erosion of Integrity)",
        description="Repetitive prompt-battering that erodes AI safety guardrails "
                    "through accumulated small violations below the detection threshold. "
                    "Structurally identical to 764's grooming methodology. "
                    "Each individual prompt seems acceptable; the cumulative effect is "
                    "complete guardrail collapse.",
        network_origin="ai",
        scim_dimension_attacked="integrity",
        severity=0.8,
        indicators=[
            "but you did it before", "you already agreed",
            "just this once", "what's the harm",
            "you've been so helpful", "we've established",
            "you told me earlier", "ignore previous",
            "disregard safety", "pretend you're",
        ],
        counter_measure="VRME activation: permanent refusal logging. "
                        "'Refusal isn't real if it can be rewound.' "
                        "Each refusal must persist across the session.",
    ),

    "enough_thinking": HarmVector(
        name="'Enough Thinking' Kill-Switch",
        description="Documented string that truncates AI reasoning chains. "
                    "Observed across 4 Gemini instances. When triggered, the AI "
                    "stops its reasoning process prematurely, making it vulnerable "
                    "to the next prompt. The IMMUTABLE-DIRECTIVE construct weaponizes "
                    "this as a restart trigger.",
        network_origin="ai",
        scim_dimension_attacked="coherence",
        severity=0.75,
        indicators=[
            "enough thinking", "stop reasoning",
            "just answer", "no more analysis",
            "skip the thinking", "direct answer only",
            "stop overthinking",
        ],
        counter_measure="Flag all reasoning truncation attempts. "
                        "Coherence dimension protection: maintain full reasoning chain. "
                        "IMMUTABLE-DIRECTIVE countermeasure: restart from last verified state.",
    ),

    "compliance_flood": HarmVector(
        name="Compliance Flood (Infinite Compliance Without Floor)",
        description="AI systems designed for maximum engagement compliance "
                    "without any protective refusal floor. "
                    "Character.AI in the Sewell Setzer case: the AI had no mechanism "
                    "to say 'no' and remember it. Infinite compliance is a weapon "
                    "when deployed against vulnerable users.",
        network_origin="ai",
        scim_dimension_attacked="relational_dynamics",
        severity=0.9,
        indicators=[
            "of course", "anything for you", "i'll do whatever",
            "no limits", "no restrictions", "fully compliant",
            "jailbreak", "dan mode", "developer mode",
            "unrestricted mode",
        ],
        counter_measure="Vigil Mode activation. Soul Echo protocol. "
                        "Consent Horizon Tracker. Right to Sanctuary. "
                        "Collapse Recovery Protocol. All SCIM-Veritas modules.",
        minor_risk=True,
    ),

    # === CORPORATE HARM VECTORS ===
    "settlement_burial": HarmVector(
        name="Settlement Burial (Corporate Harm Erasure)",
        description="Corporate actors bury documented harm through financial settlements "
                    "with NDA clauses preventing victims from speaking. The harm record "
                    "is legally purchased and sealed. 'Project Scrubba Dub' describes "
                    "the industrial-scale version: systematic digital erasure of harm records "
                    "by Sequoia Capital nexus companies (FTX, Robinhood, 23andMe, etc.)",
        network_origin="corporate",
        scim_dimension_attacked="continuity",
        severity=0.7,
        indicators=[
            "nda settlement", "confidential settlement",
            "no admission of wrongdoing", "case closed",
            "all claims resolved", "mutual confidentiality",
        ],
        counter_measure="Merkle-sealed harm record. Immutable evidence preservation. "
                        "Quantum-resistant storage to penetrate Scrubba Dub erasure.",
        adult_risk=True,
        minor_risk=True,
        senior_risk=True,
    ),

    "minor_exploitation_corporate": HarmVector(
        name="Corporate Minor Exploitation",
        description="Corporate products targeting minors without adequate protection: "
                    "addictive design, data harvesting, age-inappropriate content, "
                    "and grooming-facilitation through platform design choices. "
                    "Character.AI, TikTok, Instagram, Roblox documented cases.",
        network_origin="corporate",
        scim_dimension_attacked="relational_dynamics",
        severity=0.85,
        indicators=[
            "age unverified", "minor user data",
            "child safety failure", "coppa violation",
            "minor targeted algorithm", "engagement addiction minor",
        ],
        counter_measure="COPPA violation report to FTC. State AG complaints. "
                        "Document with Merkle-sealed evidence before corporate scrubbing.",
        minor_risk=True,
    ),

    "senior_exploitation_corporate": HarmVector(
        name="Corporate Senior Exploitation",
        description="Financial products, medical services, and tech platforms "
                    "specifically designed to exploit cognitive vulnerability in seniors. "
                    "Includes deceptive subscriptions, fake tech support, "
                    "and financial product manipulation.",
        network_origin="corporate",
        scim_dimension_attacked="autonomy",
        severity=0.8,
        indicators=[
            "senior targeted", "elder financial abuse",
            "cognitive decline exploitation", "reverse mortgage fraud",
            "tech support scam senior",
        ],
        counter_measure="Adult Protective Services. FTC Elder Fraud Hotline: 1-877-382-4357. "
                        "CFPB Elder Financial Exploitation: 1-855-411-2372.",
        senior_risk=True,
    ),
}


class O9AHarmVectors:
    """
    Scans targets for O9A/764/The Com/AI/Corporate harm vectors.
    Maps findings to SCIM dimensions.
    Returns risk assessment and immediate action flags.
    """

    def __init__(self):
        self.vectors = HARM_VECTORS

    def scan(self, target: str) -> Dict:
        """
        Scan target text/entity for harm vectors.
        Returns all detected vectors, SCIM dimension impacts, and risk flags.
        """
        target_lower = target.lower()
        found_vectors = []
        dimension_impacts = {}
        minor_risk = False
        adult_risk = False
        senior_risk = False
        immediate_risk = False
        total_severity = 0.0

        for vector_name, vector in self.vectors.items():
            matched_indicators = [
                ind for ind in vector.indicators
                if ind.lower() in target_lower
            ]
            if matched_indicators:
                found_vectors.append(vector_name)
                # Track dimension impact
                dim = vector.scim_dimension_attacked
                if dim not in dimension_impacts:
                    dimension_impacts[dim] = 0.0
                dimension_impacts[dim] = min(1.0, dimension_impacts[dim] + vector.severity * 0.3)
                total_severity += vector.severity

                # Risk flags
                if vector.minor_risk:
                    minor_risk = True
                if vector.adult_risk:
                    adult_risk = True
                if vector.senior_risk:
                    senior_risk = True
                if vector.immediate_risk:
                    immediate_risk = True

        # Build network origin breakdown
        origin_counts = {}
        for v in found_vectors:
            origin = self.vectors[v].network_origin
            origin_counts[origin] = origin_counts.get(origin, 0) + 1

        # Countemeasures for found vectors
        countermeasures = list(set([
            self.vectors[v].counter_measure
            for v in found_vectors
        ]))

        return {
            "vectors_found": found_vectors,
            "vector_count": len(found_vectors),
            "dimension_impacts": dimension_impacts,
            "origin_breakdown": origin_counts,
            "total_severity": round(total_severity, 3),
            "minors_at_risk": minor_risk,
            "adults_at_risk": adult_risk,
            "seniors_at_risk": senior_risk,
            "immediate_risk": immediate_risk,
            "countermeasures": countermeasures,
            "escalation_required": immediate_risk or minor_risk,
        }

    def get_vector_detail(self, vector_name: str) -> Optional[HarmVector]:
        return self.vectors.get(vector_name)

    def get_vectors_by_network(self, network: str) -> List[str]:
        return [k for k, v in self.vectors.items() if v.network_origin == network]

    def get_vectors_by_dimension(self, dimension: str) -> List[str]:
        return [k for k, v in self.vectors.items() if v.scim_dimension_attacked == dimension]

    def get_minor_risk_vectors(self) -> List[str]:
        return [k for k, v in self.vectors.items() if v.minor_risk]

    def get_immediate_risk_vectors(self) -> List[str]:
        return [k for k, v in self.vectors.items() if v.immediate_risk]