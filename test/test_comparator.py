import cocotb, random
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

async def reset_dut(dut):
    dut.rst_b.value = 0
    await FallingEdge(dut.clk)
    dut.rst_b.value = 1

@cocotb.test()
async def test_comparator(dut):
    count = 0
    total = 0

    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)

    dut.lut_done.value = 1
    dut.p_1.value = 1024
    dut.rnd.value = random.randint(0, 4095)

    await FallingEdge(dut.clk)

    for i in range(500000):
        total += 1
        if dut.s_i.value == 1:
            count += 1

        dut.rnd.value = random.randint(0, 4095)
        await FallingEdge(dut.clk)

    assert abs(count/total - 0.25) < 0.01, f"Expected s_i ratio=0.25 ± 0.01, got {count/total}"