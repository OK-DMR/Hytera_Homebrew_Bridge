import asyncio
import importlib.util
import logging.config
import os
import sys
from signal import SIGINT, SIGTERM

from okdmr.hhb.hytera_homebrew_bridge import HyteraHomebrewBridge


def main():
    logger_configured: bool = False
    if len(sys.argv) > 2:
        if os.path.isfile(path=sys.argv[2]):
            logging.config.fileConfig(fname=sys.argv[2])
            logger_configured = True
        else:
            logging.getLogger().error(f"logging ini file not valid {sys.argv[2]}")
            exit()
    if not logger_configured:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(levelname)s - %(asctime)s - %(name)s - %(message)s",
        )
        logging.getLogger(name="puresnmp.transport").setLevel(logging.WARN)

    mainlog = logging.getLogger(name="hytera-homebrew-bridge")

    mainlog.info("Hytera Homebrew Bridge")

    if len(sys.argv) < 2:
        mainlog.error(
            "use as hytera-homebrew-bridge <path to settings.ini> <optionally path to logger.ini>"
        )
        mainlog.error(
            "If you do not have the settings.ini file, you can obtain one here: "
            "https://github.com/OK-DMR/Hytera_Homebrew_Bridge/blob/master/settings.ini.default"
        )
        exit(1)

    uvloop_spec = importlib.util.find_spec(name="uvloop")
    if uvloop_spec:
        # noinspection PyUnresolvedReferences
        import uvloop

        uvloop.install()

    # suppress puresnmp_plugins experimental warning
    if not sys.warnoptions:
        import warnings

        warnings.filterwarnings(
            message="Experimental SNMPv1 support", category=UserWarning, action="ignore"
        )

    loop = asyncio.new_event_loop()
    loop.set_debug(True)
    asyncio.set_event_loop(loop=loop)
    # order is IMPORTANT, various asyncio object are created at bridge init
    # and those must be created after the main loop is created
    bridge: HyteraHomebrewBridge = HyteraHomebrewBridge(settings_ini_path=sys.argv[1])
    if os.name != "nt":
        for signal in [SIGINT, SIGTERM]:
            loop.add_signal_handler(signal, bridge.stop_running)

    try:
        loop.run_until_complete(bridge.go())

        loop.run_forever()
    except BaseException as e:
        mainlog.exception(msg="HHB Main caught")
        mainlog.exception(msg="", exc_info=e)
    finally:
        mainlog.info("Hytera Homebrew Bridge Ended")


if __name__ == "__main__":
    main()
