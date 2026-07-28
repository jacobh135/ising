module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/updater.fst");
    $dumpvars(0, updater);
end
endmodule
