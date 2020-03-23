from .generic_service import GenericService


class RDACService(GenericService):
    def run(self) -> None:
        self.create_socket()
        while True:
            try:
                data, address = self.serverSocket.recvfrom(4096)
                ip, port = address
                self.log("data (%d) received from %s.%s" % (len(data), ip, port))
                self.log(data.hex())
            except Exception as err:
                self.selfLogger.error(err, exc_info=True)


if __name__ == "__main__":
    t = RDACService()
    t.start()
