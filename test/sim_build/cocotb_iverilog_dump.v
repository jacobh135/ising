module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/ising.fst");
    $dumpvars(0, ising);
end
endmodule
