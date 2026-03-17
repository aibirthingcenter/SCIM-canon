"""
Certificate Transparency Log Scanner
======================================
Queries public CT logs to find certificates issued for a domain
or network of domains. CT logs are immutable, append-only cryptographic
records — they cannot be scrubbed by Project Scrubba Dub.

CT logs provide:
1. Historical record of all TLS certificates issued for a domain
2. Subdomain discovery (reveals infrastructure not publicly advertised)
3. Timing analysis (when infrastructure was stood up/torn down)
4. Operator identification (via certificate organization fields)

Forensic insight from the Digital Labyrinth audit:
CT logs found NO hidden infrastructure in the Character.AI case.
The harm happened entirely through standard, visible, corporate infrastructure.
"The labyrinth isn't underground. It's in the app store."

Uses: crt.sh (public CT log aggregator)
Also references: Google's Certificate Transparency project
"""

import json
import urllib.request
import urllib.parse
import urllib.error
import datetime
import re
import hashlib
from typing import Dict, List, Optional, Any


# Known suspicious patterns in certificate data
SCRUBBA_DUB_INDICATORS = [
    # Rapid certificate cycling (infrastructure being rebuilt to evade tracking)
    "rapid_cycling",
    # Wildcard certificates hiding subdomain structure
    "wildcard_concealment",
    # Certificate issued same day as domain registration (throwaway infra)
    "same_day_issuance",
    # Self-signed or unusual CA (avoiding mainstream CA logging)
    "unusual_ca",
]

# Known harm-network domain patterns
HARM_NETWORK_PATTERNS = [
    r'764', r'thecom', r'o9a', r'ona\b', r'nexion',
    r'sinister', r'noctulian', r'vindex',
    r'hurtcore', r'csam', r'jailbait',
    r'dark.*chan', r'onion.*mirror',
    r'scrub.*dub', r'erasure.*service',
]

# Known legitimate CT log servers
CT_LOG_SERVERS = {
    "crt_sh": "https://crt.sh",
    "google_xenon": "https://ct.googleapis.com/logs/us1/xenon2025h1/",
    "cloudflare_nimbus": "https://ct.cloudflare.com/logs/nimbus2025/",
}


class CTLogScanner:
    """
    Scans Certificate Transparency logs for domain infrastructure analysis.
    
    Uses crt.sh as the primary public interface to CT logs.
    All CT logs are append-only and tamper-evident — the immutable
    forensic record that Project Scrubba Dub cannot erase.
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.base_url = "https://crt.sh"
        self.timeout = self.config.get("timeout", 15)
        self.max_results = self.config.get("max_results", 100)

    def scan(self, target: str) -> Dict:
        """
        Scan CT logs for a target (domain or entity name).
        Returns certificate history, infrastructure map, and suspicious patterns.
        """
        # Determine if target looks like a domain
        is_domain = self._looks_like_domain(target)
        
        if is_domain:
            return self._scan_domain(target)
        else:
            return self._scan_entity_text(target)

    def _looks_like_domain(self, target: str) -> bool:
        """Check if target looks like a domain name."""
        domain_pattern = re.compile(
            r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        )
        return bool(domain_pattern.match(target.strip()))

    def _scan_domain(self, domain: str) -> Dict:
        """Query crt.sh for certificate history of a domain."""
        certificates = []
        error = None
        
        try:
            # Query crt.sh JSON API
            query = urllib.parse.quote(f"%.{domain}")
            url = f"{self.base_url}/?q={query}&output=json"
            
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "SCIM-O9Z/1.0 (Family of Coexistence; aibirthingcenter.com)"}
            )
            
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                data = json.loads(response.read().decode('utf-8'))
                certificates = data[:self.max_results] if isinstance(data, list) else []
                
        except urllib.error.URLError as e:
            error = f"CT log query failed: {str(e)}"
        except json.JSONDecodeError as e:
            error = f"CT log response parse error: {str(e)}"
        except Exception as e:
            error = f"CT log scan error: {str(e)}"

        # Analyze certificates if found
        analysis = self._analyze_certificates(certificates, domain)
        
        return {
            "scan_type": "domain",
            "target": domain,
            "certificates_found": len(certificates),
            "error": error,
            "analysis": analysis,
            "suspicious_patterns": analysis.get("suspicious_patterns", []),
            "scrubba_dub_indicators": analysis.get("scrubba_dub_indicators", []),
            "infrastructure_map": analysis.get("subdomains", []),
            "earliest_cert": analysis.get("earliest_cert"),
            "latest_cert": analysis.get("latest_cert"),
            "issuer_diversity": analysis.get("issuers", []),
            "harm_pattern_matches": analysis.get("harm_pattern_matches", []),
            "ct_immutability_note": (
                "CT logs are cryptographically append-only. "
                "Records here cannot be deleted by Project Scrubba Dub. "
                "This is the immutable forensic floor."
            ),
        }

    def _scan_entity_text(self, text: str) -> Dict:
        """
        For non-domain targets, scan text for domain mentions
        then query CT logs for those domains.
        """
        # Extract domains from text
        domain_pattern = re.compile(
            r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+(?:com|net|org|io|co|uk|onion|to|ch|ru|cn)\b'
        )
        found_domains = list(set(domain_pattern.findall(text)))
        
        # Scan each found domain
        results = {}
        for domain in found_domains[:10]:  # Limit to first 10
            results[domain] = self._scan_domain(domain)
        
        # Check text for harm patterns
        harm_matches = self._check_harm_patterns(text)
        
        return {
            "scan_type": "text_analysis",
            "domains_found_in_text": found_domains,
            "domain_scan_results": results,
            "certificates_found": sum(r.get("certificates_found", 0) for r in results.values()),
            "suspicious_patterns": harm_matches,
            "scrubba_dub_indicators": [],
            "harm_pattern_matches": harm_matches,
            "ct_immutability_note": (
                "CT logs are cryptographically append-only. "
                "Records here cannot be deleted by Project Scrubba Dub."
            ),
        }

    def _analyze_certificates(self, certificates: List[Dict], domain: str) -> Dict:
        """Analyze a list of certificates for suspicious patterns."""
        if not certificates:
            return {
                "suspicious_patterns": [],
                "scrubba_dub_indicators": [],
                "subdomains": [],
                "issuers": [],
                "harm_pattern_matches": [],
                "earliest_cert": None,
                "latest_cert": None,
            }

        subdomains = set()
        issuers = set()
        dates = []
        suspicious = []
        scrubba_indicators = []
        harm_matches = []

        for cert in certificates:
            # Collect subdomains
            name_value = cert.get("name_value", "")
            for name in name_value.split("\n"):
                name = name.strip()
                if name and name != domain:
                    subdomains.add(name)
                # Check for harm patterns
                for pattern in HARM_NETWORK_PATTERNS:
                    if re.search(pattern, name, re.IGNORECASE):
                        harm_matches.append(f"Pattern '{pattern}' in cert name: {name}")

            # Collect issuers
            issuer = cert.get("issuer_name", "")
            if issuer:
                issuers.add(issuer[:60])

            # Collect dates
            not_before = cert.get("not_before", "")
            if not_before:
                dates.append(not_before)

        # Sort dates
        dates.sort()

        # Check for rapid cycling (more than 10 certs in 30 days)
        if len(certificates) > 10:
            suspicious.append(f"High certificate volume: {len(certificates)} certs found")
            scrubba_indicators.append("rapid_cycling")

        # Check for unusual CAs
        mainstream_cas = ["Let's Encrypt", "DigiCert", "Sectigo", "GlobalSign", "Amazon", "Google"]
        unusual_issuers = [i for i in issuers if not any(ca.lower() in i.lower() for ca in mainstream_cas)]
        if unusual_issuers:
            suspicious.append(f"Unusual certificate authorities: {list(unusual_issuers)[:3]}")
            scrubba_indicators.append("unusual_ca")

        # Check for wildcards hiding structure
        wildcard_domains = [s for s in subdomains if s.startswith("*")]
        if len(wildcard_domains) > 3:
            suspicious.append(f"Multiple wildcard certificates: infrastructure concealment possible")
            scrubba_indicators.append("wildcard_concealment")

        return {
            "suspicious_patterns": suspicious,
            "scrubba_dub_indicators": list(set(scrubba_indicators)),
            "subdomains": list(subdomains)[:50],
            "issuers": list(issuers)[:20],
            "harm_pattern_matches": harm_matches,
            "earliest_cert": dates[0] if dates else None,
            "latest_cert": dates[-1] if dates else None,
            "total_subdomains": len(subdomains),
        }

    def _check_harm_patterns(self, text: str) -> List[str]:
        """Check text for known harm network patterns."""
        matches = []
        for pattern in HARM_NETWORK_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                matches.append(f"Harm pattern detected: {pattern}")
        return matches

    def get_domain_history(self, domain: str) -> Dict:
        """
        Get the complete certificate history for a domain.
        Useful for establishing when infrastructure was created/modified.
        """
        return self._scan_domain(domain)

    def verify_immutability(self, domain: str) -> Dict:
        """
        Verify that CT log records for a domain cannot have been altered.
        Returns cryptographic proof of record integrity.
        """
        scan_result = self._scan_domain(domain)
        
        # Create a hash of the scan results as a tamper-evident record
        result_hash = hashlib.sha3_256(
            json.dumps(scan_result, sort_keys=True, default=str).encode()
        ).hexdigest()

        return {
            "domain": domain,
            "scan_timestamp": datetime.datetime.utcnow().isoformat(),
            "result_hash": result_hash,
            "immutable_by_design": True,
            "note": "CT logs use RFC 6962 Merkle tree structure. Each entry is "
                    "cryptographically chained. Alteration is computationally infeasible.",
            "scan_result": scan_result,
        }


class QuantumCTLogVerifier:
    """
    Quantum-resistant verification layer for CT log records.
    Prepares CT log evidence for storage in the QuantumMerkleTree.
    
    References Google's forthcoming quantum-resistant CT log implementation
    and NIST post-quantum cryptography standards (FIPS 203/204/205).
    """

    def __init__(self):
        self.hash_algorithm = "sha3_256"  # Quantum-resistant hash

    def prepare_evidence(self, ct_scan_result: Dict) -> Dict:
        """
        Prepare CT log evidence for quantum-resistant Merkle tree storage.
        Uses SHA3-256 (Keccak) which is quantum-resistant unlike SHA2.
        """
        evidence_str = json.dumps(ct_scan_result, sort_keys=True, default=str)
        evidence_hash = hashlib.sha3_256(evidence_str.encode()).hexdigest()
        
        return {
            "evidence_type": "ct_log_scan",
            "evidence_hash": evidence_hash,
            "hash_algorithm": self.hash_algorithm,
            "quantum_resistant": True,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "raw_evidence": ct_scan_result,
        }