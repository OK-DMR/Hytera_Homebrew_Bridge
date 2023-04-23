from okdmr.hhb.callback_interface import CallbackInterface


def test_do_succ():
    c = CallbackInterface()
    assert isinstance(c, CallbackInterface)
