import ising_pkg::*;

module feeder (
    input wire next_color, clk, rst_b,
    output wire s_j, s_k, term_valid, fetch_done,
    output wire [1:0] term_type,
    output wire signed [WEIGHT_W-1:0] weight
);
    reg [INDEX_W-1:0] index;
    reg [INDEX_STRING_W-1:0] indices [0:COLORS_PER_ROUND-1];
    reg [TERM_STRING_W-1:0] terms [0:TERM_TOTAL_MAX-1];
    wire [INDEX_STRING_W-1:0] index_string;
    wire [TERM_STRING_W-1:0] term_string;

    initial begin
        $readmemh("indices.hex", indices);
        $readmemh("terms.hex", terms);
    end
    
    always @(*) begin
        index_string = indices[index]
        

        term_string = terms[]
    end


endmodule