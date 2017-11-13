#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import subprocess
from coregen.toolflow.programmer import Programmer


def _run_impact(cmd):
    print("iMPACT cmd: ", cmd)


class iMPACT(Programmer):
    def load_bitstream(self, bitfile):
        cmd = "setMode -bs"
        _run_impact(cmd)

    def flash(self, bitfile):
        cmd = "setMode -bs"
        _run_impact(cmd)


class XSTOOLS(Programmer):
    def __init__(self, model):
        self.model = model

    def load_bitstream(self, bitfile):
        print('Loading "{}" to FPGA. Model: {}'.format(bitfile, self.model))
        subprocess.call(['xsload', '--fpga', bitfile, '-b', self.model])

    def flash(self, bitfile):
        print('Loading "{}" to FLASH. Model: {}'.format(bitfile, self.model))
        subprocess.call(['xsload', '--flash', bitfile, '-b', self.model])

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
