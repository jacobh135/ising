import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

async def reset_dut(dut):
    dut.rst_b.value = 0
    await FallingEdge(dut.clk)
    dut.rst_b.value = 1

@cocotb.test()
async def test_random(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)

    dut.sum.value = 64
    dut.b.value = 6144
    dut.mac_done.value = 1
    dut.next_color.value = 0
    await FallingEdge(dut.clk)

    assert dut.p_1.value == 3901, f"Expected p_1=3901, got {dut.p_1.value}"
    assert dut.lut_done.value == 1, f"Expected lut_done=1, got {dut.lut_done.value}"

@cocotb.test()
async def test_zero(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)

    dut.sum.value = -256
    dut.b.value = 8192
    dut.mac_done.value = 1
    dut.next_color.value = 0
    await FallingEdge(dut.clk)

    assert dut.p_1.value == 0, f"Expected p_1=0, got {dut.p_1.value}"
    assert dut.lut_done.value == 1, f"Expected lut_done=1, got {dut.lut_done.value}"


