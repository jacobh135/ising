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

async def feed_profile_1(dut):
    await feed_term(dut, term_spin_k=1, term_type=2, term_weight=8)
    await feed_term(dut, term_spin_j=1, term_type=1, term_weight=5)
    await feed_term(dut, fetch_done=1, term_type=0, term_weight=9)

async def feed_profile_2(dut):
    await feed_term(dut, term_spin_k=1, term_type=2, term_weight=4)
    await feed_term(dut, term_spin_j=1, term_type=1, term_weight=8)
    await feed_term(dut, fetch_done=1, term_type=0, term_weight=3)

@cocotb.test()
async def test_file(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)

    count = 0
    total = 0
    for i in range(100000):
        dut.b.value = 20480

        await feed_profile_1(dut)

        await FallingEdge(dut.clk)
        await FallingEdge(dut.clk)

        total += 1
        if (dut.spin_i.value):
            count += 1

        dut.next_color.value = 1
        await FallingEdge(dut.clk)
        dut.next_color.value = 0

    assert abs(count/total - 0.718) < 0.01, f"Expected spin_i ratio=0.718 ± 0.01, got {count/total}"

    count = 0
    total = 0
    for i in range(100000):
        dut.b.value = 2048

        await feed_profile_2(dut)

        await FallingEdge(dut.clk)
        await FallingEdge(dut.clk)

        total += 1
        if (dut.spin_i.value):
            count += 1

        dut.next_color.value = 1
        await FallingEdge(dut.clk)
        dut.next_color.value = 0

    assert abs(count/total - 0.527) < 0.01, f"Expected spin_i ratio=0.527 ± 0.01, got {count/total}"