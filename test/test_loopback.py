#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl
from coregen.utils import createSignal
from rtl.loopback import Loopback

# Constantes
CLK_XTAL    = 5000
BAUD        = 10
TXRX_DATA   = [ord(i) for i in "Hello world! :D"]
TIMEOUT     = int(5*(12*len(TXRX_DATA)/BAUD)*CLK_XTAL)  # 12 symbols x char. Worst case: 5 times the message
TICK_PERIOD = 10
RESET_TIME  = 5


@hdl.block
def clk_n_timeout(clk, rst):
    @hdl.always(hdl.delay(int(TICK_PERIOD / 2)))
    def gen_clock():
        clk.next = not clk

    @hdl.instance
    def timeout():
        rst.next = True
        yield hdl.delay(RESET_TIME * TICK_PERIOD)
        rst.next = False
        yield hdl.delay(TIMEOUT * TICK_PERIOD)
        raise hdl.Error("Test failed: TIMEOUT")

    return hdl.instances()


@hdl.block
def loopback_testbench():
    clk       = createSignal(0, 1)
    rst       = hdl.ResetSignal(0, active=True, async=False)
    clk_tout  = clk_n_timeout(clk, rst)  # noqa
    rx        = createSignal(1, 1)
    tx        = createSignal(0, 1)
    anodos    = createSignal(0, 4)
    segmentos = createSignal(0, 8)
    clk_tout  = clk_n_timeout(clk, rst)  # noqa
    dut       = Loopback(clk_i=clk, rst_i=rst, rx_i=rx, tx_o=tx, anodos_o=anodos, segmentos_o=segmentos, CLK_BUS=CLK_XTAL, BAUD_RATE=BAUD)  # noqa

    rx_data   = createSignal(0, 8)
    rx_buffer = []

    def _rx_proc(data):
        yield tx.negedge
        data.next = 0
        yield hdl.delay((CLK_XTAL // (BAUD * 2)) * TICK_PERIOD)
        for _ in range(8):
            yield hdl.delay((CLK_XTAL // BAUD) * TICK_PERIOD)
            data.next = hdl.concat(tx, data[8:1])
        yield tx.posedge

    def _tx_proc(data, tx):
        tx.next = False
        yield hdl.delay((CLK_XTAL // BAUD) * TICK_PERIOD)
        for i in range(8):
            tx.next = (data >> i) & 0x01
            yield hdl.delay((CLK_XTAL // BAUD) * TICK_PERIOD)
        tx.next = True
        yield hdl.delay((CLK_XTAL // BAUD) * TICK_PERIOD)

    @hdl.instance
    def rx_proc():
        for _ in range(len(TXRX_DATA)):
            yield _rx_proc(rx_data)
            if rx_data != '\n':
                rx_buffer.append(int(rx_data))
        assert TXRX_DATA == rx_buffer, "[Loopback Error]: Send: {0}, Received: {1}".format(TXRX_DATA, rx_buffer)

        raise hdl.StopSimulation

    @hdl.instance
    def tx_proc():
        yield hdl.delay(2*(CLK_XTAL // BAUD) * TICK_PERIOD)
        for data in TXRX_DATA:
            yield _tx_proc(data, rx)
        yield _tx_proc(ord('\n'), rx)

    return hdl.instances()


def test_loopback():
    tb = loopback_testbench()
    tb.config_sim(trace=True)
    tb.run_sim()

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
