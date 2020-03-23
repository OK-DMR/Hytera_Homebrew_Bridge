from __future__ import annotations
from threading import Thread
from .storage import Storage
import logging
import socket


class GenericService(Thread):
    DEFAULT_LISTEN_PORT: int

    serverSocket: socket
    selfLogger: logging.Logger = None
    storage: Storage = None

    def log(self, msg, level=logging.INFO) -> None:
        if not self.selfLogger:
            self.selfLogger = logging.getLogger(type(self).__name__)
            self.selfLogger.setLevel(logging.DEBUG)
            console_log_output = logging.StreamHandler()
            console_log_output.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            console_log_output.setFormatter(formatter)
            self.selfLogger.addHandler(console_log_output)
        self.selfLogger.log(level, msg)

    def set_storage(self, storage_instance: Storage) -> GenericService:
        self.storage = storage_instance
        return self

    def get_ip(self) -> str:
        if isinstance(self.storage, Storage):
            return self.storage.get_service_ip()
        raise AssertionError("no storage set %s" % type(self.storage))

    def get_port(self) -> int:
        if isinstance(self.storage, Storage):
            return self.storage.get_service_port(type(self).__name__)
        raise AssertionError("no storage set")

    def create_socket(self) -> GenericService:
        self.serverSocket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
        )
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((self.get_ip(), self.get_port()))
        self.log("server socket created %s:%s" % (self.get_ip(), self.get_port()))
        return self
