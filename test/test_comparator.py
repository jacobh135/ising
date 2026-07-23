import cocotb, random
from cocotb.clock import Clock
from cocotb.triggers import NextTimeStep, RisingEdge, ReadOnly

async def reset_dut(dut):
    dut.rst_b.value = 0
    await RisingEdge(dut.clk)
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
    await RisingEdge(dut.clk)

    for i in range(500000):
        await ReadOnly()
        total += 1
        if dut.spin.value == 1:
            count += 1

        await NextTimeStep()
        dut.rnd.value = random.randint(0, 4095)
        await RisingEdge(dut.clk)

    assert abs(count/total - 0.25) < 0.01, f"Expected spin ratio=0.25 ± 0.01, got {count/total}"