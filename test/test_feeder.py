import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from ising_pkg import *

async def assert_feeder(dut, pbit_valid, pbit_i_index, term_type, term_weight, term_spin_j, term_spin_k, fetch_done):
    assert dut.pbit_valid.value == pbit_valid, f"Expected pbit_valid={pbit_valid}, got pbit_valid={dut.pbit_valid.value}"
    assert dut.pbit_i_index.value == pbit_i_index, f"Expected pbit_i_index={pbit_i_index}, got pbit_i_index={dut.pbit_i_index.value}"
    assert dut.term_type.value == term_type, f"Expected term_type={term_type}, got term_type={dut.term_type.value}"
    assert dut.term_weight.value == term_weight, f"Expected term_weight={term_weight}, got term_weight={dut.term_weight.value}"
    assert dut.term_spin_j.value == term_spin_j, f"Expected term_spin_j={term_spin_j}, got term_spin_j={dut.term_spin_j.value}"
    assert dut.term_spin_k.value == term_spin_k, f"Expected term_spin_k={term_spin_k}, got term_spin_k={dut.term_spin_k.value}"
    assert dut.fetch_done.value == fetch_done, f"Expected fetch_done={fetch_done}, got fetch_done={dut.fetch_done.value}"

async def drive_feeder(dut, spins, next_color):
    dut.spins.value = spins
    dut.next_color.value = next_color

    await FallingEdge(dut.clk)

async def reset_dut(dut):
    dut.rst_b.value = 0
    await FallingEdge(dut.clk)
    dut.rst_b.value = 1

@cocotb.test()
async def test_feeder(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)

    spins = 85738190

    with open("indices.hex") as f:
        indices = [int(line, 16) for line in f if line.strip()]

    with open("terms.hex") as f:
        terms = [int(line, 16) for line in f if line.strip()]

    await drive_feeder(dut, spins, 1)

    for i in range(len(indices)):
        index_string = indices[i]
        valid = (index_string >> (PBIT_TERM_COUNT_W + PBIT_PROFILE_ADDRESS_W + PBIT_INDEX_W)) & (1)
        i_index = (index_string >> (PBIT_TERM_COUNT_W + PBIT_PROFILE_ADDRESS_W)) & ((2 ** PBIT_INDEX_W) - 1)
        profile_address = (index_string >> PBIT_TERM_COUNT_W) & ((2 ** PBIT_PROFILE_ADDRESS_W) - 1)
        term_count = index_string & ((2 ** PBIT_TERM_COUNT_W) - 1)

        if (valid):
            for j in range(term_count):
                term_string = terms[profile_address + j]
                type = (term_string >> (2*PBIT_INDEX_W + TERM_WEIGHT_W)) & 3
                weight = (term_string >> (2*PBIT_INDEX_W)) & ((2 ** TERM_WEIGHT_W) - 1)
                spin_j_index = (term_string >> PBIT_INDEX_W) & ((2 ** PBIT_INDEX_W) - 1)
                spin_k_index = term_string & ((2 ** PBIT_INDEX_W) - 1)

                spin_j = (spins >> spin_j_index) & 1
                spin_k = (spins >> spin_k_index) & 1

                fetch_done = int(j == term_count-1)

                await assert_feeder(dut, valid, i_index, type, weight, spin_j, spin_k, fetch_done)

                await drive_feeder(dut, spins, (fetch_done & 1))
        else:
            term_string = terms[profile_address]
            type = (term_string >> (2*PBIT_INDEX_W + TERM_WEIGHT_W)) & 3
            weight = (term_string >> (2*PBIT_INDEX_W)) & ((2 ** TERM_WEIGHT_W) - 1)
            spin_j_index = (term_string >> PBIT_INDEX_W) & ((2 ** PBIT_INDEX_W) - 1)
            spin_k_index = term_string & ((2 ** PBIT_INDEX_W) - 1)

            spin_j = (spins >> spin_j_index) & 1
            spin_k = (spins >> spin_k_index) & 1
            
            fetch_done = 1

            await assert_feeder(dut, valid, i_index, type, weight, spin_j, spin_k, fetch_done)

            await drive_feeder(dut, spins, (fetch_done & 1))