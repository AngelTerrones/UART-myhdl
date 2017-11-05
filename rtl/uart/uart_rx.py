#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl
from coregen.utils import createSignal


@hdl.block
def uart_rx(clk_i, rst_i, rx_tick_i, rx_i, dat_o, ready_o):
    rx_sync     = createSignal(0b111, 3)
    rx_r        = createSignal(1, 1)
    bit_spacing = createSignal(0, 4)
    nxt_bit     = createSignal(0, 1)
    bit_cnt     = createSignal(0, 3)
    dat_r       = createSignal(0, 8)
    rx_state    = hdl.enum('IDLE', 'DATA', 'STOP')
    state       = hdl.Signal(rx_state.IDLE)

    @hdl.always_seq(clk_i.posedge, reset=rst_i)
    def rx_sync_proc():
        if rx_tick_i:
            rx_sync.next = hdl.concat(rx_sync[2:0], rx_i)

    @hdl.always_comb
    def assign_proc():
        rx_r.next  = rx_sync == 0b111 or rx_sync == 0b011 or rx_sync == 0b101 or rx_sync == 0b110
        dat_o.next = dat_r

    @hdl.always_seq(clk_i.posedge, reset=rst_i)
    def nxt_bit_proc():
        nxt_bit.next = bit_spacing == 0b1111
        if rx_tick_i and state != rx_state.IDLE:
            bit_spacing.next = bit_spacing + hdl.modbv(1)[4:]

    @hdl.always_seq(clk_i.posedge, reset=rst_i)
    def fsm_proc():
        if state == rx_state.IDLE:
            ready_o.next = False
            if not rx_r:
                state.next = rx_state.DATA
        elif state == rx_state.DATA:
            if nxt_bit:
                dat_r.next   = hdl.concat(rx_r, dat_r[8:1])
                bit_cnt.next = bit_cnt + 1
                if bit_cnt == 7:
                    state.next = rx_state.STOP
        elif state == rx_state.STOP:
            if nxt_bit:
                state.next = rx_state.IDLE
                ready_o.next = True
        else:
            state.next = rx_state.IDLE

    return hdl.instances()

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End: