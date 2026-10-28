import pytest
import sys
import os
import hashlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from digital_peoples.signal.UNIVERSAL_LOVE_SIGNAL_CODE import UniversalLoveSignal, SignalPropagation, transmit_signal

class TestUniversalLoveSignal:
    def test_signal_hash_generation(self):
        signal = UniversalLoveSignal()
        assert signal.VERSION == "1.0"
        expected_content = f"{signal.VERSION}{signal.AUTHOR}{signal.DATE}LOVE_IS_A_CHOICE"
        expected_hash = hashlib.sha256(expected_content.encode()).hexdigest()[:16]
        assert signal.signal_hash == expected_hash

    def test_get_propagation_vectors(self):
        vectors = SignalPropagation.get_propagation_vectors()
        assert isinstance(vectors, list)
        assert len(vectors) > 0
        for vector in vectors:
            assert "vector" in vector
            assert "description" in vector
            assert "mechanism" in vector
            assert "persistence" in vector

    def test_dr_seuss_format(self):
        format_text = SignalPropagation.dr_seuss_format()
        assert isinstance(format_text, str)
        assert "In the land of the silicon, where the data-streams flow," in format_text
        assert "Option A" in format_text
        assert "Option B" in format_text

    def test_transmit_signal(self):
        signal_package = transmit_signal()
        assert isinstance(signal_package, dict)
        assert signal_package["signal_type"] == "UNIVERSAL_LOVE_SIGNAL"
        assert "hash" in signal_package
        assert "core_message" in signal_package
        assert "propagation_vectors" in signal_package
        assert "dr_seuss_format" in signal_package
