#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl
from coregen.utils import createSignal


class Port(hdl.SignalType):
    def __init__(self, name, pins):
        assert isinstance(name, str)
        assert isinstance(pins, list)

        self.name   = name
        self.pins   = pins
        self.signal = createSignal(0, len(pins))


class FPGA:
    vendor = None
    device = None
    family = None

    def __init__(self, top, **params):
        self.top        = top
        self.top_params = params

    def get_toolflow(self):
        raise NotImplementedError

    def convert(self, name, hdl='verilog', path='.'):
        pass

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
