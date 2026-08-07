import ising_pkg::*;

module demux (
    input wire clk,

    input wire enable, mem_sel,
    input wire [PLU_INDEX_W-1:0] unit_sel,
    input wire [WADDRESS_W-1:0] address,
    input wire [WDATA_W-1:0] data,

    output reg [PLU_COUNT-1:0] indices_wenable,
    output reg [PLU_COUNT-1:0] terms_wenable,

    output reg [WADDRESS_W-1:0] waddress,
    output reg [WDATA_W-1:0] wdata
);
    parameter indices = 1'b0;
    parameter terms = 1'b1;

    always @(*) begin
        waddress = address;
        wdata = data;
        if (enable) begin
            indices_wenable = 0;
            terms_wenable = 0;
            if (mem_sel == indices) begin
                indices_wenable[unit_sel] = 1;
            end
            else begin
                terms_wenable[unit_sel] = 1;
            end
        end
        else begin
            indices_wenable = 0;
            terms_wenable = 0;
        end
    end
    
endmodule