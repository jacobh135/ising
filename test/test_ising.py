import cocotb, random
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

async def update(dut):
    for i in range(4):
        dut.updater_done.value = 0
        await FallingEdge(dut.clk)

    while (random.randint(0, 10) != 0):
        dut.updater_done.value = 0
        await FallingEdge(dut.clk)
        assert dut.next_color.value == 0, f"Expected next_color={0}, got next_color={dut.next_color.value}"

    dut.updater_done.value = 1

    await FallingEdge(dut.clk)
    if (not dut.ising_done.value):
        assert dut.next_color.value == 1, f"Expected next_color={1}, got next_color={dut.next_color.value}"
    else:
        assert dut.next_color.value == 0, f"Expected next_color={0}, got next_color={dut.next_color.value}"
        
    await FallingEdge(dut.clk)
    assert dut.next_color.value == 0, f"Expected next_color={0}, got next_color={dut.next_color.value}"

async def reset_dut(dut):
    dut.rst_b.value = 0
    await FallingEdge(dut.clk)
    dut.rst_b.value = 1

@cocotb.test()
async def test_comparator(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)
    dut.run.value = 1

    for i in range(1000):
        await update(dut)