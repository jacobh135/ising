import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer

@cocotb.test()
async def test_demux(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    dut.enable.value = 1
    dut.mem_sel.value = 0
    dut.unit_sel.value = 3
    dut.address.value = 17
    dut.data.value = 27

    await Timer(1, unit="ns")

    assert dut.indices_wenable.value == 8
    assert dut.terms_wenable.value == 0
    assert dut.waddress.value == 17
    assert dut.wdata.value == 27

    dut.enable.value = 0
    dut.mem_sel.value = 1
    dut.unit_sel.value = 7
    dut.address.value = 8
    dut.data.value = 9

    await Timer(1, unit="ns")

    assert dut.indices_wenable.value == 0
    assert dut.indices_wenable.value == 0
    assert dut.waddress.value == 8
    assert dut.wdata.value == 9

    dut.enable.value = 1
    dut.mem_sel.value = 1
    dut.unit_sel.value = 0
    dut.address.value = 18
    dut.data.value = 19

    await Timer(1, unit="ns")

    assert dut.indices_wenable.value == 0
    assert dut.terms_wenable.value == 1
    assert dut.waddress.value == 18
    assert dut.wdata.value == 19