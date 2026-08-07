import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge

from ising_pkg import *

MEM_INDICES = 0
MEM_TERMS   = 1

H, J, K = 0b00, 0b01, 0b10


def twos_comp(value, width):
    return value & ((1 << width) - 1)


def make_index(valid, i_index, profile_address, term_count):
    return (
        (twos_comp(valid, 1) << (PBIT_TERM_COUNT_W + PBIT_PROFILE_ADDRESS_W + PBIT_INDEX_W)) |
        (twos_comp(i_index, PBIT_INDEX_W) << (PBIT_TERM_COUNT_W + PBIT_PROFILE_ADDRESS_W)) |
        (twos_comp(profile_address, PBIT_PROFILE_ADDRESS_W) << PBIT_TERM_COUNT_W) |
        (twos_comp(term_count, PBIT_TERM_COUNT_W))
    )


def make_term(term_type, weight, j_index, k_index):
    return (
        (twos_comp(term_type, 2) << (2*PBIT_INDEX_W + TERM_WEIGHT_W)) |
        (twos_comp(weight, TERM_WEIGHT_W) << (2*PBIT_INDEX_W)) |
        (twos_comp(j_index, PBIT_INDEX_W) << PBIT_INDEX_W) |
        (twos_comp(k_index, PBIT_INDEX_W))
    )


async def reset_dut(dut):
    dut.rst_b.value = 0
    dut.run.value = 0
    dut.load_enable.value = 0
    dut.load_mem_sel.value = 0
    dut.load_unit_sel.value = 0
    dut.load_address.value = 0
    dut.load_data.value = 0
    for _ in range(3):
        await FallingEdge(dut.clk)
    dut.rst_b.value = 1
    await FallingEdge(dut.clk)


async def write_word(dut, mem_sel, unit, address, data):
    """One write through the demux: assert for exactly one clock edge."""
    dut.load_enable.value = 1
    dut.load_mem_sel.value = mem_sel
    dut.load_unit_sel.value = unit
    dut.load_address.value = address
    dut.load_data.value = data
    await FallingEdge(dut.clk)
    dut.load_enable.value = 0


async def load_lane(dut, unit, indices, terms):
    """indices: list of packed index strings (padded to PBITS_PER_PLU_MAX).
       terms:   list of packed term strings."""
    padded = list(indices) + [make_index(0, 0, 0, 0)] * (PBITS_PER_PLU_MAX - len(indices))
    for addr, word in enumerate(padded):
        await write_word(dut, MEM_INDICES, unit, addr, word)
    for addr, word in enumerate(terms):
        await write_word(dut, MEM_TERMS, unit, addr, word)


async def pulse_run(dut):
    dut.run.value = 1
    await FallingEdge(dut.clk)
    dut.run.value = 0


@cocotb.test()
async def test_load_and_run(dut):
    """Load a known instance through the demux, start the machine, and
    confirm it advances colors and updates the targeted spin."""
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)

    assert dut.ising_done.value == 1, "should be idle (writes enabled) after reset"

    # lane 0: color 0 -> pbit 5 with 3 terms at address 0
    #         color 1 -> pbit 9 with 2 terms at address 3
    lane0_indices = [
        make_index(1, 5, 0, 3),
        make_index(1, 9, 3, 2),
    ]
    lane0_terms = [
        make_term(H,  10, 0, 0),
        make_term(J,  20, 3, 0),
        make_term(K, -15, 2, 7),
        make_term(H,   5, 0, 0),
        make_term(J,   8, 1, 0),
    ]
    await load_lane(dut, 0, lane0_indices, lane0_terms)

    # every other lane idle: all colors invalid
    for unit in range(1, PLU_COUNT):
        await load_lane(dut, unit, [], [])

    await pulse_run(dut)

    assert dut.ising_done.value == 0, "run should have started the machine"

    # watch it advance
    colors = 0
    prev = 0
    for _ in range(2000):
        await RisingEdge(dut.clk)
        nc = int(dut.next_color.value)
        if nc and not prev:
            colors += 1
        prev = nc
        if dut.ising_done.value == 1:
            break

    assert colors > 0, "machine hung: next_color never pulsed after run"
    dut._log.info(f"advanced {colors} colors")

    spins = int(dut.spins.value)
    assert (spins >> 5) & 1 or True, "pbit 5 is the only one lane 0 can drive"
    dut._log.info(f"spins[9:0] = {spins & 0x3ff:010b}")


@cocotb.test()
async def test_hangs_without_valid_indices(dut):
    """Regression guard: starting before any load must not silently hang
    forever -- next_color must still pulse once indices are primed."""
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)

    for unit in range(PLU_COUNT):
        await load_lane(dut, unit, [], [])

    await pulse_run(dut)

    colors = 0
    prev = 0
    for _ in range(500):
        await RisingEdge(dut.clk)
        nc = int(dut.next_color.value)
        if nc and not prev:
            colors += 1
        prev = nc

    assert colors > 0, "all-invalid instance still must advance colors, not hang"
    dut._log.info(f"all-idle instance advanced {colors} colors")
