#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl
from coregen.utils import createSignal
from coregen.utils import log2up


@hdl.block
def clk_div(clk_i, rst_i, uart_tick, uart_tick_x16, CLK_BUS=50000000, BAUD_RATE=115200):
    _divisor16 = CLK_BUS // (BAUD_RATE * 16)
    counter    = createSignal(0, 4)
    counter16  = createSignal(0, log2up(_divisor16))

    @hdl.always_seq(clk_i.posedge, reset=rst_i)
    def counter_proc():
        if counter16 == 0:
            counter.next   = counter + 1

    @hdl.always_seq(clk_i.posedge, reset=rst_i)
    def counter16_proc():
        if counter16 == _divisor16 - 1:
            counter16.next = 0
        else:
            counter16.next = counter16 + 1

    @hdl.always_seq(clk_i.posedge, reset=rst_i)
    def uart_tick_proc():
        uart_tick_x16.next = counter16 == 0
        uart_tick.next     = counter == 0 and uart_tick_x16

    return hdl.instances()

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
