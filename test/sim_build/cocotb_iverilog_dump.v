module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/control.fst");
    $dumpvars(0, control);
end
endmodule
