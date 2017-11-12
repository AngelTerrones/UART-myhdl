#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

from coregen.coregen import Coregen
from coregen.boards import Xula2
from rtl.loopback import Loopback
from coregen.toolflow.platform import Port
from coregen.toolflow.platform import ResetPort


def main():
    io = dict(clk_i=Port('T9'),
              rst_i=ResetPort('T2', val=0, active=False, async=False),
              rx_i=Port('B2'),
              tx_o=Port('B1'),
              anodos_o=Port('F16 F15 J14 J16'),
              segmentos_o=Port('T7 R7 R15 R16 M15 M16 K15 K16'))
    params = dict(FIFO_DEPTH=500, CLK_BUS=Xula2.Platform.default_clk_freq)
    board   = Xula2.Platform(module=Loopback, io=io, params=params)
    Coregen(board).run()


if __name__ == '__main__':
    main()

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
