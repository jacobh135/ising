import ising_pkg::*;

module lut (
    input wire signed [SUM_W-1:0] i_i,
    input wire signed [BETA_W-1:0] b,
    input wire mac_done,
    input wire next_color, clk, rst_b,
    output reg [PROBABILITY_W-1:0] p_1,
    output reg lut_done
);
    wire signed [LUT_PRODUCT_W-1:0] product;
    wire signed [LUT_SCALED_W-1:0] scaled;
    wire signed [LUT_INPUT_W-1:0] tanh_input;
    wire [LUT_ADDR_W-1:0] addr;
    reg [PROBABILITY_W-1:0] lut [0:LUT_DEPTH-1];
    
    initial begin
        $readmemh("lut.hex", lut);
    end

    assign product = i_i * b;
    assign scaled = (product + LUT_ROUND) >>> LUT_SHIFT;
    assign tanh_input = (scaled > LUT_CLAMP_HIGH) ? LUT_CLAMP_HIGH : ((scaled < LUT_CLAMP_LOW) ? LUT_CLAMP_LOW : $signed(scaled[8:0]));
    assign addr = {~tanh_input[LUT_BIAS], tanh_input[LUT_BIAS-1:0]};

    always @(posedge clk, negedge rst_b) begin
        if (~rst_b) begin
            p_1 <= 0;
            lut_done <= 0;
        end
        else if (next_color) begin
            p_1 <= 0;
            lut_done <= 0;
        end
        else begin
            if (mac_done) begin
                p_1 <= lut[addr];
                lut_done <= 1;
            end
        end
    end

endmodule
