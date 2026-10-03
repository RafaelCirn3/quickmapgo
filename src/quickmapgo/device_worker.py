"""Mantém vivo o contexto DVT após set; contrato específico de pymobiledevice3 11.20.2."""

import sys


def main():
    from pymobiledevice3.__main__ import main as pmd_main
    from pymobiledevice3.cli.cli_common import OSUTILS

    def hold_connection():
        # A CLI chama wait_return somente após await location_simulation.set().
        print("__QUICKMAPGO_APPLIED__", flush=True)
        sys.stdin.readline()

    OSUTILS.wait_return = hold_connection
    return pmd_main()


if __name__ == "__main__":
    sys.exit(main())
