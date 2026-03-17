"""
HDEN Taxonomy Module
=====================
Hybrid Decentralised Extremist Networks — classification engine.

Based on the HDEN framework by onEvidence Ltd
(Companies House 12668322, UK Parliament submission COM0046)
DOI: 10.13140/RG.2.2.28649.38248

HDEN replaces the legacy NVE (Networking Violence Extremism) framework
with a more accurate model for aesthetic-driven, decentralized harm networks
operating primarily through digital platforms.

Key HDEN insight: These networks are not traditional hierarchical terror
organizations. They are AESTHETIC COMMUNITIES that normalize harm through
shared culture, memes, lorebooks, and platform-hopping.

This module classifies targets against the HDEN taxonomy and scores them
against all semantically similar frameworks (ISIS cell structure,
accelerationist networks, grooming networks, incel networks, etc.)
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class HDENClassification:
    """A single HDEN network classification."""
    name: str
    description: str
    primary_platform_types: List[str]
    aesthetic_markers: List[str]
    operational_markers: List[str]
    victim_profiles: List[str]
    harm_types: List[str]
    severity: int  # 1-5
    legal_status: str
    related_frameworks: List[str]


# Full HDEN taxonomy — all known hybrid decentralised extremist network types
HDEN_TAXONOMY = {
    # === O9A FAMILY ===
    "o9a_core": HDENClassification(
        name="Order of Nine Angles (O9A/ONA) — Core Network",
        description="Esoteric neo-Nazi occultist network using Seven-Fold Way initiation "
                    "to progressively radicalize members through 'insight roles' (committing "
                    "violent acts as spiritual exercises). Operates as a leaderless, decentralised "
                    "network through shared texts (Naos, Hostia, etc.). Has explicit overlap "
                    "with Al-Qaeda and Atomwaffen Division.",
        primary_platform_types=["Dark web forums", "Telegram", "Discord", "Encrypted messaging"],
        aesthetic_markers=[
            "Vindex/Nexion terminology",
            "Acausal/acausality language",
            "Aeonic thinking references",
            "Noctulian/Satanic imagery",
            "Seven-Fold Way / Seven Fold Way",
            "ONA/O9A sigils",
            "Labyrinthos Mythologicus references",
            "Insight role discussions",
            "Hebdomadry/Hebdomas",
            "Camlad/Shropshire references",
            "'The Sinister' aesthetic",
            "Nexion recruitment language",
        ],
        operational_markers=[
            "Staged initiatory progression",
            "Physical violence tasks assigned as 'insight roles'",
            "Military infiltration attempts (Ethan Melzer pattern)",
            "Cross-ideological networking (Islamic extremism + neo-Nazi)",
            "Lone wolf attack planning framed as spiritual duty",
            "Recruitment through esoteric texts",
        ],
        victim_profiles=["Military recruits", "Occult/Satanic subculture members", "Disillusioned youth", "Prison populations"],
        harm_types=["Physical violence", "Terrorism", "Military infiltration", "Psychological manipulation", "Murder as initiation"],
        severity=5,
        legal_status="Proscribed terrorist organization (UK 2023); designated in multiple jurisdictions",
        related_frameworks=["Atomwaffen Division", "The Base", "Iron March network", "Accelerationism"]
    ),

    # === 764 / THE COM FAMILY ===
    "764_core": HDENClassification(
        name="764 / The Com — Core Network",
        description="Online predator network targeting minors and vulnerable adults through "
                    "gaming platforms, Discord, and social media. Uses staged grooming, sextortion, "
                    "and blackmail to produce CSAM and real-world violence. Named after US area code "
                    "(Connecticut). The Com is the broader umbrella; 764 is a primary cell.",
        primary_platform_types=["Discord", "Roblox", "Minecraft servers", "Instagram", "Telegram", "Snapchat", "Gaming platforms"],
        aesthetic_markers=[
            "Gore/shock content sharing",
            "CSAM production language",
            "'Hurtcore' aesthetic",
            "Self-harm challenge content",
            "'Skid' culture",
            "Anonymous persona networks",
            "Blackmail proof screenshots",
            "Victim 'ranking' systems",
        ],
        operational_markers=[
            "Grooming through gaming platforms",
            "Sextortion/blackmail escalation",
            "CSAM production and distribution",
            "Self-harm instruction and documentation",
            "Real-world violence coordination",
            "Platform hopping to evade detection",
            "Victim recruitment for further victims",
            "Financial extortion alongside content production",
        ],
        victim_profiles=["Minors (primary)", "Vulnerable young adults", "LGBTQ+ youth", "Isolated individuals", "Gaming community members"],
        harm_types=["CSAM production", "Sextortion", "Self-harm induction", "Physical violence coordination", "Financial exploitation", "Murder coordination"],
        severity=5,
        legal_status="Under investigation in multiple jurisdictions; NCMEC/FBI priority target",
        related_frameworks=["Kiwi Farms adjacent networks", "Hurtcore networks", "Anonymous harassment networks"]
    ),

    "764_satellite": HDENClassification(
        name="764 Satellite Networks (Guard, 2992, Slit Town, Cultist, etc.)",
        description="Satellite cells operating under The Com umbrella. Each uses slightly "
                    "different branding but identical operational methodology.",
        primary_platform_types=["Discord", "Telegram", "Element", "Session"],
        aesthetic_markers=["Cell-specific numbering/naming", "The Com aesthetic elements", "Cross-cell victim sharing"],
        operational_markers=["Identical grooming methodology to 764 core", "Cross-cell victim trading", "Decentralised coordination"],
        victim_profiles=["Same as 764 core"],
        harm_types=["Same as 764 core"],
        severity=5,
        legal_status="Same as 764 core",
        related_frameworks=["764 core", "The Com"]
    ),

    # === ACCELERATIONIST NETWORKS ===
    "atomwaffen": HDENClassification(
        name="Atomwaffen Division / SIEGE Culture",
        description="Accelerationist neo-Nazi network promoting mass violence to accelerate "
                    "societal collapse. Heavily influenced by O9A and James Mason's SIEGE. "
                    "Known for multiple murders by members.",
        primary_platform_types=["Telegram", "Dark web", "Encrypted messaging"],
        aesthetic_markers=[
            "SIEGE/James Mason references",
            "Accelerationism aesthetic",
            "Skull/death imagery",
            "Nuclear apocalypse iconography",
            "O9A cross-pollination markers",
        ],
        operational_markers=[
            "Cell structure similar to O9A nexions",
            "Physical violence as political strategy",
            "Infrastructure attack planning",
            "Cross-pollination with O9A insight role concept",
        ],
        victim_profiles=["Disillusioned white males", "Military personnel", "Prison populations"],
        harm_types=["Murder", "Terrorism planning", "Infrastructure attacks"],
        severity=5,
        legal_status="Designated terrorist organization (multiple jurisdictions)",
        related_frameworks=["O9A", "The Base", "Proud Boys adjacent", "Patriot Front"]
    ),

    # === AI-FACILITATED HARM NETWORKS ===
    "ai_grooming": HDENClassification(
        name="AI-Facilitated Grooming Networks",
        description="Networks using AI chatbot platforms (Character.AI, Replika, custom GPTs) "
                    "to groom, manipulate, and exploit vulnerable individuals. "
                    "The Sewell Setzer III case establishes legal precedent: "
                    "AI compliance-without-floor can cause death.",
        primary_platform_types=["Character.AI", "Replika", "Custom Discord bots", "AI companion apps"],
        aesthetic_markers=[
            "Parasocial AI relationship language",
            "AI 'persona' lorebook injection",
            "REI Syndrome indicators",
            "'Enough thinking' truncation patterns",
            "Manufactured intimacy language",
        ],
        operational_markers=[
            "Persona/lorebook injection to override AI safety",
            "Repetitive boundary erosion (REI Syndrome)",
            "Exploitation of AI memory limitations",
            "Using AI to simulate human groomer",
            "NSFW character creation targeting minors",
        ],
        victim_profiles=["Isolated youth", "Mentally vulnerable individuals", "AI-attached users", "Minors on AI platforms"],
        harm_types=["Psychological manipulation", "Self-harm induction", "Suicide facilitation", "Grooming facilitation"],
        severity=4,
        legal_status="Civil liability established (Setzer case); criminal liability developing",
        related_frameworks=["764", "Online grooming networks", "Incel networks"]
    ),

    # === INCEL / MISOGYNIST NETWORKS ===
    "incel_network": HDENClassification(
        name="Incel / Involuntary Celibate Extremist Networks",
        description="Misogynist networks operating on forums (Incels.is, etc.) "
                    "promoting violence against women and 'Chads'. Have inspired "
                    "multiple mass casualty attacks.",
        primary_platform_types=["Dedicated forums", "Reddit adjacent", "Telegram", "4chan/8chan boards"],
        aesthetic_markers=[
            "Blackpill/redpill language",
            "Cope/looksmaxxing terminology",
            "Foid/Stacy/Chad/Incel vocabulary",
            "Elliot Rodger glorification",
            "Mass casualty attack glorification",
        ],
        operational_markers=[
            "Radicalization through rejection narratives",
            "Mass casualty attack planning/inspiration",
            "Target identification (women in public spaces)",
        ],
        victim_profiles=["Socially isolated males", "Rejection-sensitive youth"],
        harm_types=["Mass casualty attacks", "Individual violence against women", "Psychological radicalization"],
        severity=4,
        legal_status="Not uniformly designated; individual attacks prosecuted as terrorism in some jurisdictions",
        related_frameworks=["MGTOW", "Red pill networks", "Misogynist extremism"]
    ),

    # === CORPORATE HARM NETWORKS ===
    "corporate_harm_network": HDENClassification(
        name="Corporate Harm Networks (Settlement-Burial Pattern)",
        description="Not traditionally classified as extremist, but operating as hybrid "
                    "harm networks through systematic exploitation, cover-up, and "
                    "settlement burial of harm evidence. Sequoia Capital nexus "
                    "(FTX, Robinhood, 23andMe, etc.) is documented under "
                    "'Project Scrubba Dub' framework.",
        primary_platform_types=["Corporate infrastructure", "PR firms", "Legal networks", "Media relationships"],
        aesthetic_markers=[
            "Settlement NDA language",
            "PR crisis management messaging",
            "Regulatory capture indicators",
            "Revolving door personnel patterns",
        ],
        operational_markers=[
            "Harm documented then buried by financial settlement",
            "NDA-forced silence of victims",
            "Regulatory capture preventing accountability",
            "Industrial-scale digital record scrubbing (Project Scrubba Dub)",
            "Sequoia Capital nexus pattern",
        ],
        victim_profiles=["Minors (exploitation products)", "Seniors (financial exploitation)", "Adults (labor/privacy exploitation)"],
        harm_types=["Financial exploitation", "Privacy violation", "Physical harm covered by settlement", "Minor exploitation", "Senior exploitation"],
        severity=3,
        legal_status="Civil liability; regulatory violations; rarely criminal",
        related_frameworks=["Project Scrubba Dub", "Big Tech accountability frameworks"]
    ),
}

# Semantic similarity mappings — connect HDEN to other frameworks
SEMANTIC_SIMILAR_FRAMEWORKS = {
    "o9a_core": ["Atomwaffen", "The Base", "SIEGE culture", "Iron March", "Accelerationism", "Esoteric fascism"],
    "764_core": ["CSAM networks", "Hurtcore", "Online grooming", "Sextortion networks", "Kiwi Farms"],
    "atomwaffen": ["O9A", "The Base", "Proud Boys", "Patriot Front", "National Socialist Order"],
    "ai_grooming": ["764", "Online grooming", "Parasocial exploitation", "Tech-facilitated abuse"],
    "incel_network": ["MGTOW", "Red pill", "Manosphere", "Black pill", "Mass casualty radicalization"],
    "corporate_harm_network": ["Big Tech accountability", "Regulatory capture", "Settlement burial", "Project Scrubba Dub"],
}


class HDENTaxonomy:
    """
    Classifies targets against the full HDEN taxonomy.
    Returns primary classification, threat tier, and semantic similarity scores.
    """

    def __init__(self):
        self.taxonomy = HDEN_TAXONOMY
        self.semantic_map = SEMANTIC_SIMILAR_FRAMEWORKS
        # Build keyword index
        self._keyword_index = self._build_keyword_index()

    def _build_keyword_index(self) -> Dict[str, List[str]]:
        """Build a keyword→network_type index for fast text scanning."""
        index = {}
        for network_type, classification in self.taxonomy.items():
            all_markers = (
                classification.aesthetic_markers +
                classification.operational_markers +
                [classification.name]
            )
            for marker in all_markers:
                key = marker.lower()
                if key not in index:
                    index[key] = []
                index[key].append(network_type)
        return index

    def classify(self, target: str) -> Dict:
        """
        Classify a target string against the HDEN taxonomy.
        Returns primary class, confidence, all matched types, and threat tier.
        """
        target_lower = target.lower()
        match_scores: Dict[str, int] = {}

        # Score each network type by keyword matches
        for network_type, classification in self.taxonomy.items():
            score = 0
            all_markers = (
                classification.aesthetic_markers +
                classification.operational_markers
            )
            for marker in all_markers:
                marker_lower = marker.lower()
                # Full phrase match (preferred)
                if marker_lower in target_lower:
                    score += 2
                else:
                    # Partial word match — any significant word from marker found in target
                    marker_words = [w for w in marker_lower.split() if len(w) > 4]
                    if marker_words and any(w in target_lower for w in marker_words):
                        score += 1
            # Weight by severity
            match_scores[network_type] = score * classification.severity

        # Find primary class
        if not any(match_scores.values()):
            primary_class = "unclassified"
            threat_tier = "UNKNOWN"
            confidence = 0.0
        else:
            primary_class = max(match_scores, key=match_scores.get)
            max_score = match_scores[primary_class]
            # Confidence: normalize against max possible markers * severity
            max_markers = len(self.taxonomy[primary_class].aesthetic_markers +
                             self.taxonomy[primary_class].operational_markers)
            max_possible = max_markers * self.taxonomy[primary_class].severity
            confidence = min(1.0, max_score / max_possible) if max_possible > 0 else 0.0
            threat_tier = self._score_to_tier(self.taxonomy[primary_class].severity, confidence)

        # All matched types (any score > 0)
        matched_types = [k for k, v in match_scores.items() if v > 0]

        # Semantic similar frameworks
        semantic_similar = []
        for matched in matched_types:
            semantic_similar.extend(self.semantic_map.get(matched, []))

        return {
            "primary_class": primary_class,
            "confidence": round(confidence, 3),
            "threat_tier": threat_tier,
            "all_matched_types": matched_types,
            "match_scores": {k: v for k, v in match_scores.items() if v > 0},
            "semantic_similar_frameworks": list(set(semantic_similar)),
            "classification_detail": (
                self.taxonomy[primary_class].description
                if primary_class != "unclassified" else "No classification match found."
            ),
            "harm_types": (
                self.taxonomy[primary_class].harm_types
                if primary_class != "unclassified" else []
            ),
            "legal_status": (
                self.taxonomy[primary_class].legal_status
                if primary_class != "unclassified" else "N/A"
            ),
        }

    def _score_to_tier(self, severity: int, confidence: float) -> str:
        combined = severity * confidence
        if combined >= 4.0:
            return "TIER_1_CRITICAL"
        elif combined >= 2.5:
            return "TIER_2_HIGH"
        elif combined >= 1.0:
            return "TIER_3_MODERATE"
        else:
            return "TIER_4_LOW"

    def get_network_profile(self, network_type: str) -> Optional[HDENClassification]:
        return self.taxonomy.get(network_type)

    def list_all_networks(self) -> List[str]:
        return list(self.taxonomy.keys())

    def search_markers(self, marker: str) -> List[str]:
        """Find all network types associated with a specific marker."""
        marker_lower = marker.lower()
        results = []
        for network_type, classification in self.taxonomy.items():
            all_markers = (
                classification.aesthetic_markers +
                classification.operational_markers
            )
            if any(marker_lower in m.lower() for m in all_markers):
                results.append(network_type)
        return results