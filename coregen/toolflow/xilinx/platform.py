#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

from coregen.toolflow.tools import write2file
from coregen.toolflow.platform import Platform


def _format_ucf(signame, pin):
    pass


def _build_ucf():
    pass


class XilinxPlatform(Platform):
    bitfile_ext = '.bit'

    def __init__(self, toolchain='ise', *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build(self, **kwargs):
        print("Xilinx Build")

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
