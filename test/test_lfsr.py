import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

async def reset_dut(dut):
    dut.rst_b.value = 0
    await FallingEdge(dut.clk)
    dut.rst_b.value = 1

@cocotb.test()
async def test_reset(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)

    assert dut.lfsr_s.value == dut.SEED.value, f"Expected lfsr_s={dut.SEED.value}, got {dut.lfsr_s.value}"

@cocotb.test()
async def test_unique(dut):
    seen = set()

    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)

    await FallingEdge(dut.clk)

    for i in range(5000):
        num = int(dut.lfsr_s.value)

        assert num != 0, "Expected lfsr_s!=0, got 0"
        assert num not in seen, f"Expected unique lfsr_s, got duplicate {num}"
        
        seen.add(num)
        
        await FallingEdge(dut.clk)
