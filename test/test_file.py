import cocotb
from cocotb.clock import Clock
from cocotb.triggers import NextTimeStep, RisingEdge, ReadOnly

async def reset_dut(dut):
    dut.rst_b.value = 0
    await RisingEdge(dut.clk)
    dut.rst_b.value = 1

@cocotb.test()
async def test_file(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)