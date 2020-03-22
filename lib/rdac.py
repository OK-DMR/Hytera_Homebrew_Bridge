from generic_service import GenericService
import constants


class RDACService(GenericService):
    def __init__(self):
        super().__init__()
        self.listenPort = constants.DEFAULT_RDAC_PORT


if __name__ == "__main__":
    t = RDACService()
    t.start()
