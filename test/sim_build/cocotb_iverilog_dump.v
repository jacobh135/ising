module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/plu.fst");
    $dumpvars(0, plu);
end
endmodule
