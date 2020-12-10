import configparser
import logging
import socket
from threading import Thread


class HomebrewService(Thread):
    """Main thread of Homebrew client
    """

    UPSTREAM_IP: str
    UPSTREAM_PORT: int
    UPSTREAM_PASSWORD: str

    clientSocket: socket
    selfLogger: logging.Logger = None

    def start(self) -> None:
        self.load_settings()

        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((self.UPSTREAM_IP, self.UPSTREAM_IP))

    def load_settings(self) -> None:
        config = configparser.ConfigParser()
        config.sections()
        config.read("settings.ini")

        if "homebrew" in config:
            homebrew_config = config["homebrew"]
            if "MASTER_IP" in homebrew_config:
                self.UPSTREAM_IP = str(homebrew_config["MASTER_IP"])
            if "MASTER_PORT" in homebrew_config:
                self.UPSTREAM_PORT = int(homebrew_config["MASTER_PORT"])
            if "MASTER_PASSWORD" in homebrew_config:
                self.UPSTREAM_PASSWORD = str(homebrew_config["MASTER_PASSWORD"])

        self.log(
            "load_settings finished found %s %d %s"
            % (self.UPSTREAM_IP, self.UPSTREAM_PORT, self.UPSTREAM_PASSWORD)
        )

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
