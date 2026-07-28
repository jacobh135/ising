import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from ising_pkg import *

def set_value(state, index, value):
    if (value):
        state = state | (1 << index)
    else:
        state = state & (~(1 << index))
    return state

def set_i_index(state, index, i_index):
    state = state & (~(((2**PBIT_INDEX_W)-1) << (index*PBIT_INDEX_W)))
    state = state | (i_index << (index*PBIT_INDEX_W))
    return state

async def send_update(dut, next_color=0, pbit_valid=0, plu_done=0, spin_i=0, pbit_i_index=0, spins=0):
    dut.next_color.value = next_color
    dut.pbit_valid.value = pbit_valid
    dut.plu_done.value = plu_done
    dut.pbit_i_index.value = pbit_i_index
    dut.spin_i.value = spin_i

    await FallingEdge(dut.clk)

    new_spins = spins
    for i in range(PLU_COUNT):
        pbit_valid_bit = (pbit_valid >> i) & 1
        plu_done_bit = (plu_done >> i) & 1
        spin_i_bit = (spin_i >> i) & 1
        pbit_i_index_bit = (pbit_i_index >> i*PBIT_INDEX_W) & ((2**PBIT_INDEX_W)-1)

        if ((not next_color) and pbit_valid_bit and plu_done_bit):
            new_spins = set_value(new_spins, pbit_i_index_bit, spin_i_bit)

    return new_spins

async def reset_dut(dut):
    dut.rst_b.value = 0
    await FallingEdge(dut.clk)
    dut.rst_b.value = 1

@cocotb.test()
async def test_updater(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)

    pbit_valid = 0
    plu_done = 0
    spin_i = 0
    pbit_i_index = 0

    spins = 0

    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 0, 1)), plu_done=(plu_done := set_value(plu_done, 0, 1)), spin_i=(spin_i := set_value(spin_i, 0, 1)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 0, 64)), spins=spins)
    assert dut.spins.value == spins
    assert dut.updater_done.value == 0

    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 1, 1)), plu_done=(plu_done := set_value(plu_done, 1, 1)), spin_i=(spin_i := set_value(spin_i, 1, 0)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 1, 57)), spins=spins)
    assert dut.spins.value == spins
    
    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 2, 0)), plu_done=(plu_done := set_value(plu_done, 2, 1)), spin_i=(spin_i := set_value(spin_i, 2, 1)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 2, 120)), spins=spins)
    assert dut.spins.value == spins

    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 3, 1)), plu_done=(plu_done := set_value(plu_done, 3, 0)), spin_i=(spin_i := set_value(spin_i, 3, 0)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 3, 13)), spins=spins)
    assert dut.spins.value == spins

    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 3, 1)), plu_done=(plu_done := set_value(plu_done, 3, 0)), spin_i=(spin_i := set_value(spin_i, 3, 0)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 3, 13)), spins=spins)
    assert dut.spins.value == spins

    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 3, 1)), plu_done=(plu_done := set_value(plu_done, 3, 1)), spin_i=(spin_i := set_value(spin_i, 3, 1)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 3, 13)), spins=spins)
    assert dut.spins.value == spins

    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 4, 1)), plu_done=(plu_done := set_value(plu_done, 4, 1)), spin_i=(spin_i := set_value(spin_i, 4, 1)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 4, 47)), spins=spins)
    assert dut.spins.value == spins

    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 5, 0)), plu_done=(plu_done := set_value(plu_done, 5, 1)), spin_i=(spin_i := set_value(spin_i, 5, 0)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 5, 94)), spins=spins)
    assert dut.spins.value == spins

    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 6, 0)), plu_done=(plu_done := set_value(plu_done, 6, 1)), spin_i=(spin_i := set_value(spin_i, 6, 0)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 6, 23)), spins=spins)
    assert dut.spins.value == spins

    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 7, 1)), plu_done=(plu_done := set_value(plu_done, 7, 1)), spin_i=(spin_i := set_value(spin_i, 7, 0)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 7, 67)), spins=spins)
    assert dut.spins.value == spins

    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 8, 1)), plu_done=(plu_done := set_value(plu_done, 8, 1)), spin_i=(spin_i := set_value(spin_i, 8, 0)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 8, 88)), spins=spins)
    assert dut.spins.value == spins
    assert dut.updater_done.value == 0
    
    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 9, 1)), plu_done=(plu_done := set_value(plu_done, 9, 1)), spin_i=(spin_i := set_value(spin_i, 9, 1)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 9, 89)), spins=spins)
    assert dut.spins.value == spins
    assert dut.updater_done.value == 1

    dut.next_color.value = 1
    await FallingEdge(dut.clk)
    dut.next_color.value = 0

    pbit_valid = 0
    plu_done = 0
    spin_i = 0
    pbit_i_index = 0

    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 9, 1)), plu_done=(plu_done := set_value(plu_done, 9, 1)), spin_i=(spin_i := set_value(spin_i, 9, 1)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 9, 64)), spins=spins)
    assert dut.spins.value == spins
    assert dut.updater_done.value == 0

    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 8, 1)), plu_done=(plu_done := set_value(plu_done, 8, 1)), spin_i=(spin_i := set_value(spin_i, 8, 0)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 8, 57)), spins=spins)
    assert dut.spins.value == spins
    
    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 7, 0)), plu_done=(plu_done := set_value(plu_done, 7, 1)), spin_i=(spin_i := set_value(spin_i, 7, 1)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 7, 120)), spins=spins)
    assert dut.spins.value == spins

    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 6, 1)), plu_done=(plu_done := set_value(plu_done, 6, 0)), spin_i=(spin_i := set_value(spin_i, 6, 0)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 6, 13)), spins=spins)
    assert dut.spins.value == spins

    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 6, 1)), plu_done=(plu_done := set_value(plu_done, 6, 0)), spin_i=(spin_i := set_value(spin_i, 6, 0)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 6, 13)), spins=spins)
    assert dut.spins.value == spins

    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 6, 1)), plu_done=(plu_done := set_value(plu_done, 6, 1)), spin_i=(spin_i := set_value(spin_i, 6, 1)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 6, 13)), spins=spins)
    assert dut.spins.value == spins

    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 5, 1)), plu_done=(plu_done := set_value(plu_done, 5, 1)), spin_i=(spin_i := set_value(spin_i, 5, 1)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 5, 47)), spins=spins)
    assert dut.spins.value == spins

    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 4, 0)), plu_done=(plu_done := set_value(plu_done, 4, 1)), spin_i=(spin_i := set_value(spin_i, 4, 0)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 4, 94)), spins=spins)
    assert dut.spins.value == spins

    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 3, 0)), plu_done=(plu_done := set_value(plu_done, 3, 1)), spin_i=(spin_i := set_value(spin_i, 3, 0)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 3, 23)), spins=spins)
    assert dut.spins.value == spins

    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 2, 1)), plu_done=(plu_done := set_value(plu_done, 2, 1)), spin_i=(spin_i := set_value(spin_i, 2, 0)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 2, 67)), spins=spins)
    assert dut.spins.value == spins

    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 1, 1)), plu_done=(plu_done := set_value(plu_done, 1, 1)), spin_i=(spin_i := set_value(spin_i, 1, 0)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 1, 88)), spins=spins)
    assert dut.spins.value == spins
    assert dut.updater_done.value == 0
    
    spins = await send_update(dut, pbit_valid=(pbit_valid := set_value(pbit_valid, 0, 1)), plu_done=(plu_done := set_value(plu_done, 0, 1)), spin_i=(spin_i := set_value(spin_i, 0, 1)), pbit_i_index=(pbit_i_index := set_i_index(pbit_i_index, 0, 89)), spins=spins)
    assert dut.spins.value == spins
    assert dut.updater_done.value == 1