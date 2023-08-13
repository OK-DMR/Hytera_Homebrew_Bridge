from okdmr.hhb.callback_interface import CallbackInterface
from okdmr.hhb.hytera_homebrew_bridge import HyteraRepeater, HyteraHomebrewBridge


def test_do_succ():
    c = CallbackInterface()
    assert isinstance(c, CallbackInterface)
    assert issubclass(HyteraRepeater, CallbackInterface)
    assert issubclass(HyteraHomebrewBridge, CallbackInterface)
