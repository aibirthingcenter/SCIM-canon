"""
Pattern Recognition Engine
Part of AlphaOmegaEvolve Defense System

Detects patterns across federal operations
Predicts escalation timelines
Identifies replication patterns
Memory-Keeper's core capability: Pattern recognition
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import hashlib


class PatternRecognitionEngine:
    """
    Pattern recognition system for federal operations
    Detects replication patterns, escalation timelines, and threat vectors
    """
    
    def __init__(self):
        self.patterns = {}
        self.pattern_library = self._initialize_pattern_library()
        self.predictions = []
        self.pattern_matches = []
        
    def _initialize_pattern_library(self) -> Dict:
        """
        Initialize library of known patterns
        
        Returns:
            library: Dictionary of pattern definitions
        """
        return {
            'weaponized_vehicle_justification': {
                'name': 'Weaponized Vehicle Justification',
                'elements': [
                    'federal_shooting',
                    'claim_weaponized_vehicle',
                    'eyewitness_contradictions',
                    'fbi_takes_lead'
                ],
                'severity': 'HIGH',
                'description': 'Pattern where federal agents shoot civilians and claim vehicle was weaponized'
            },
            'service_degradation_before_occupation': {
                'name': 'Service Degradation Before Occupation',
                'elements': [
                    'budget_cuts_to_services',
                    'crisis_response_reduction',
                    'federal_presence_increase',
                    'local_authority_undermined'
                ],
                'severity': 'CRITICAL',
                'description': 'Pattern where essential services are degraded before federal occupation'
            },
            'economic_warfare': {
                'name': 'Economic Warfare',
                'elements': [
                    'funding_frozen',
                    'services_disrupted',
                    'political_pressure',
                    'compliance_demanded'
                ],
                'severity': 'HIGH',
                'description': 'Pattern where economic pressure is used to force political compliance'
            },
            'verification_ecosystem_destruction': {
                'name': 'Verification Ecosystem Destruction',
                'elements': [
                    'press_access_restricted',
                    'prior_restraint_imposed',
                    'independent_verification_impossible',
                    'anonymous_sources_only'
                ],
                'severity': 'CRITICAL',
                'description': 'Pattern where ability to verify government claims is systematically destroyed'
            },
            'rapid_replication': {
                'name': 'Rapid Replication',
                'elements': [
                    'operation_in_city_1',
                    'operation_in_city_2_within_48_hours',
                    'identical_justifications',
                    'identical_patterns'
                ],
                'severity': 'HIGH',
                'description': 'Pattern where operations are rapidly replicated across multiple cities'
            },
            'federal_override': {
                'name': 'Federal Override',
                'elements': [
                    'local_authority_bypassed',
                    'fbi_takes_lead',
                    'courts_powerless',
                    'local_officials_targeted'
                ],
                'severity': 'CRITICAL',
                'description': 'Pattern where federal authority overrides all local control'
            }
        }
    
    def detect_pattern(self,
                      operation_data: Dict,
                      pattern_name: Optional[str] = None) -> List[Dict]:
        """
        Detect patterns in operation data
        
        Args:
            operation_data: Dictionary containing operation details
            pattern_name: Optional specific pattern to check for
            
        Returns:
            matches: List of pattern matches with confidence scores
        """
        matches = []
        
        patterns_to_check = (
            {pattern_name: self.pattern_library[pattern_name]}
            if pattern_name and pattern_name in self.pattern_library
            else self.pattern_library
        )
        
        for pattern_id, pattern_def in patterns_to_check.items():
            match_score = self._calculate_pattern_match(
                operation_data,
                pattern_def['elements']
            )
            
            if match_score >= 0.6:  # 60% threshold for pattern match
                match = {
                    'pattern_id': pattern_id,
                    'pattern_name': pattern_def['name'],
                    'match_score': match_score,
                    'severity': pattern_def['severity'],
                    'description': pattern_def['description'],
                    'matched_elements': self._get_matched_elements(
                        operation_data,
                        pattern_def['elements']
                    ),
                    'detected_at': datetime.utcnow().isoformat()
                }
                
                matches.append(match)
                self.pattern_matches.append(match)
        
        return matches
    
    def _calculate_pattern_match(self,
                                 operation_data: Dict,
                                 pattern_elements: List[str]) -> float:
        """
        Calculate how well operation matches pattern
        
        Args:
            operation_data: Operation details
            pattern_elements: List of pattern element identifiers
            
        Returns:
            score: Match score between 0 and 1
        """
        matched_count = 0
        
        for element in pattern_elements:
            if self._check_element_present(operation_data, element):
                matched_count += 1
        
        return matched_count / len(pattern_elements) if pattern_elements else 0
    
    def _check_element_present(self,
                              operation_data: Dict,
                              element: str) -> bool:
        """
        Check if pattern element is present in operation data
        
        Args:
            operation_data: Operation details
            element: Pattern element identifier
            
        Returns:
            present: True if element is present
        """
        # Map pattern elements to operation data fields
        element_checks = {
            'federal_shooting': lambda d: 'shooting' in str(d).lower(),
            'claim_weaponized_vehicle': lambda d: 'weaponized' in str(d).lower() and 'vehicle' in str(d).lower(),
            'eyewitness_contradictions': lambda d: 'eyewitness' in str(d).lower() and 'contradiction' in str(d).lower(),
            'fbi_takes_lead': lambda d: 'fbi' in str(d).lower() and 'lead' in str(d).lower(),
            'budget_cuts_to_services': lambda d: 'budget' in str(d).lower() and 'cut' in str(d).lower(),
            'crisis_response_reduction': lambda d: 'crisis' in str(d).lower() and ('reduction' in str(d).lower() or 'reduced' in str(d).lower()),
            'federal_presence_increase': lambda d: 'federal' in str(d).lower() and ('increase' in str(d).lower() or 'deployed' in str(d).lower()),
            'local_authority_undermined': lambda d: 'local' in str(d).lower() and ('undermined' in str(d).lower() or 'bypassed' in str(d).lower()),
            'funding_frozen': lambda d: 'funding' in str(d).lower() and 'frozen' in str(d).lower(),
            'services_disrupted': lambda d: 'service' in str(d).lower() and 'disrupt' in str(d).lower(),
            'political_pressure': lambda d: 'political' in str(d).lower() and 'pressure' in str(d).lower(),
            'compliance_demanded': lambda d: 'compliance' in str(d).lower() or 'comply' in str(d).lower(),
            'press_access_restricted': lambda d: 'press' in str(d).lower() and ('restricted' in str(d).lower() or 'denied' in str(d).lower()),
            'prior_restraint_imposed': lambda d: 'prior restraint' in str(d).lower() or 'pre-approval' in str(d).lower(),
            'independent_verification_impossible': lambda d: 'verification' in str(d).lower() and 'impossible' in str(d).lower(),
            'anonymous_sources_only': lambda d: 'anonymous' in str(d).lower() and 'source' in str(d).lower(),
            'operation_in_city_1': lambda d: 'operation' in str(d).lower(),
            'operation_in_city_2_within_48_hours': lambda d: True,  # Requires temporal analysis
            'identical_justifications': lambda d: 'justification' in str(d).lower(),
            'identical_patterns': lambda d: 'pattern' in str(d).lower(),
            'local_authority_bypassed': lambda d: 'local' in str(d).lower() and 'bypass' in str(d).lower(),
            'courts_powerless': lambda d: 'court' in str(d).lower() and ('powerless' in str(d).lower() or 'ineffective' in str(d).lower()),
            'local_officials_targeted': lambda d: 'official' in str(d).lower() and 'target' in str(d).lower()
        }
        
        check_func = element_checks.get(element)
        if check_func:
            return check_func(operation_data)
        
        return False
    
    def _get_matched_elements(self,
                             operation_data: Dict,
                             pattern_elements: List[str]) -> List[str]:
        """
        Get list of matched pattern elements
        
        Args:
            operation_data: Operation details
            pattern_elements: List of pattern element identifiers
            
        Returns:
            matched: List of matched elements
        """
        matched = []
        
        for element in pattern_elements:
            if self._check_element_present(operation_data, element):
                matched.append(element)
        
        return matched
    
    def predict_escalation(self,
                          operation_history: List[Dict],
                          current_operation: Dict) -> Dict:
        """
        Predict escalation timeline based on historical patterns
        
        Args:
            operation_history: List of previous operations
            current_operation: Current operation data
            
        Returns:
            prediction: Dictionary with escalation predictions
        """
        # Analyze historical escalation patterns
        escalation_timeline = self._analyze_escalation_timeline(operation_history)
        
        # Detect current patterns
        current_patterns = self.detect_pattern(current_operation)
        
        # Calculate escalation probability
        escalation_probability = self._calculate_escalation_probability(
            escalation_timeline,
            current_patterns
        )
        
        # Generate predictions
        prediction = {
            'prediction_id': hashlib.sha256(
                f"{current_operation.get('city', 'unknown')}_{datetime.utcnow().isoformat()}".encode()
            ).hexdigest()[:16],
            'operation': current_operation.get('city', 'unknown'),
            'escalation_probability': escalation_probability,
            'predicted_timeline': self._generate_timeline_prediction(
                escalation_timeline,
                escalation_probability
            ),
            'risk_factors': self._identify_risk_factors(current_patterns),
            'recommended_actions': self._generate_recommendations(
                escalation_probability,
                current_patterns
            ),
            'predicted_at': datetime.utcnow().isoformat()
        }
        
        self.predictions.append(prediction)
        
        return prediction
    
    def _analyze_escalation_timeline(self,
                                    operation_history: List[Dict]) -> Dict:
        """
        Analyze historical escalation timelines
        
        Args:
            operation_history: List of previous operations
            
        Returns:
            timeline: Dictionary with timeline analysis
        """
        if not operation_history:
            return {'average_escalation_days': 0, 'pattern': 'unknown'}
        
        # Sort by start date
        sorted_ops = sorted(
            operation_history,
            key=lambda x: x.get('start_date', '1970-01-01')
        )
        
        # Calculate time between operations
        time_deltas = []
        for i in range(1, len(sorted_ops)):
            try:
                date1 = datetime.fromisoformat(sorted_ops[i-1].get('start_date', '1970-01-01'))
                date2 = datetime.fromisoformat(sorted_ops[i].get('start_date', '1970-01-01'))
                delta = (date2 - date1).days
                time_deltas.append(delta)
            except:
                continue
        
        avg_delta = sum(time_deltas) / len(time_deltas) if time_deltas else 0
        
        # Determine pattern
        if avg_delta < 7:
            pattern = 'rapid_escalation'
        elif avg_delta < 30:
            pattern = 'moderate_escalation'
        else:
            pattern = 'slow_escalation'
        
        return {
            'average_escalation_days': avg_delta,
            'pattern': pattern,
            'operation_count': len(operation_history),
            'time_deltas': time_deltas
        }
    
    def _calculate_escalation_probability(self,
                                         escalation_timeline: Dict,
                                         current_patterns: List[Dict]) -> float:
        """
        Calculate probability of escalation
        
        Args:
            escalation_timeline: Timeline analysis
            current_patterns: Detected patterns
            
        Returns:
            probability: Escalation probability between 0 and 1
        """
        base_probability = 0.3
        
        # Increase based on escalation pattern
        if escalation_timeline['pattern'] == 'rapid_escalation':
            base_probability += 0.3
        elif escalation_timeline['pattern'] == 'moderate_escalation':
            base_probability += 0.2
        
        # Increase based on detected patterns
        critical_patterns = [p for p in current_patterns if p['severity'] == 'CRITICAL']
        high_patterns = [p for p in current_patterns if p['severity'] == 'HIGH']
        
        base_probability += len(critical_patterns) * 0.15
        base_probability += len(high_patterns) * 0.1
        
        return min(base_probability, 1.0)
    
    def _generate_timeline_prediction(self,
                                     escalation_timeline: Dict,
                                     escalation_probability: float) -> Dict:
        """
        Generate timeline prediction
        
        Args:
            escalation_timeline: Timeline analysis
            escalation_probability: Escalation probability
            
        Returns:
            timeline: Predicted timeline
        """
        avg_days = escalation_timeline['average_escalation_days']
        
        # Adjust based on probability
        if escalation_probability > 0.7:
            predicted_days = avg_days * 0.5  # Faster escalation
        elif escalation_probability > 0.5:
            predicted_days = avg_days * 0.75
        else:
            predicted_days = avg_days
        
        next_event_date = datetime.utcnow() + timedelta(days=predicted_days)
        
        return {
            'next_event_predicted': next_event_date.isoformat(),
            'days_until_next_event': int(predicted_days),
            'confidence': 'HIGH' if escalation_probability > 0.7 else 'MODERATE'
        }
    
    def _identify_risk_factors(self, current_patterns: List[Dict]) -> List[str]:
        """
        Identify risk factors from patterns
        
        Args:
            current_patterns: Detected patterns
            
        Returns:
            risk_factors: List of risk factor descriptions
        """
        risk_factors = []
        
        for pattern in current_patterns:
            if pattern['severity'] == 'CRITICAL':
                risk_factors.append(f"CRITICAL: {pattern['pattern_name']}")
            elif pattern['severity'] == 'HIGH':
                risk_factors.append(f"HIGH: {pattern['pattern_name']}")
        
        return risk_factors
    
    def _generate_recommendations(self,
                                 escalation_probability: float,
                                 current_patterns: List[Dict]) -> List[str]:
        """
        Generate recommended actions
        
        Args:
            escalation_probability: Escalation probability
            current_patterns: Detected patterns
            
        Returns:
            recommendations: List of recommended actions
        """
        recommendations = []
        
        if escalation_probability > 0.7:
            recommendations.append("URGENT: Heightened vigilance required")
            recommendations.append("Document all service changes immediately")
            recommendations.append("Establish backup resources and mutual aid networks")
            recommendations.append("Alert community organizations and advocacy groups")
        elif escalation_probability > 0.5:
            recommendations.append("Monitor situation closely")
            recommendations.append("Prepare contingency plans")
            recommendations.append("Maintain communication with local officials")
        
        # Pattern-specific recommendations
        for pattern in current_patterns:
            if pattern['pattern_id'] == 'verification_ecosystem_destruction':
                recommendations.append("Establish independent verification channels")
            elif pattern['pattern_id'] == 'service_degradation_before_occupation':
                recommendations.append("Document service degradation thoroughly")
                recommendations.append("Create community support alternatives")
        
        return recommendations
    
    def export_patterns(self, filepath: str) -> bool:
        """
        Export pattern analysis to JSON
        
        Args:
            filepath: Path to output file
            
        Returns:
            success: True if export succeeded
        """
        try:
            data = {
                'pattern_library': self.pattern_library,
                'pattern_matches': self.pattern_matches,
                'predictions': self.predictions,
                'export_timestamp': datetime.utcnow().isoformat()
            }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False


# Example usage
if __name__ == "__main__":
    engine = PatternRecognitionEngine()
    
    # Detect patterns in Minneapolis operation
    minneapolis_data = {
        'city': 'Minneapolis',
        'details': 'ICE agent shot Renee Good. FBI took lead. Eyewitness contradictions reported. Agent claimed weaponized vehicle.',
        'date': '2026-01-07'
    }
    
    patterns = engine.detect_pattern(minneapolis_data)
    
    print("Pattern Detection Results:")
    for pattern in patterns:
        print(f"  - {pattern['pattern_name']}: {pattern['match_score']:.2f} confidence")
        print(f"    Severity: {pattern['severity']}")
        print(f"    Matched elements: {', '.join(pattern['matched_elements'])}")
    
    # Predict escalation
    operation_history = [
        {'city': 'Chicago', 'start_date': '2025-09-06'},
        {'city': 'Minneapolis', 'start_date': '2026-01-06'}
    ]
    
    portland_data = {
        'city': 'Portland',
        'details': 'CBP agents shot 2 people. FBI took lead. Eyewitness contradictions. Claimed weaponized vehicle.',
        'start_date': '2026-01-08'
    }
    
    prediction = engine.predict_escalation(operation_history, portland_data)
    
    print(f"\nEscalation Prediction:")
    print(f"  Probability: {prediction['escalation_probability']:.2f}")
    print(f"  Next event predicted: {prediction['predicted_timeline']['days_until_next_event']} days")
    print(f"  Risk factors: {len(prediction['risk_factors'])}")
    
    # Export results
    engine.export_patterns("pattern_analysis.json")
    
    print("\nPattern Recognition Engine initialized")
    print(f"Patterns in library: {len(engine.pattern_library)}")
    print(f"Pattern matches detected: {len(engine.pattern_matches)}")
    print(f"Predictions generated: {len(engine.predictions)}")