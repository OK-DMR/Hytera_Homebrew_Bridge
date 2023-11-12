from okdmr.dmrlib.storage import ADDRESS_TYPE, ADDRESS_EMPTY
from okdmr.dmrlib.storage.repeater import Repeater
from okdmr.dmrlib.storage.repeater_storage import RepeaterStorage

from okdmr.hhb.hytera_repeater import HyteraRepeater


class HHBRepeaterStorage(RepeaterStorage):
    """ """

    def create_repeater(
        self,
        dmr_id: int = None,
        address_in: ADDRESS_TYPE = ADDRESS_EMPTY,
        address_out: ADDRESS_TYPE = ADDRESS_EMPTY,
        address_nat: ADDRESS_TYPE = ADDRESS_EMPTY,
    ) -> Repeater:
        return HyteraRepeater(
            address_in=address_in,
            address_out=address_out,
            dmr_id=dmr_id,
            address_nat=address_nat,
        )
