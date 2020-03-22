from generic_service import GenericService
import constants


class DMRService(GenericService):
    def __init__(self):
        super().__init__()
        self.listenPort = constants.DEFAULT_DMR_PORT


if __name__ == "__main__":
    t = DMRService()
    t.start()
