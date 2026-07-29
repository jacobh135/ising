SIM ?= icarus
TOPLEVEL_LANG ?= verilog
WAVES = 1

VERILOG_SOURCES = $(PWD)/../src/ising_pkg.sv
VERILOG_SOURCES += $(PWD)/../src/feeder.sv
VERILOG_SOURCES += $(PWD)/../src/plu.sv
VERILOG_SOURCES += $(PWD)/../src/mac.sv
VERILOG_SOURCES += $(PWD)/../src/lut.sv
VERILOG_SOURCES += $(PWD)/../src/lfsr.sv
VERILOG_SOURCES += $(PWD)/../src/comparator.sv
VERILOG_SOURCES += $(PWD)/../src/updater.sv
VERILOG_SOURCES += $(PWD)/../src/control.sv

TOPLEVEL = control
MODULE = test_control

COMPILE_ARGS += -Pplu.SEED=32\'h12345678

include $(shell cocotb-config --makefiles)/Makefile.sim