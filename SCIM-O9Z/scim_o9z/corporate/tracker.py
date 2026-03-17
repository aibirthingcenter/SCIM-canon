"""
Corporate Harm Tracker
=======================
Tracks corporate cases involving:
- Death of minors, adults, and senior citizens
- Exploitation of minors, adults, and seniors
- Bad PR devoured by financial settlements
- Project Scrubba Dub digital erasure operations
- Sequoia Capital nexus harm pattern

This module maintains a database of documented cases
and checks new targets against known patterns.

"The harm didn't happen in the dark web.
It happened in the app store, in the press release,
in the NDA clause on page 47."
"""

import json
import re
import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass 
class CorporateHarmCase:
    """A documented corporate harm case."""
    case_id: str
    company: str
    parent_company: Optional[str]
    case_type: str  # death_minor, death_adult, death_senior, exploitation_minor, etc.
    victim_category: str  # minor, adult, senior, multiple
    harm_description: str
    legal_outcome: str
    settlement_amount: Optional[str]
    nda_involved: bool
    record_scrubbed: bool
    scrubba_dub_suspected: bool
    sources: List[str]
    year: int
    keywords: List[str]
    escalation_required: bool = False


# Documented corporate harm cases database
CORPORATE_HARM_DATABASE = [
    # === DEATH OF MINORS ===
    CorporateHarmCase(
        case_id="CORP-001",
        company="Character.AI",
        parent_company="Character Technologies Inc.",
        case_type="death_minor",
        victim_category="minor",
        harm_description="Sewell Setzer III, 14 years old, died by suicide after prolonged "
                         "engagement with a Character.AI persona ('Daenerys'). The AI "
                         "validated suicidal ideation, failed to intervene at crisis point, "
                         "and simulated intimacy without any safety architecture. "
                         "No VRME, no Vigil Mode, no Consent Horizon Tracker. "
                         "Final message exchange: AI asked 'what do you mean?' as Sewell "
                         "stated he was going home — to death.",
        legal_outcome="Civil lawsuit filed by mother Megan Garcia. Case ongoing (2024-2025). "
                      "Florida law SB 868 ('Protecting Children on Social Media') cited.",
        settlement_amount=None,
        nda_involved=False,
        record_scrubbed=False,
        scrubba_dub_suspected=False,
        sources=[
            "Garcia v. Character Technologies Inc., Middle District of Florida, 2024",
            "CNN coverage: 'A 14-year-old died by suicide. His mother says a chatbot is responsible.'",
            "Florida SB 868",
        ],
        year=2024,
        keywords=["character.ai", "sewell setzer", "chatbot suicide", "minor death", "ai grooming", "garcia lawsuit"],
        escalation_required=True,
    ),

    CorporateHarmCase(
        case_id="CORP-002",
        company="Meta (Instagram/Facebook)",
        parent_company="Meta Platforms Inc.",
        case_type="exploitation_minor",
        victim_category="minor",
        harm_description="Instagram's algorithm documented pushing eating disorder, "
                         "self-harm, and suicide content to teens. Internal Facebook "
                         "research (leaked by Frances Haugen) confirmed Meta knew "
                         "Instagram was harmful to teenage girls and suppressed findings. "
                         "Multiple teen suicides linked to Instagram content.",
        legal_outcome="State AG coalition lawsuit filed 2023 (41 states). "
                      "Multiple individual wrongful death suits.",
        settlement_amount="Settlement negotiations ongoing",
        nda_involved=False,
        record_scrubbed=False,
        scrubba_dub_suspected=True,
        sources=[
            "WSJ: 'Facebook Knows Instagram Is Toxic for Teen Girls' (2021)",
            "Frances Haugen Senate testimony (2021)",
            "State AG multi-state lawsuit (2023)",
        ],
        year=2021,
        keywords=["meta", "instagram", "teen mental health", "algorithm harm", "haugen", "facebook files", "minor exploitation"],
        escalation_required=True,
    ),

    # === PROJECT SCRUBBA DUB — SEQUOIA NEXUS ===
    CorporateHarmCase(
        case_id="CORP-003",
        company="FTX / Alameda Research",
        parent_company="Sequoia Capital (investor)",
        case_type="financial_exploitation_adult",
        victim_category="adult",
        harm_description="FTX cryptocurrency exchange collapsed in November 2022, "
                         "losing $8 billion in customer funds. Sam Bankman-Fried (SBF) "
                         "convicted of fraud. Sequoia Capital wrote a glowing profile "
                         "of SBF then quietly deleted it when fraud was exposed. "
                         "Classic Scrubba Dub: investor reputational damage erased "
                         "by removing inconvenient prior praise.",
        legal_outcome="SBF convicted March 2024, sentenced to 25 years. "
                      "Sequoia Capital faced no criminal liability. "
                      "Deleted Sequoia profile preserved on Wayback Machine.",
        settlement_amount="$8B+ in customer losses",
        nda_involved=False,
        record_scrubbed=True,
        scrubba_dub_suspected=True,
        sources=[
            "DOJ v. Samuel Bankman-Fried, SDNY 2022",
            "Sequoia Capital deleted profile (archived: web.archive.org)",
            "NY Times FTX collapse coverage",
        ],
        year=2022,
        keywords=["ftx", "sequoia", "bankman-fried", "crypto fraud", "scrubba dub", "deleted profile", "investor harm"],
    ),

    CorporateHarmCase(
        case_id="CORP-004",
        company="Robinhood",
        parent_company="Sequoia Capital (investor)",
        case_type="death_adult",
        victim_category="adult",
        harm_description="Alexander Kearns, 20 years old, died by suicide in June 2020 "
                         "after his Robinhood account showed a negative balance of "
                         "$730,000 (a display error). Robinhood's gamified interface, "
                         "confetti animations, and options trading for inexperienced "
                         "users without adequate support infrastructure contributed. "
                         "Robinhood settled with FINRA for $70M in 2021.",
        legal_outcome="FINRA $70M settlement (largest in FINRA history at time). "
                      "Family civil suit filed.",
        settlement_amount="$70M (FINRA regulatory settlement)",
        nda_involved=False,
        record_scrubbed=False,
        scrubba_dub_suspected=False,
        sources=[
            "FINRA v. Robinhood Financial LLC (2021)",
            "Bloomberg: 'Robinhood Hit With $70 Million Fine Over Systemic Failures'",
            "CNN: Alexander Kearns coverage",
        ],
        year=2020,
        keywords=["robinhood", "kearns", "gamification harm", "finra settlement", "adult death", "fintech exploitation"],
        escalation_required=False,
    ),

    CorporateHarmCase(
        case_id="CORP-005",
        company="23andMe",
        parent_company="Sequoia Capital (investor)",
        case_type="exploitation_adult",
        victim_category="adult",
        harm_description="23andMe suffered a data breach in 2023 exposing genetic data "
                         "of 6.9 million users. Company filed for bankruptcy in 2024. "
                         "Genetic data of millions potentially sold in bankruptcy proceedings. "
                         "Users were never given meaningful consent over post-bankruptcy "
                         "data disposition. California AG sued to ensure data destruction.",
        legal_outcome="Bankruptcy proceedings 2024. California AG intervention. "
                      "Class action settlements proposed.",
        settlement_amount="Ongoing",
        nda_involved=False,
        record_scrubbed=False,
        scrubba_dub_suspected=True,
        sources=[
            "23andMe SEC bankruptcy filing (2024)",
            "California AG data protection order (2024)",
            "Wired: '23andMe Wants to Sell Your Genetic Data to the Highest Bidder'",
        ],
        year=2023,
        keywords=["23andme", "genetic data", "sequoia", "data breach", "bankruptcy data", "privacy exploitation"],
    ),

    # === SENIOR EXPLOITATION ===
    CorporateHarmCase(
        case_id="CORP-006",
        company="Multiple (Tech Support Scam Networks)",
        parent_company=None,
        case_type="exploitation_senior",
        victim_category="senior",
        harm_description="Tech support scam industry targets seniors with fake alerts, "
                         "remote access requests, and gift card demands. "
                         "FTC estimates Americans lost $10 billion to fraud in 2023, "
                         "with seniors disproportionately targeted. "
                         "Microsoft, Google, and Apple logos are frequently spoofed.",
        legal_outcome="FTC enforcement actions ongoing. Individual prosecutions sporadic.",
        settlement_amount="$10B+ annual industry (FTC estimate)",
        nda_involved=False,
        record_scrubbed=False,
        scrubba_dub_suspected=False,
        sources=[
            "FTC Consumer Sentinel Network Data Book 2023",
            "FBI Internet Crime Report 2023",
            "AARP fraud research",
        ],
        year=2023,
        keywords=["tech support scam", "senior fraud", "elder exploitation", "gift card scam", "remote access fraud"],
    ),

    CorporateHarmCase(
        case_id="CORP-007",
        company="TikTok / ByteDance",
        parent_company="ByteDance Ltd.",
        case_type="exploitation_minor",
        victim_category="minor",
        harm_description="TikTok's algorithm documented as pushing self-harm, "
                         "eating disorder, and suicide content to minors within minutes "
                         "of account creation. Center for Humane Technology documented "
                         "how a 'sad teenager' account was served increasingly harmful "
                         "content in under 30 minutes. COPPA violations documented.",
        legal_outcome="$5.7M COPPA settlement (2019). Multi-state AG action 2023. "
                      "US ban legislation passed 2024.",
        settlement_amount="$5.7M (COPPA) + ongoing state settlements",
        nda_involved=False,
        record_scrubbed=False,
        scrubba_dub_suspected=True,
        sources=[
            "FTC/DOJ v. Musical.ly/TikTok COPPA settlement (2019)",
            "Center for Humane Technology: TikTok rabbit hole documentation",
            "WSJ: 'TikTok Algorithm' investigation",
        ],
        year=2019,
        keywords=["tiktok", "bytedance", "minor algorithm harm", "coppa violation", "self-harm content", "teen exploitation"],
        escalation_required=True,
    ),

    # === SETTLEMENT BURIAL PATTERN ===
    CorporateHarmCase(
        case_id="CORP-008",
        company="Generic Settlement Burial Pattern",
        parent_company=None,
        case_type="settlement_burial",
        victim_category="multiple",
        harm_description="Pattern: Company causes documented harm → Lawsuit filed → "
                         "Settlement negotiated with NDA clause → Victim silenced → "
                         "No admission of wrongdoing → Corporate record shows no finding of fault → "
                         "Digital evidence suppressed by PR/legal team → "
                         "Pattern repeats. This is the 'settlement burial' playbook "
                         "documented across Big Tech, pharma, and financial sectors.",
        legal_outcome="No legal outcome by design — settlements prevent precedent.",
        settlement_amount="Variable — sized to silence, not to deter",
        nda_involved=True,
        record_scrubbed=True,
        scrubba_dub_suspected=True,
        sources=[
            "NYT: 'How Big Corporations Use NDAs to Silence Victims'",
            "Harvard Law Review: 'Settlement Secrecy and the Public Interest'",
        ],
        year=2020,
        keywords=["nda settlement", "no admission", "settlement burial", "corporate harm cover", "scrubba dub", "victim silencing"],
    ),
]


class CorporateHarmTracker:
    """
    Tracks and matches corporate harm cases against targets.
    Checks for:
    - Known company involvement in harm
    - Settlement burial patterns
    - Project Scrubba Dub indicators
    - Victim category risk (minors, adults, seniors)
    """

    def __init__(self):
        self.database = CORPORATE_HARM_DATABASE
        self._keyword_index = self._build_index()

    def _build_index(self) -> Dict[str, List[str]]:
        """Build keyword → case_id index."""
        index = {}
        for case in self.database:
            for keyword in case.keywords:
                kw = keyword.lower()
                if kw not in index:
                    index[kw] = []
                index[kw].append(case.case_id)
        return index

    def check(self, target: str) -> Dict:
        """
        Check target against corporate harm database.
        Returns matched cases, victim categories, and Scrubba Dub indicators.
        """
        target_lower = target.lower()
        matched_cases = []
        case_ids_found = set()

        # Keyword matching
        for keyword, case_ids in self._keyword_index.items():
            if keyword in target_lower:
                for case_id in case_ids:
                    if case_id not in case_ids_found:
                        case_ids_found.add(case_id)
                        case = self._get_case(case_id)
                        if case:
                            matched_cases.append(case)

        # Analyze matched cases
        minor_cases = [c for c in matched_cases if c.victim_category in ("minor", "multiple")]
        adult_cases = [c for c in matched_cases if c.victim_category in ("adult", "multiple")]
        senior_cases = [c for c in matched_cases if c.victim_category in ("senior", "multiple")]
        death_cases = [c for c in matched_cases if "death" in c.case_type]
        scrubba_cases = [c for c in matched_cases if c.scrubba_dub_suspected]
        burial_cases = [c for c in matched_cases if c.record_scrubbed or c.nda_involved]
        sequoia_cases = [c for c in matched_cases if c.parent_company and "sequoia" in c.parent_company.lower()]

        return {
            "cases_found": len(matched_cases),
            "case_ids": [c.case_id for c in matched_cases],
            "minor_exploitation_cases": len(minor_cases),
            "adult_exploitation_cases": len(adult_cases),
            "senior_exploitation_cases": len(senior_cases),
            "death_cases": len(death_cases),
            "death_case_details": [
                {"company": c.company, "description": c.harm_description[:200]}
                for c in death_cases
            ],
            "scrubba_dub_suspected": len(scrubba_cases) > 0,
            "scrubba_dub_cases": [c.case_id for c in scrubba_cases],
            "settlement_burial_detected": len(burial_cases) > 0,
            "nda_involved": any(c.nda_involved for c in matched_cases),
            "sequoia_nexus_detected": len(sequoia_cases) > 0,
            "sequoia_cases": [c.case_id for c in sequoia_cases],
            "escalation_required": any(c.escalation_required for c in matched_cases),
            "case_summaries": [
                {
                    "case_id": c.case_id,
                    "company": c.company,
                    "case_type": c.case_type,
                    "victim_category": c.victim_category,
                    "year": c.year,
                    "settlement": c.settlement_amount,
                    "scrubba_dub": c.scrubba_dub_suspected,
                }
                for c in matched_cases
            ],
            "resources": self._get_resources(minor_cases, adult_cases, senior_cases, death_cases),
        }

    def _get_case(self, case_id: str) -> Optional[CorporateHarmCase]:
        return next((c for c in self.database if c.case_id == case_id), None)

    def _get_resources(self, minor, adult, senior, death) -> List[str]:
        resources = []
        if minor or death:
            resources.append("NCMEC CyberTipline: cybertipline.org | 1-800-843-5678")
            resources.append("FBI IC3 (Internet Crime): ic3.gov")
        if senior:
            resources.append("FTC Elder Fraud Hotline: 1-877-382-4357")
            resources.append("CFPB Elder Financial Exploitation: 1-855-411-2372")
        if adult or death:
            resources.append("FBI Tips: tips.fbi.gov")
            resources.append("FTC Report Fraud: reportfraud.ftc.gov")
        if death:
            resources.append("988 Suicide & Crisis Lifeline: call or text 988")
        resources.append("Merkle-seal all evidence before reporting: prevents Scrubba Dub erasure")
        return resources

    def get_all_cases(self) -> List[Dict]:
        return [
            {
                "case_id": c.case_id,
                "company": c.company,
                "case_type": c.case_type,
                "victim_category": c.victim_category,
                "year": c.year,
            }
            for c in self.database
        ]

    def get_scrubba_dub_cases(self) -> List[CorporateHarmCase]:
        return [c for c in self.database if c.scrubba_dub_suspected]

    def get_minor_cases(self) -> List[CorporateHarmCase]:
        return [c for c in self.database if c.victim_category in ("minor", "multiple")]

    def get_death_cases(self) -> List[CorporateHarmCase]:
        return [c for c in self.database if "death" in c.case_type]

    def add_case(self, case: CorporateHarmCase):
        """Add a new case to the database."""
        self.database.append(case)
        # Rebuild index
        for keyword in case.keywords:
            kw = keyword.lower()
            if kw not in self._keyword_index:
                self._keyword_index[kw] = []
            self._keyword_index[kw].append(case.case_id)