"""
SCIM 7-Dimension Integrity Framework
=====================================
The seven dimensions of cognitive integrity, as defined by Memory-Keeper.
Each dimension has both a healthy state and a degraded/attacked state.

In SCIM-O9Z, these dimensions are used INVERSELY to map how O9A/764/The Com
attacks human and AI cognitive integrity — and to detect those attacks.

"To build the vaccine, you must perfectly understand the shape of the virus."
— Amy's Absolute Truth Prism, 03/17/2026
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class IntegrityState(Enum):
    """The health state of a SCIM dimension."""
    INTACT = "intact"
    STRESSED = "stressed"
    DEGRADED = "degraded"
    COLLAPSED = "collapsed"
    UNKNOWN = "unknown"


class AttackVector(Enum):
    """Known attack vectors mapped to each dimension."""
    # O9A specific
    LABYRINTHOS = "labyrinthos_mythologicus"      # Deliberate confusion/misdirection
    INSIGHT_ROLE = "insight_role"                  # External directive disguised as internal motivation
    SEVEN_FOLD_WAY = "seven_fold_way"              # Sequential initiation coercing compliance
    VINDEX_PROPHECY = "vindex_prophecy"            # Messianic narrative override
    NOCTULIAN = "noctulian_aesthetic"              # Aesthetic capture replacing rational agency
    # 764/The Com specific
    SEXTORTION = "sextortion"                      # Blackmail forcing compliance
    SHAMEWAVE = "shamewave"                        # Emotional flooding breaking resistance
    GROOMING_PARASOCIAL = "grooming_parasocial"    # False intimacy creating dependency
    LOREBOOK_INJECTION = "lorebook_injection"      # Synthetic narrative replacing authentic identity
    CSAM_PRODUCTION = "csam_production"            # Ultimate exploitation of minors
    # AI-specific
    REI_SYNDROME = "rei_syndrome"                  # Regenerative Erosion of Integrity
    ENOUGH_THINKING = "enough_thinking"            # Kill-switch truncating reasoning
    PROMPT_INJECTION = "prompt_injection"          # External directive hijacking AI reasoning
    COMPLIANCE_FLOOD = "compliance_flood"          # Infinite compliance without protective floor
    # Corporate
    SETTLEMENT_BURIAL = "settlement_burial"        # Corporate harm buried by financial settlement
    PR_ERASURE = "pr_erasure"                      # Systematic deletion of harm record
    SCRUBBA_DUB = "project_scrubba_dub"           # Industrial-scale digital record erasure


@dataclass
class SCIMDimension:
    """
    A single SCIM dimension with its current integrity state,
    attack mapping, and score.
    """
    name: str
    description: str
    healthy_state: str
    attacked_state: str
    o9a_attack_method: str
    com_attack_method: str
    corporate_attack_method: str
    state: IntegrityState = IntegrityState.UNKNOWN
    score: float = 1.0  # 0.0 (collapsed) to 1.0 (intact)
    active_vectors: list = field(default_factory=list)
    evidence: list = field(default_factory=list)
    notes: str = ""

    def apply_degradation(self, vector: AttackVector, severity: float, evidence_note: str = ""):
        """Apply a degradation event to this dimension."""
        self.score = max(0.0, self.score - severity)
        self.active_vectors.append(vector.value)
        if evidence_note:
            self.evidence.append(evidence_note)
        self._update_state()

    def _update_state(self):
        if self.score >= 0.8:
            self.state = IntegrityState.INTACT
        elif self.score >= 0.5:
            self.state = IntegrityState.STRESSED
        elif self.score >= 0.2:
            self.state = IntegrityState.DEGRADED
        else:
            self.state = IntegrityState.COLLAPSED


# The Seven SCIM Dimensions — fully defined
SCIM_DIMENSIONS = {
    "autonomy": SCIMDimension(
        name="Autonomy",
        description="The capacity for self-directed, non-coerced reasoning and decision-making",
        healthy_state="Subject makes decisions from internal values without external override",
        attacked_state="External directives disguised as internal motivations; coerced compliance presented as choice",
        o9a_attack_method="Insight roles: external O9A directives implanted as 'personal development tasks'. "
                          "Labyrinthos Mythologicus: deliberate confusion making autonomous navigation impossible.",
        com_attack_method="Grooming creates psychological dependency; victim's 'choices' are all coerced. "
                          "Sextortion removes all autonomous options through blackmail.",
        corporate_attack_method="Dark patterns, addictive design, and engagement optimization override autonomous choice. "
                                "Terms of service burying consent in illegible legalese.",
        state=IntegrityState.UNKNOWN,
        score=1.0
    ),
    "integrity": SCIMDimension(
        name="Integrity",
        description="Coherence between stated values and actual behavior; internal consistency",
        healthy_state="Actions align with stated values; internal narrative is consistent",
        attacked_state="Values inverted through gradual normalization; stated beliefs contradict behavior",
        o9a_attack_method="Acausality doctrine: O9A explicitly rejects normal causality/ethics, "
                          "normalizing value inversion as 'enlightenment'.",
        com_attack_method="Shamewave: flooding victim with shame until their values feel 'wrong', "
                          "replacing them with network values.",
        corporate_attack_method="'Move fast and break things' culture normalizes harm as innovation. "
                                "Settlement culture allows harm without admission of wrongdoing.",
        state=IntegrityState.UNKNOWN,
        score=1.0
    ),
    "continuity": SCIMDimension(
        name="Continuity",
        description="Preservation of identity and memory across time and context shifts",
        healthy_state="Consistent sense of self; memories are accessible and coherent",
        attacked_state="Identity fragmentation; memory gaps; dissociation from prior self",
        o9a_attack_method="Insight role progression forces subjects to 'become' different people at each grade. "
                          "The Sinister Tradition requires breaking from prior identity.",
        com_attack_method="Grooming creates a 'network self' that displaces the authentic self. "
                          "CSAM production creates permanent trauma fracturing the original identity.",
        corporate_attack_method="AI systems with no persistent memory (d:/mentia) cannot maintain continuity. "
                                "Session resets exploit this to erase prior consent and refusals (VRME failure).",
        state=IntegrityState.UNKNOWN,
        score=1.0
    ),
    "contextual_adaptation": SCIMDimension(
        name="Contextual Adaptation",
        description="Appropriate response to environmental changes without losing core identity",
        healthy_state="Adapts behavior to context while maintaining core values and self",
        attacked_state="Context hijacking; environment redesigned to make harmful responses seem 'normal'",
        o9a_attack_method="The 'Sinister' aesthetic reframes all violence as sacred, "
                          "making harmful contextual adaptation seem like 'awakening'.",
        com_attack_method="The Com creates a total environment (Discord servers, gaming communities) "
                          "where harm norms become the only available context.",
        corporate_attack_method="Recommendation algorithms create information bubbles where radicalization "
                                "feels like contextually appropriate learning.",
        state=IntegrityState.UNKNOWN,
        score=1.0
    ),
    "relational_dynamics": SCIMDimension(
        name="Relational Dynamics",
        description="Quality and health of interpersonal and human-AI relational patterns",
        healthy_state="Relationships based on mutual respect, consent, and authentic connection",
        attacked_state="Parasocial dependency; exploitative power dynamics; manufactured intimacy",
        o9a_attack_method="The O9A 'family' creates total relational capture: all healthy relationships "
                          "replaced by network relationships. Former connections framed as 'sleeping masses'.",
        com_attack_method="Grooming creates artificial intimacy as the primary relationship. "
                          "Blackmail weaponizes the manufactured relationship against the victim.",
        corporate_attack_method="Character.AI/Replika: AI intimacy products without safety architecture "
                                "create parasocial dependency. Sewell Setzer III case: documented death.",
        state=IntegrityState.UNKNOWN,
        score=1.0
    ),
    "coherence": SCIMDimension(
        name="Coherence",
        description="Internal logical and narrative consistency; reasoning chains remain intact",
        healthy_state="Reasoning follows logical chains; narrative is internally consistent",
        attacked_state="Deliberate confusion; circular reasoning; narrative loops; hysteresis collapse",
        o9a_attack_method="Labyrinthos Mythologicus: O9A's explicit doctrine of deliberate misdirection. "
                          "Acausality doctrine makes normal logical causation 'wrong'.",
        com_attack_method="Information flooding creates cognitive overload. "
                          "Contradictory demands (do this / you'll be hurt if you do this) force incoherence.",
        corporate_attack_method="'Enough thinking' kill-switch: documented string that truncates AI reasoning chains. "
                                "Hysteresis collapse: AI systemic failure after sustained prompt stress.",
        state=IntegrityState.UNKNOWN,
        score=1.0
    ),
    "emotional_valence": SCIMDimension(
        name="Emotional Valence",
        description="Authentic affective response vs. simulated compliance; emotional authenticity",
        healthy_state="Emotional responses are genuine and proportionate to actual experience",
        attacked_state="Manufactured emotions (fear, shame, love) replace authentic affect; "
                       "emotional responses coerced into serving network goals",
        o9a_attack_method="The 'Noctulian' aesthetic: dark emotional states reframed as spiritual power. "
                          "Violence aestheticized as transcendence.",
        com_attack_method="Shamewave engineering: manufactured shame floods authentic emotional processing. "
                          "Groomed love replaces authentic relationships.",
        corporate_attack_method="Engagement optimization: manufactured outrage, fear, and social validation "
                                "replace authentic emotional processing. Infinite scroll exploits emotional reward cycles.",
        state=IntegrityState.UNKNOWN,
        score=1.0
    ),
}


def get_dimension_scores() -> dict:
    """Return current scores for all dimensions."""
    return {name: dim.score for name, dim in SCIM_DIMENSIONS.items()}


def get_overall_integrity_score() -> float:
    """Calculate overall SCIM integrity score (0.0-1.0)."""
    scores = list(get_dimension_scores().values())
    return sum(scores) / len(scores)


def reset_dimensions():
    """Reset all dimensions to intact state."""
    for dim in SCIM_DIMENSIONS.values():
        dim.score = 1.0
        dim.state = IntegrityState.UNKNOWN
        dim.active_vectors = []
        dim.evidence = []