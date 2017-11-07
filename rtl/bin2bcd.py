#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl


@hdl.block
def bin2bcd(binary, thousands, hundreds, tens, ones):
    assert len(binary) <= 14, "[bin2bcd] Error: max length of 'binary' is 14. Wrong value: {1}".format(len(binary))
    assert len(thousands) == 4, "[bin2bcd] Error: len(thousands) must be 4"
    assert len(hundreds) == 4, "[bin2bcd] Error: len(hundreds) must be 4"
    assert len(tens) == 4, "[bin2bcd] Error: len(tens) must be 4"
    assert len(ones) == 4, "[bin2bcd] Error: len(ones) must be 4"

    @hdl.always_comb
    def decomp_proc():
        thousands.next = 0
        hundreds.next  = 0
        tens.next      = 0
        ones.next      = 0
        for i in range(len(binary)):
            if thousands >= 5:
                thousands.next = thousands + 3
            if hundreds >= 5:
                hundreds.next = hundreds + 3
            if tens >= 5:
                tens.next = tens + 3
            if ones >= 5:
                ones.next = ones + 3
            # shift left one
            thousands.next    = thousands << 1
            thousands[0].next = hundreds[3]
            hundreds.next     = hundreds << 1
            hundreds[0].next  = tens[3]
            tens.next         = tens << 1
            tens[0].next      = ones[3]
            ones.next         = ones << 1
            ones[0].next      = binary[i]

    return hdl.instances()


if __name__ == '__main__':
    from coregen.utils import createSignal
    b   = createSignal(0, 10)
    t   = createSignal(0, 4)
    h   = createSignal(0, 4)
    tn  = createSignal(0, 4)
    o   = createSignal(0, 4)
    dut = bin2bcd(b, t, h, tn, o)
    dut.convert(testbench=False)

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
