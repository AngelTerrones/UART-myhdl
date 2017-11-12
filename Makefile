#-------------------------------------------------------------------------------
# Makefile for EC1723-Lab 4.
# Author: Angel Terrones <aterrones@usb.ve>
#-------------------------------------------------------------------------------
.PYTHON=python3
.PYTEST=pytest

.PWD=$(shell pwd)
.RTL_FOLDER=$(shell cd rtl; pwd)
.PYTHON_FILES=$(shell find $(.RTL_FOLDER) -name "*.py")
.SCRIPT_FOLDER=$(shell cd scripts; pwd)

#-------------------------------------------------------------------------------
# FPGA
#-------------------------------------------------------------------------------
# Boards:
# Xula2 (using SPARTAN-6)
# spartan3sb (Using SPARTAN-3)
#-------------------------------------------------------------------------------
.BRD=xula2
.TOPE_V=Loopback

#-------------------------------------------------------------------------------
# XILINX ISE
#-------------------------------------------------------------------------------
ifeq ($(shell uname), Linux)
		.ISE_BIN=/opt/Xilinx/14.7/ISE_DS/ISE/bin/lin64
else
		.ISE_BIN=/cygdrive/c/Xilinx/14.7/ISE_DS/ISE/bin/nt
endif
export PATH:=$(.ISE_BIN):$(PATH)

# ********************************************************************
.PHONY: default clean distclean

# ********************************************************************
# Syntax check
# ********************************************************************
check-verilog: to-verilog
	@verilator --lint-only build/$(.TOPE_V).v && echo "CHECK: OK"

# ********************************************************************
# Test
# ********************************************************************
run-tests:
	@rm -f *.vcd*
	$(.PYTEST) --tb=short -s test/

# ********************************************************************
# Implementation
# ********************************************************************
to-verilog: $(.PYTHON_FILES) build/$(.TOPE_V).v

# ---
%.v: $(.PYTHON_FILES)
	@PYTHONPATH=$(PWD) $(.PYTHON) $(.SCRIPT_FOLDER)/build_$(.BRD).py toverilog

# ********************************************************************
# Clean
# ********************************************************************
clean:
	@rm -rf build/
	@find . | grep -E "(\.vcd|\.v)" | xargs rm -rf

distclean: clean
	@find . | grep -E "(__pycache__|\.pyc|\.pyo|\.cache)" | xargs rm -rf
