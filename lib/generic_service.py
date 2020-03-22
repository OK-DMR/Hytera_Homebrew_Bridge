from __future__ import annotations
from threading import Thread
from .storage import Storage
from .constants import *
import logging
import socket


class GenericService(Thread):
    DEFAULT_LISTEN_PORT: int

    listenPort: int
    listenIP: str = DEFAULT_SERVICE_IP
    serverSocket: socket
    selfLogger: logging.Logger = None
    storage: Storage = Storage.instance()

    def log(self, msg, level=logging.INFO):
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

    def set_port(self, port: int) -> GenericService:
        self.listenPort = self.DEFAULT_LISTEN_PORT if not port else port
        self.log("Listen on Port set %s" % self.listenPort)
        return self

    def set_ip(self, ip: str) -> GenericService:
        self.listenIP = DEFAULT_SERVICE_IP if not ip else ip
        self.log("Listen on IP set %s" % self.listenIP)
        return self

    def create_socket(self) -> GenericService:
        self.serverSocket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
        )
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((self.listenIP, self.listenPort))
        self.log("server socket created")
        return self
