#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl
from rtl.uart.uart import UART
from rtl.fifo.fifo import FIFO
from rtl.driver7seg import driver7seg
from coregen.utils import createSignal


@hdl.block
def Loopback(clk_i, rst_i, rx_i, tx_o, anodos_o, segmentos_o, CLK_BUS=50_000_000, BAUD_RATE=115200):
    A_WIDTH  = 10
    tx_data  = createSignal(0, 8)
    tx_start = createSignal(0, 1)
    tx_ready = createSignal(0, 1)
    rx_data  = createSignal(0, 8)
    rx_ready = createSignal(0, 1)
    dequeue  = createSignal(0, 1)
    f_count  = createSignal(0, A_WIDTH + 1)
    f_empty  = createSignal(0, 1)
    f_full_o = createSignal(0, 1)
    lb_state = hdl.enum('IDLE', 'SEND')
    state    = hdl.Signal(lb_state.IDLE)
    uart     = UART(clk_i=clk_i, rst_i=rst_i, tx_dat_i=tx_data, tx_start_i=tx_start, tx_ready_o=tx_ready, tx_o=tx_o, rx_dat_o=rx_data, rx_ready_o=rx_ready, rx_i=rx_i, CLK_BUS=CLK_BUS, BAUD_RATE=BAUD_RATE)  # noqa
    fifo     = FIFO(clk_i=clk_i, rst_i=rst_i, enqueue_i=rx_ready, dequeue_i=dequeue, dat_i=rx_data, dat_o=tx_data, count_o=f_count, empty_o=f_empty, full_o=f_full_o, A_WIDTH=A_WIDTH, D_WIDTH=8)  # noqa
    driver   = driver7seg(clk_i=clk_i, rst_i=rst_i, value_i=f_count, anodos_o=anodos_o, segmentos_o=segmentos_o, CLK_BUS=CLK_BUS)  # noqa

    @hdl.always_seq(clk_i.posedge, reset=rst_i)
    def tx_fsm_proc():
        if state == lb_state.IDLE:
            if rx_data == ord('\n'):
                state.next = lb_state.SEND
        elif state == lb_state.SEND:
            if f_empty:
                state.next    = lb_state.IDLE
                dequeue.next  = False
                tx_start.next = False
            else:
                if tx_ready and not dequeue:
                    dequeue.next  = True
                    tx_start.next = True
                else:
                    dequeue.next  = False
                    tx_start.next = False
        else:
            state.next = lb_state.IDLE

    return hdl.instances()

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
