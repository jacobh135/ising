module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/feeder.fst");
    $dumpvars(0, feeder);
end
endmodule
