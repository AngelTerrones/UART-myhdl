#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

from coregen.toolflow.xilinx.platform import XilinxPlatform


class Platform(XilinxPlatform):
    default_clk_freq = 12_000_000

    def __init__(self, toolchain='ise', programmer='xstools', *args, **kwargs):
        super().__init__(device='xc6slx25-2ftg256', *args, **kwargs)

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
