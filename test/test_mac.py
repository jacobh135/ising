import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

async def reset_dut(dut):
    dut.rst_b.value = 0
    await FallingEdge(dut.clk)
    dut.rst_b.value = 1

async def feed_term(dut, term_spin_j=0, term_spin_k=0, fetch_done=0, next_color=0, term_type=0, term_weight=0):
    dut.term_spin_j.value = term_spin_j
    dut.term_spin_k.value = term_spin_k
    dut.fetch_done.value = fetch_done
    dut.next_color.value = next_color
    dut.term_type.value = term_type
    dut.term_weight.value = term_weight

    await FallingEdge(dut.clk)
    
@cocotb.test()
async def test_mac(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)

    await feed_term(dut, term_spin_k=1, term_type=2, term_weight=8)

    await feed_term(dut, term_spin_j=1, term_type=1, term_weight=5)

    await feed_term(dut, fetch_done=1, term_type=0, term_weight=9)

    assert dut.sum.value.to_signed() == 6, f"Expected sum=6, got {dut.sum.value.to_signed()}"
    assert dut.mac_done.value == 1, f"Expected mac_done=1, got {dut.mac_done.value}"

    await feed_term(dut, next_color=1)

    assert dut.sum.value.to_signed() == 0, f"Expected sum=0 after next_color, got {dut.sum.value.to_signed()}"
    assert dut.mac_done.value == 0, f"Expected mac_done=0, got {dut.mac_done.value}"
