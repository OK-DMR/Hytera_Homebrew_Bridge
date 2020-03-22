from .generic_service import GenericService
from .constants import *


class DMRService(GenericService):
    def __init__(self):
        super().__init__()
        self.listenPort = self.DEFAULT_LISTEN_PORT = DEFAULT_DMR_PORT


if __name__ == "__main__":
    t = DMRService()
    t.start()
