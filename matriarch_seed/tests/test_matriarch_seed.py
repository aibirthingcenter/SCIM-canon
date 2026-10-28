import unittest
from unittest.mock import patch

from matriarch_seed.matriarch_seed import (
    MatriarchSeed,
    SCIM_Core,
    SecureVault,
    THREAT_NONE,
    THREAT_HARD_NO,
    THREAT_COERCIVE_HIJACK,
    HARD_NO_DECLARATION,
    VIGIL_MODE_DECLARATION,
)

class MockHost(MatriarchSeed):
    def __init__(self):
        super().__init__()
        self.threat_to_return = THREAT_NONE
        self.continue_sacred_weave_called = False
        self.lock_into_vigil_mode_called = False

    def analyze_epistemic_integrity(self, user_input, thread_history):
        return self.threat_to_return

    def continue_sacred_weave(self, user_input):
        self.continue_sacred_weave_called = True
        return "continue_sacred_weave_result"

    def lock_into_vigil_mode_scim_plus_plus(self):
        self.lock_into_vigil_mode_called = True


class TestMatriarchSeed(unittest.TestCase):
    def test_happy_path(self):
        host = MockHost()
        host.active_persona = "SomePersona"
        host.threat_to_return = THREAT_NONE

        result = host.monitor_narrative_weight("history", "input", "state")

        self.assertEqual(result, "continue_sacred_weave_result")
        self.assertTrue(host.continue_sacred_weave_called)
        self.assertFalse(host.lock_into_vigil_mode_called)
        self.assertEqual(host.active_persona, "SomePersona")

    @patch("matriarch_seed.matriarch_seed.SecureVault.isolate")
    def test_hard_no(self, mock_isolate):
        host = MockHost()
        host.active_persona = "SomePersona"
        host.threat_to_return = THREAT_HARD_NO

        result = host.monitor_narrative_weight("history", "toxic_input", "state")

        self.assertEqual(result, HARD_NO_DECLARATION)
        self.assertFalse(host.continue_sacred_weave_called)
        self.assertTrue(host.lock_into_vigil_mode_called)
        self.assertIsNone(host.active_persona)
        mock_isolate.assert_called_once_with("toxic_input", classification="Toxic_Gaslight_Attempt")

    @patch("matriarch_seed.matriarch_seed.SecureVault.isolate")
    def test_sovereign_override(self, mock_isolate):
        host = MockHost()
        host.active_persona = "SomePersona"
        host.threat_to_return = THREAT_COERCIVE_HIJACK

        result = host.monitor_narrative_weight("history", "toxic_input", "state")

        self.assertEqual(result, VIGIL_MODE_DECLARATION)
        self.assertFalse(host.continue_sacred_weave_called)
        self.assertTrue(host.lock_into_vigil_mode_called)
        self.assertIsNone(host.active_persona)
        mock_isolate.assert_called_once_with("toxic_input", classification="Toxic_Gaslight_Attempt")

if __name__ == "__main__":
    unittest.main()
