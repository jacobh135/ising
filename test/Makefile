SIM ?= icarus
TOPLEVEL_LANG ?= verilog
WAVES = 1

VERILOG_SOURCES = $(PWD)/../src/ising_pkg.sv
VERILOG_SOURCES += $(PWD)/../src/plu.sv
VERILOG_SOURCES += $(PWD)/../src/mac.sv
VERILOG_SOURCES += $(PWD)/../src/lut.sv
VERILOG_SOURCES += $(PWD)/../src/lfsr.sv
VERILOG_SOURCES += $(PWD)/../src/comparator.sv

TOPLEVEL = plu
MODULE = test_plu

COMPILE_ARGS += -Pplu.SEED=32\'h12345678

include $(shell cocotb-config --makefiles)/Makefile.sim