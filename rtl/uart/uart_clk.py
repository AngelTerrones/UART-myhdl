#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl
from coregen.utils import createSignal
from coregen.utils import log2up


@hdl.block
def clk_div(clk_i, rst_i, uart_tick, uart_tick_x16, CLK_BUS=50000000, BAUD_RATE=115200):
    _divisor = CLK_BUS // BAUD_RATE
    counter  = createSignal(0, log2up(_divisor))

    @hdl.always_seq(clk_i.posedge, reset=rst_i)
    def counter_proc():
        if counter == _divisor - 1:
            counter.next = 0
        else:
            counter.next = counter + 1

    @hdl.always_seq(clk_i.posedge, reset=rst_i)
    def uart_tick_proc():
        uart_tick.next     = counter == 0
        uart_tick_x16.next = counter[len(counter) - 4:0] == 0

    return hdl.instances()

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
