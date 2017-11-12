#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import os
import argparse


class Coregen:
    _build_path = './build'

    def __init__(self, board):
        parser    = argparse.ArgumentParser(description='Core generation.')
        subparser = parser.add_subparsers(title='Sub-commands', description='Available functions')
        # convert
        p2v = subparser.add_parser('to_verilog')
        p2v.set_defaults(func=self.convert_to_verilog)
        # build
        build = subparser.add_parser('build')
        build.set_defaults(func=self.build_project)
        # program
        prog = subparser.add_parser('program')
        prog.set_defaults(func=self.program)

        self.parser = parser
        self.board  = board

    def run(self):
        args = self.parser.parse_args()

        try:
            args.func(args)
        except AttributeError:
            self.parser.print_help()

    def convert_to_verilog(self, args):
        os.makedirs(self._build_path, exist_ok=True)
        self.board.convert(path=self._build_path, trace=False, testbench=False)

    def build_project(self, args):
        os.makedirs(self._build_path, exist_ok=True)
        self.board.build(path=self._build_path)

    def program(self, args):
        self.board.program()

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
