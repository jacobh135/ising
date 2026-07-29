import cocotb
import random
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from ising_pkg import *

async def reset_dut(dut):
    dut.rst_b.value = 0
    await FallingEdge(dut.clk)
    dut.rst_b.value = 1

@cocotb.test()
async def test_control(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)

    for i in range(4):
        dut.updater_done.value = 0
        await FallingEdge(dut.clk)

    dut.updater_done.value = 1
    await FallingEdge(dut.clk)

    for i in range(4):
        for i in range(4):
            dut.updater_done.value = 0
            await FallingEdge(dut.clk)

        while (random.randint(0, 10) != 0):
            dut.updater_done.value = 0
            await FallingEdge(dut.clk)
            assert dut.next_color.value == 0

        dut.updater_done.value = 1
        await FallingEdge(dut.clk)

        assert dut.b.value == 0
        assert dut.next_color.value == 1

    b = 614

    for i in range(ROUND_COUNT):

        if (i % 4):
            b += 1
        
        for j in range(PBITS_PER_PLU):

            for i in range(4):
                dut.updater_done.value = 0
                await FallingEdge(dut.clk)

            while (random.randint(0, 10) != 0):
                dut.updater_done.value = 0
                await FallingEdge(dut.clk)
                assert dut.next_color.value == 0
    
            dut.updater_done.value = 1
            await FallingEdge(dut.clk)

            assert dut.b.value == b
            assert dut.next_color.value == 1
            assert dut.ising_done.value == 0

    assert dut.ising_done.value == 1