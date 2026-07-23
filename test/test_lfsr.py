import cocotb
from cocotb.clock import Clock
from cocotb.triggers import NextTimeStep, RisingEdge, ReadOnly

async def reset_dut(dut):
    dut.rst_b.value = 0
    await RisingEdge(dut.clk)
    dut.rst_b.value = 1

@cocotb.test()
async def test_reset(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)

    await ReadOnly()
    assert dut.lfsr_s.value == 2504355158, f"Expected lfsr_s=2504355158, got {dut.lfsr_s.value}"

@cocotb.test()
async def test_unique(dut):
    seen = set()

    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)

    await RisingEdge(dut.clk)

    for i in range(5000):
        await ReadOnly()
        num = int(dut.lfsr_s.value)
        assert num != 0, "Expected lfsr_s!=0, got 0"
        assert num not in seen, f"Expected unique lfsr_s, got duplicate {num}"
        seen.add(num)
        
        await NextTimeStep()
        await RisingEdge(dut.clk)
