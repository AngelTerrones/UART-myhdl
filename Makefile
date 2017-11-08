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
.TOPE_V=Loopback

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
run-tests:
	@rm -f *.vcd*
	$(.PYTEST) --tb=short -s test/

# ********************************************************************
# Implementation
# ********************************************************************
to-verilog: $(.PYTHON_FILES) $(.FOUT)/$(.TOPE_V).v

# ---
%.v: $(.PYTHON_FILES)
	@mkdir -p $(.FOUT)
	@PYTHONPATH=$(PWD) $(.PYTHON) $(.SCRIPT_FOLDER)/core_gen.py to_verilog --path $(.FOUT) --filename $(.TOPE_V) --clock $(.CLK) $(.RST_NEG)

# ********************************************************************
# Clean
# ********************************************************************
clean:
	@rm -rf $(.FOUT)/
	@find . | grep -E "(\.vcd|\.v)" | xargs rm -rf

distclean: clean
	@find . | grep -E "(__pycache__|\.pyc|\.pyo|\.cache)" | xargs rm -rf
