SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES  = $(PWD)/../src/plu.v
VERILOG_SOURCES += $(PWD)/../src/mac.v
VERILOG_SOURCES += $(PWD)/../src/lut.v
VERILOG_SOURCES += $(PWD)/../src/lfsr.v
VERILOG_SOURCES += $(PWD)/../src/comparator.v

TOPLEVEL = plu
MODULE = test_plu

COMPILE_ARGS += -Pplu.SEED=32\'h12345678

include $(shell cocotb-config --makefiles)/Makefile.sim