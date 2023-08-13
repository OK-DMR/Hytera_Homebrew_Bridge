class CallbackInterface:
    """
    This interface doesn't have other purpose than code de-duplication
    """

    async def homebrew_connect(self, ip: str, port: int) -> None:
        pass
