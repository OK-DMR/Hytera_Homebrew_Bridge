from .generic_service import GenericService
from .constants import *


class RDACService(GenericService):
    def __init__(self):
        super().__init__()
        self.listenPort = self.DEFAULT_LISTEN_PORT = DEFAULT_RDAC_PORT


if __name__ == "__main__":
    t = RDACService()
    t.start()
