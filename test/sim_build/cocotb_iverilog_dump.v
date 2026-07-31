module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/demux.fst");
    $dumpvars(0, demux);
end
endmodule
