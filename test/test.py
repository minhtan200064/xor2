# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    dut.ena.value = 1
    dut.rst_n.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    await ClockCycles(dut.clk, 5)

    dut.rst_n.value = 1

    # 00 -> 0
    dut.ui_in.value = 0b00000000
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value.integer == 0

    # 01 -> 1
    dut.ui_in.value = 0b00000010
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value.integer == 1

    # 10 -> 1
    dut.ui_in.value = 0b00000001
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value.integer == 1

    # 11 -> 0
    dut.ui_in.value = 0b00000011
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value.integer == 0
