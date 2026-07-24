import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

async def reset_dut(dut):
    dut.rst_b.value = 0
    await FallingEdge(dut.clk)
    dut.rst_b.value = 1

async def feed_term(dut, s_j=0, s_k=0, term_valid=0, fetch_done=0, next_color=0, term_type=0, weight=0):
    dut.s_j.value = s_j
    dut.s_k.value = s_k
    dut.term_valid.value = term_valid
    dut.fetch_done.value = fetch_done
    dut.next_color.value = next_color
    dut.term_type.value = term_type
    dut.weight.value = weight

    await FallingEdge(dut.clk)

async def feed_profile_1(dut):
    await feed_term(dut, s_k=1, term_valid=1, term_type=2, weight=8)
    await feed_term(dut, s_j=1, term_valid=0, term_type=1, weight=10)
    await feed_term(dut, s_j=1, term_valid=1, term_type=1, weight=5)
    await feed_term(dut, term_valid=1, fetch_done=1, term_type=0, weight=9)

async def feed_profile_2(dut):
    await feed_term(dut, s_k=1, term_valid=1, term_type=2, weight=4)
    await feed_term(dut, s_j=1, term_valid=0, term_type=1, weight=9)
    await feed_term(dut, s_j=1, term_valid=1, term_type=1, weight=8)
    await feed_term(dut, term_valid=1, fetch_done=1, term_type=0, weight=3)

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
        await FallingEdge(dut.clk)

        total += 1
        if (dut.s_i.value):
            count += 1

    assert abs(count/total - 0.718) < 0.01, f"Expected s_i ratio=0.718 ± 0.01, got {count/total}"

    dut.next_color.value = 1
    await FallingEdge(dut.clk)
    dut.next_color.value = 0

    count = 0
    total = 0
    for i in range(100000):
        dut.b.value = 2048

        await feed_profile_2(dut)

        await FallingEdge(dut.clk)
        await FallingEdge(dut.clk)
        await FallingEdge(dut.clk)

        total += 1
        if (dut.s_i.value):
            count += 1

    assert abs(count/total - 0.527) < 0.01, f"Expected s_i ratio=0.527 ± 0.01, got {count/total}"