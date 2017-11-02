#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl
from rtl.utils import createSignal
from rtl.utils import log2up


@hdl.block
def clk_div(clk_i, rst_i, uart_tick, uart_tick_16x, CLK_BUS=50000000, BAUD_RATE=115200):
    _divisor = CLK_BUS//(BAUD_RATE * 16)  # clk base for rx (x16)

    counter = createSignal(0, log2up(_divisor))

    return hdl.instances()

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
