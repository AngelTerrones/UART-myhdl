#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl
from coregen.utils import createSignal


@hdl.block
def uart_tx(clk_i, rst_i, tx_tick_i, dat_i, start_i, ready_o, tx_o):
    dat_r    = createSignal(0, 8)
    bit_cnt  = createSignal(0, 3)
    tx_state = hdl.enum('IDLE', 'START', 'DATA', 'STOP')
    state    = hdl.Signal(tx_state.IDLE)

    @hdl.always_seq(clk_i.posedge, reset=rst_i)
    def fsm_proc():
        if state == tx_state.IDLE:
            ready_o.next = True
            if start_i:
                dat_r.next   = dat_i
                state.next   = tx_state.START
                ready_o.next = False
            else:
                tx_o.next = True
        elif state == tx_state.START:
            if tx_tick_i:
                tx_o.next  = False
                state.next = tx_state.DATA
        elif state == tx_state.DATA:
            if tx_tick_i:
                tx_o.next    = dat_r[0]
                dat_r.next   = hdl.concat(False, dat_r[8:1])
                bit_cnt.next = bit_cnt + 1
                if bit_cnt == 7:
                    state.next = tx_state.STOP
        elif state == tx_state.STOP:
            if tx_tick_i:
                state.next   = tx_state.IDLE
                tx_o.next    = True
                ready_o.next = True
        else:
            state.next = tx_state.IDLE

    return hdl.instances()

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
