import asyncio
import sys
from asyncio import DatagramProtocol
from asyncio import transports
from typing import Any, Union

if __name__ == "__main__":
    listen_ip: str = sys.argv[1]
    listen_port: int = int(sys.argv[2])
    target_ip: str = sys.argv[3]
    target_port: int = int(sys.argv[4])
    print(f"Listen {listen_ip}:{listen_port} \nTarget {target_ip}:{target_port}")


class SimpleProtocol(DatagramProtocol):
    def datagram_received(self, data: bytes, addr: tuple[Union[str, Any], int]) -> None:
        print(f"datagram_received from {addr} data {data.hex()}")
        self.transport.sendto(bytes([0x44, 0x55, 0x66]), addr)
        exit()

    def connection_made(self, transport: transports.DatagramTransport) -> None:
        print(f"connection_made {transport}")
        self.transport: transports.DatagramTransport = transport
        transport.sendto(bytes([0x11, 0x22, 0x33]), (target_ip, target_port))


async def main() -> None:
    proto = SimpleProtocol()
    _transport, _protocol = await asyncio.get_running_loop().create_datagram_endpoint(
        lambda: proto, local_addr=(listen_ip, listen_port)
    )
    await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
