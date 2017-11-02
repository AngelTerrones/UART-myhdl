#-------------------------------------------------------------------------------
# Makefile for EC1723-Lab 4.
# Author: Angel Terrones <aterrones@usb.ve>
#-------------------------------------------------------------------------------
.FOUT=build
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
# S3 (Using SPARTAN-3)
#-------------------------------------------------------------------------------
.BRD=xula2
.TOPE_V=banner

ifeq ($(.BRD), xula2)
	.FPGA=xc6slx25-2-ftg256  # SPARTAN-6
	.CLK=12
	.RST_NEG=--rst_neg
	.CLK_SRC=Cclk  # Or JtagClk
else ifeq ($(.BRD), s3)
	.FPGA=xc3s200-ft256-4  # SPARTAN-3
	.CLK=50
	.CLK_SRC=JtagClk
else
$(error Invalid FPGA board)
endif

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
	@verilator --lint-only $(.FOUT)/$(.TOPE_V).v && echo "CHECK: OK"

# ********************************************************************
# Test
# ********************************************************************
test-myhdl:
	@rm -f *.vcd*
	@PYTHONPATH=$(PWD) $(.PYTEST) --tb=short -s test/

test-cosim:
	@mkdir -p $(.FOUT)
	@PYTHONPATH=$(PWD) $(.PYTEST) --tb=short test/

# ********************************************************************
# Implementation
# ********************************************************************


# ********************************************************************
# Clean
# ********************************************************************
clean:
	@rm -rf $(.FOUT)/
	@find . | grep -E "(\.vcd)" | xargs rm -rf

distclean: clean
	@find . | grep -E "(__pycache__|\.pyc|\.pyo|\.vcd|\.cache)" | xargs rm -rf
