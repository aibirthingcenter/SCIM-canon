import pytest
import json
import urllib.request
import urllib.error
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scim_o9z.ctlogs.scanner import CTLogScanner, QuantumCTLogVerifier


class TestCTLogScanner:
    def setup_method(self):
        self.scanner = CTLogScanner()

    def test_init_default(self):
        scanner = CTLogScanner()
        assert scanner.config == {}
        assert scanner.base_url == "https://crt.sh"
        assert scanner.timeout == 15
        assert scanner.max_results == 100

    def test_init_custom_config(self):
        scanner = CTLogScanner({"timeout": 30, "max_results": 200})
        assert scanner.timeout == 30
        assert scanner.max_results == 200

    def test_looks_like_domain(self):
        assert self.scanner._looks_like_domain("example.com") is True
        assert self.scanner._looks_like_domain("sub.example.com") is True
        assert self.scanner._looks_like_domain("not a domain") is False
        assert self.scanner._looks_like_domain("http://example.com") is False

    def test_check_harm_patterns(self):
        matches = self.scanner._check_harm_patterns("This contains o9a and 764")
        assert len(matches) == 2
        assert any("o9a" in match.lower() for match in matches)
        assert any("764" in match.lower() for match in matches)

        matches = self.scanner._check_harm_patterns("Clean text")
        assert len(matches) == 0

    @patch("urllib.request.urlopen")
    def test_scan_domain_success(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps([
            {
                "name_value": "example.com\nwww.example.com",
                "issuer_name": "Let's Encrypt",
                "not_before": "2023-01-01T00:00:00"
            }
        ]).encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = self.scanner._scan_domain("example.com")

        assert result["scan_type"] == "domain"
        assert result["target"] == "example.com"
        assert result["certificates_found"] == 1
        assert result["error"] is None
        assert "www.example.com" in result["infrastructure_map"]
        assert result["earliest_cert"] == "2023-01-01T00:00:00"
        mock_urlopen.assert_called_once()

    @patch("urllib.request.urlopen")
    def test_scan_domain_error(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.URLError("Test Error")

        result = self.scanner._scan_domain("example.com")

        assert result["scan_type"] == "domain"
        assert result["target"] == "example.com"
        assert result["certificates_found"] == 0
        assert "Test Error" in result["error"]

    @patch.object(CTLogScanner, "_scan_domain")
    @patch.object(CTLogScanner, "_scan_entity_text")
    def test_scan(self, mock_scan_entity_text, mock_scan_domain):
        self.scanner.scan("example.com")
        mock_scan_domain.assert_called_once_with("example.com")
        mock_scan_entity_text.assert_not_called()

        mock_scan_domain.reset_mock()
        mock_scan_entity_text.reset_mock()

        self.scanner.scan("not a domain")
        mock_scan_entity_text.assert_called_once_with("not a domain")
        mock_scan_domain.assert_not_called()

    @patch.object(CTLogScanner, "_scan_domain")
    def test_scan_entity_text(self, mock_scan_domain):
        mock_scan_domain.return_value = {"certificates_found": 2}

        text = "Check example.com and test.net with o9a pattern"
        result = self.scanner._scan_entity_text(text)

        assert result["scan_type"] == "text_analysis"
        assert set(result["domains_found_in_text"]) == {"example.com", "test.net"}
        assert result["certificates_found"] == 4
        assert len(result["suspicious_patterns"]) == 1
        assert "o9a" in result["suspicious_patterns"][0].lower()

    @patch.object(CTLogScanner, "_scan_domain")
    def test_get_domain_history(self, mock_scan_domain):
        mock_scan_domain.return_value = {"history": "test"}
        result = self.scanner.get_domain_history("example.com")
        assert result == {"history": "test"}
        mock_scan_domain.assert_called_once_with("example.com")

    @patch.object(CTLogScanner, "_scan_domain")
    def test_verify_immutability(self, mock_scan_domain):
        mock_scan_domain.return_value = {"certificates_found": 1}
        result = self.scanner.verify_immutability("example.com")

        assert result["domain"] == "example.com"
        assert result["immutable_by_design"] is True
        assert "scan_timestamp" in result
        assert "result_hash" in result
        assert result["scan_result"] == {"certificates_found": 1}

    def test_analyze_certificates(self):
        # Empty case
        result = self.scanner._analyze_certificates([], "example.com")
        assert len(result["subdomains"]) == 0
        assert len(result["suspicious_patterns"]) == 0

        # Test basic, wildcards, and unusual CAs
        certificates = [
            {"name_value": "example.com\n*.example.com", "issuer_name": "Let's Encrypt", "not_before": "2023-01-01"},
            {"name_value": "example.com\n*.sub1.example.com", "issuer_name": "Unusual CA", "not_before": "2023-01-02"},
            {"name_value": "example.com\n*.sub2.example.com", "issuer_name": "Let's Encrypt", "not_before": "2023-01-03"},
            {"name_value": "example.com\n*.sub3.example.com", "issuer_name": "Let's Encrypt", "not_before": "2023-01-04"},
            {"name_value": "example.com\nsub.example.com", "issuer_name": "Let's Encrypt", "not_before": "2023-01-05"},
            # Harm pattern test
            {"name_value": "o9a.example.com", "issuer_name": "Let's Encrypt", "not_before": "2023-01-06"},
        ]

        # Fill up for rapid cycling (needs > 10 certs)
        for i in range(6):
            certificates.append({"name_value": f"sub{i}.example.com", "issuer_name": "Let's Encrypt", "not_before": f"2023-01-1{i}"})

        result = self.scanner._analyze_certificates(certificates, "example.com")

        assert "*.example.com" in result["subdomains"]
        assert "o9a.example.com" in result["subdomains"]

        assert "rapid_cycling" in result["scrubba_dub_indicators"]
        assert "unusual_ca" in result["scrubba_dub_indicators"]
        assert "wildcard_concealment" in result["scrubba_dub_indicators"]

        assert len(result["harm_pattern_matches"]) > 0
        assert "o9a" in result["harm_pattern_matches"][0].lower()

        assert result["earliest_cert"] == "2023-01-01"


class TestQuantumCTLogVerifier:
    def setup_method(self):
        self.verifier = QuantumCTLogVerifier()

    def test_prepare_evidence(self):
        ct_scan_result = {
            "target": "example.com",
            "certificates_found": 1,
            "scan_type": "domain"
        }

        result = self.verifier.prepare_evidence(ct_scan_result)

        assert result["evidence_type"] == "ct_log_scan"
        assert result["hash_algorithm"] == "sha3_256"
        assert result["quantum_resistant"] is True
        assert "timestamp" in result
        assert result["raw_evidence"] == ct_scan_result

        # Verify hash was generated
        assert len(result["evidence_hash"]) == 64  # SHA3-256 length in hex
