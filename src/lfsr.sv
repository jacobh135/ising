import ising_pkg::*;

module lfsr #(parameter [31:0] SEED = 32'd0) (
    input wire clk, rst_b, 
    output reg [PROBABILITY_W-1:0] rnd
);
    integer i;

    reg [31:0] lfsr_s, temp_s;
    reg [PROBABILITY_W-1:0] temp_n;
    
    always @(posedge clk, negedge rst_b) begin
        if (~rst_b) begin
            lfsr_s <= SEED;
            rnd <= 12'd0;
        end
        else begin
            temp_s = lfsr_s;
            for (i = 0; i < PROBABILITY_W; i = i + 1) begin
                temp_n[i] = temp_s[0];
                if (temp_s[0] == 1) begin
                    temp_s = temp_s >> 1;
                    temp_s = temp_s ^ 32'b10000000001000000000000000000011;
                end
                else begin
                    temp_s = temp_s >> 1;
                end
            end
            lfsr_s <= temp_s;
            rnd <= temp_n;
            
        end
    end

endmodule