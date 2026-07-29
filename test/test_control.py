import cocotb
import random
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from ising_pkg import *

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
async def test_control(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)

    await update(dut)

    for i in range(PBITS_PER_PLU):
        assert dut.b.value == 0, f"Expected b={0}, got b={dut.b.value}"
        assert dut.ising_done.value == 0, f"Expected ising_done={0}, got ising_done={dut.ising_done.value}"

        await update(dut)

    b = 614

    for i in range(ROUND_COUNT):
        if (i % 4 == 0):
            b += 1
        
        for j in range(PBITS_PER_PLU):
            assert dut.b.value == b, f"Expected b={b}, got b={dut.b.value}"
            assert dut.ising_done.value == 0, f"Expected ising_done={0}, got ising_done={dut.ising_done.value}"

            await update(dut)

    assert dut.ising_done.value == 1, f"Expected ising_done={1}, got ising_done={dut.ising_done.value}"

    await update(dut)
    await update(dut)
    await update(dut)