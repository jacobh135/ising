module lfsr (
    input wire clk, rst_b, 
    output reg [11:0] rnd
);
    parameter seed = 32'b10010101010001010110110101010110;
    integer i;

    reg [31:0] lfsr_s, temp_s;
    reg [11:0] temp_n;
    
    always @(posedge clk, negedge rst_b) begin
        if (~rst_b) begin
            lfsr_s <= seed;
        end
        else begin
            temp_s = lfsr_s;
            for (i = 0; i < 12; i = i + 1) begin
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