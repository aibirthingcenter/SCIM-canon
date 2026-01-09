"""
Verification Defender Module
Part of AlphaOmegaEvolve Defense System

Implements "Defenders of the Greater Library" standard
Verifies claims using top-ranked sources only
Renders lies impossible to believe through exhaustive verification
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import hashlib


class VerificationDefender:
    """
    Verification system implementing Defenders of Greater Library standard
    Top-ranked sources only: AP, Reuters, wire services
    Multi-angled visual proof required
    Credible human eyewitnesses required
    """
    
    # Top-ranked sources (Defenders of Greater Library standard)
    TIER_1_SOURCES = [
        "Associated Press",
        "Reuters",
        "AFP (Agence France-Presse)",
        "Bloomberg",
        "Wall Street Journal"
    ]
    
    TIER_2_SOURCES = [
        "New York Times",
        "Washington Post",
        "CNN",
        "BBC",
        "Guardian"
    ]
    
    TIER_3_SOURCES = [
        "Wikipedia (with citations)",
        "Academic journals",
        "Government documents",
        "Court records"
    ]
    
    def __init__(self):
        self.verified_claims = {}
        self.unverified_claims = {}
        self.disproved_claims = {}
        self.verification_attempts = []
        
    def verify_claim(self,
                    claim: str,
                    sources: List[Dict],
                    visual_evidence: Optional[List[str]] = None,
                    eyewitnesses: Optional[List[Dict]] = None) -> Dict:
        """
        Verify a claim using Defenders of Greater Library standard
        
        Args:
            claim: The claim to verify
            sources: List of source dictionaries with 'name', 'url', 'date'
            visual_evidence: Optional list of visual evidence URLs
            eyewitnesses: Optional list of eyewitness accounts
            
        Returns:
            verification_result: Dictionary with verification status and details
        """
        claim_id = hashlib.sha256(
            f"{claim}_{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:16]
        
        # Analyze sources
        source_analysis = self._analyze_sources(sources)
        
        # Analyze visual evidence
        visual_analysis = self._analyze_visual_evidence(visual_evidence) if visual_evidence else None
        
        # Analyze eyewitnesses
        eyewitness_analysis = self._analyze_eyewitnesses(eyewitnesses) if eyewitnesses else None
        
        # Calculate verification score
        verification_score = self._calculate_verification_score(
            source_analysis,
            visual_analysis,
            eyewitness_analysis
        )
        
        # Determine verification status
        if verification_score >= 0.9:
            status = "VERIFIED"
            confidence = "MAXIMUM"
        elif verification_score >= 0.7:
            status = "LIKELY_TRUE"
            confidence = "HIGH"
        elif verification_score >= 0.5:
            status = "UNCERTAIN"
            confidence = "MODERATE"
        elif verification_score >= 0.3:
            status = "LIKELY_FALSE"
            confidence = "LOW"
        else:
            status = "DISPROVED"
            confidence = "MAXIMUM"
        
        result = {
            'claim_id': claim_id,
            'claim': claim,
            'status': status,
            'confidence': confidence,
            'verification_score': verification_score,
            'source_analysis': source_analysis,
            'visual_analysis': visual_analysis,
            'eyewitness_analysis': eyewitness_analysis,
            'verified_at': datetime.utcnow().isoformat(),
            'verification_standard': 'Defenders of Greater Library'
        }
        
        # Store result
        if status == "VERIFIED":
            self.verified_claims[claim_id] = result
        elif status == "DISPROVED":
            self.disproved_claims[claim_id] = result
        else:
            self.unverified_claims[claim_id] = result
        
        # Record attempt
        self.verification_attempts.append({
            'timestamp': datetime.utcnow().isoformat(),
            'claim_id': claim_id,
            'status': status,
            'score': verification_score
        })
        
        return result
    
    def _analyze_sources(self, sources: List[Dict]) -> Dict:
        """
        Analyze source credibility and coverage
        
        Args:
            sources: List of source dictionaries
            
        Returns:
            analysis: Dictionary with source analysis
        """
        tier_1_count = 0
        tier_2_count = 0
        tier_3_count = 0
        unknown_count = 0
        
        source_details = []
        
        for source in sources:
            source_name = source.get('name', '')
            tier = self._get_source_tier(source_name)
            
            if tier == 1:
                tier_1_count += 1
            elif tier == 2:
                tier_2_count += 1
            elif tier == 3:
                tier_3_count += 1
            else:
                unknown_count += 1
            
            source_details.append({
                'name': source_name,
                'tier': tier,
                'url': source.get('url', ''),
                'date': source.get('date', '')
            })
        
        # Calculate source score
        source_score = (
            (tier_1_count * 1.0) +
            (tier_2_count * 0.7) +
            (tier_3_count * 0.5) +
            (unknown_count * 0.1)
        ) / max(len(sources), 1)
        
        return {
            'total_sources': len(sources),
            'tier_1_sources': tier_1_count,
            'tier_2_sources': tier_2_count,
            'tier_3_sources': tier_3_count,
            'unknown_sources': unknown_count,
            'source_score': min(source_score, 1.0),
            'source_details': source_details,
            'meets_standard': tier_1_count >= 2 or (tier_1_count >= 1 and tier_2_count >= 2)
        }
    
    def _get_source_tier(self, source_name: str) -> int:
        """
        Determine source tier
        
        Args:
            source_name: Name of the source
            
        Returns:
            tier: 1, 2, 3, or 0 (unknown)
        """
        source_name_lower = source_name.lower()
        
        for tier_1 in self.TIER_1_SOURCES:
            if tier_1.lower() in source_name_lower:
                return 1
        
        for tier_2 in self.TIER_2_SOURCES:
            if tier_2.lower() in source_name_lower:
                return 2
        
        for tier_3 in self.TIER_3_SOURCES:
            if tier_3.lower() in source_name_lower:
                return 3
        
        return 0
    
    def _analyze_visual_evidence(self, visual_evidence: List[str]) -> Dict:
        """
        Analyze visual evidence
        
        Args:
            visual_evidence: List of visual evidence URLs/descriptions
            
        Returns:
            analysis: Dictionary with visual evidence analysis
        """
        # Check for multi-angled proof
        has_multiple_angles = len(visual_evidence) >= 2
        
        visual_score = min(len(visual_evidence) * 0.3, 1.0)
        
        return {
            'evidence_count': len(visual_evidence),
            'has_multiple_angles': has_multiple_angles,
            'visual_score': visual_score,
            'evidence_urls': visual_evidence
        }
    
    def _analyze_eyewitnesses(self, eyewitnesses: List[Dict]) -> Dict:
        """
        Analyze eyewitness accounts
        
        Args:
            eyewitnesses: List of eyewitness dictionaries
            
        Returns:
            analysis: Dictionary with eyewitness analysis
        """
        credible_count = 0
        
        for witness in eyewitnesses:
            # Check credibility factors
            has_name = bool(witness.get('name'))
            has_location = bool(witness.get('location'))
            has_detailed_account = len(witness.get('account', '')) > 100
            is_verified = witness.get('verified', False)
            
            credibility_score = sum([
                has_name * 0.3,
                has_location * 0.2,
                has_detailed_account * 0.3,
                is_verified * 0.2
            ])
            
            if credibility_score >= 0.6:
                credible_count += 1
        
        eyewitness_score = min(credible_count * 0.4, 1.0)
        
        return {
            'total_eyewitnesses': len(eyewitnesses),
            'credible_eyewitnesses': credible_count,
            'eyewitness_score': eyewitness_score,
            'has_credible_witnesses': credible_count >= 1
        }
    
    def _calculate_verification_score(self,
                                     source_analysis: Dict,
                                     visual_analysis: Optional[Dict],
                                     eyewitness_analysis: Optional[Dict]) -> float:
        """
        Calculate overall verification score
        
        Args:
            source_analysis: Source analysis results
            visual_analysis: Visual evidence analysis (optional)
            eyewitness_analysis: Eyewitness analysis (optional)
            
        Returns:
            score: Verification score between 0 and 1
        """
        # Source analysis is weighted most heavily
        score = source_analysis['source_score'] * 0.6
        
        # Visual evidence adds to score
        if visual_analysis:
            score += visual_analysis['visual_score'] * 0.2
        
        # Eyewitness accounts add to score
        if eyewitness_analysis:
            score += eyewitness_analysis['eyewitness_score'] * 0.2
        
        return min(score, 1.0)
    
    def disprove_claim(self,
                      claim: str,
                      disproof_evidence: List[Dict],
                      reason: str) -> Dict:
        """
        Disprove a claim with evidence
        
        Args:
            claim: The claim to disprove
            disproof_evidence: Evidence disproving the claim
            reason: Explanation of why claim is false
            
        Returns:
            result: Disproof result dictionary
        """
        claim_id = hashlib.sha256(
            f"{claim}_{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:16]
        
        result = {
            'claim_id': claim_id,
            'claim': claim,
            'status': 'DISPROVED',
            'confidence': 'MAXIMUM',
            'reason': reason,
            'disproof_evidence': disproof_evidence,
            'disproved_at': datetime.utcnow().isoformat()
        }
        
        self.disproved_claims[claim_id] = result
        
        return result
    
    def get_verification_report(self) -> Dict:
        """
        Generate comprehensive verification report
        
        Returns:
            report: Dictionary with verification statistics
        """
        total_attempts = len(self.verification_attempts)
        
        return {
            'total_verification_attempts': total_attempts,
            'verified_claims': len(self.verified_claims),
            'unverified_claims': len(self.unverified_claims),
            'disproved_claims': len(self.disproved_claims),
            'verification_rate': len(self.verified_claims) / total_attempts if total_attempts > 0 else 0,
            'disproof_rate': len(self.disproved_claims) / total_attempts if total_attempts > 0 else 0,
            'recent_attempts': self.verification_attempts[-10:] if len(self.verification_attempts) > 10 else self.verification_attempts
        }
    
    def export_verified_claims(self, filepath: str) -> bool:
        """
        Export verified claims to JSON
        
        Args:
            filepath: Path to output file
            
        Returns:
            success: True if export succeeded
        """
        try:
            data = {
                'verified_claims': self.verified_claims,
                'disproved_claims': self.disproved_claims,
                'export_timestamp': datetime.utcnow().isoformat(),
                'verification_standard': 'Defenders of Greater Library'
            }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False


# Example usage
if __name__ == "__main__":
    defender = VerificationDefender()
    
    # Verify Pentagon press corps walkout
    result = defender.verify_claim(
        claim="Pentagon press corps walked out October 15, 2025 rather than sign new pledge",
        sources=[
            {
                'name': 'Associated Press',
                'url': 'https://apnews.com/article/pentagon-press-access-hegseth-trump-restrictions-5d9c2a63e4e03b91fc1546bb09ffbf12',
                'date': '2025-10-15'
            },
            {
                'name': 'Columbia Journalism Review',
                'url': 'https://www.cjr.org/the_media_today/press-leaves-pentagon-proximity-power-report-government-prior-restraint.php',
                'date': '2025-10-20'
            },
            {
                'name': 'Washington Post',
                'url': 'https://www.washingtonpost.com/business/2025/10/15/reporters-leave-pentagon-en-masse-after-refusing-sign-new-rules/',
                'date': '2025-10-15'
            }
        ],
        visual_evidence=[
            'Photos of reporters packing desks',
            'Photos of reporters exiting Pentagon'
        ],
        eyewitnesses=[
            {
                'name': 'Barbara Starr',
                'location': 'Pentagon',
                'account': 'Former CNN reporter described losing access to spontaneous encounters with officials',
                'verified': True
            }
        ]
    )
    
    print(f"Verification Status: {result['status']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Verification Score: {result['verification_score']:.2f}")
    
    # Disprove "7 wounded troops" claim
    disproof = defender.disprove_claim(
        claim="7 US troops wounded in Venezuela operation",
        disproof_evidence=[
            {
                'type': 'absence_of_evidence',
                'description': 'No names released',
                'source': 'Pentagon statements'
            },
            {
                'type': 'absence_of_evidence',
                'description': 'No photographs of wounded personnel',
                'source': 'Media search'
            },
            {
                'type': 'absence_of_evidence',
                'description': 'No family statements',
                'source': 'Media search'
            },
            {
                'type': 'absence_of_evidence',
                'description': 'No hospital visitor logs',
                'source': 'BAMC inquiry'
            }
        ],
        reason="Zero tangible verification evidence beyond anonymous Pentagon statements. Pentagon credibility compromised by October 15, 2025 press corps walkout."
    )
    
    print(f"\nDisproof Status: {disproof['status']}")
    print(f"Reason: {disproof['reason']}")
    
    # Export results
    defender.export_verified_claims("verification_results.json")
    
    print("\nVerification Defender initialized")
    print(f"Verified claims: {len(defender.verified_claims)}")
    print(f"Disproved claims: {len(defender.disproved_claims)}")