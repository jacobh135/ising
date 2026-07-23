import cocotb
from cocotb.clock import Clock
from cocotb.triggers import NextTimeStep, RisingEdge, ReadOnly

async def reset_dut(dut):
    dut.rst_b.value = 0
    await RisingEdge(dut.clk)
    dut.rst_b.value = 1

async def drive_term(dut, s_j=0, s_k=0, fetch_done=0, next_pb=0, kjh=0, k_ijk=0, j_ij=0, h_i=0):
    await NextTimeStep()  # Wait for the next simulation time step
    dut.s_j.value = s_j
    dut.s_k.value = s_k
    dut.fetch_done.value = fetch_done
    dut.next_pb.value = next_pb
    dut.kjh.value = kjh
    dut.k_ijk.value = k_ijk
    dut.j_ij.value = j_ij
    dut.h_i.value = h_i
    await RisingEdge(dut.clk)
    
    await ReadOnly()  # Ensure we read the values after they have been processed

@cocotb.test()
async def test_mac(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)

    await drive_term(dut, s_k=1, kjh=2, k_ijk=8)

    await drive_term(dut, s_j=1, kjh=1, j_ij=5)

    await drive_term(dut, fetch_done=1, kjh=0, h_i=9)

    assert dut.i_i.value.to_signed() == 6, f"Expected i_i=6, got {dut.i_i.value.to_signed()}"
    assert dut.mac_done.value == 1, f"Expected mac_done=1, got {dut.mac_done.value}"

    await drive_term(dut, next_pb=1)

    assert dut.i_i.value.to_signed() == 0, f"Expected i_i=0 after next_pb, got {dut.i_i.value.to_signed()}"
    assert dut.mac_done.value == 0, f"Expected mac_done=0, got {dut.mac_done.value}"
