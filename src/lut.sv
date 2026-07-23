module lut (
    input wire signed [15:0] i_i, b,
    input wire mac_done,
    input wire next_pb, clk, rst_b,
    output reg [11:0] p_1,
    output reg lut_done
);
    wire signed [31:0] product;
    wire signed [18:0] scaled;
    wire signed [8:0] clamped;
    wire [8:0] addr;
    reg [11:0] lut [0:511];
    initial begin
        $readmemh("lut.hex", lut);
    end

    assign product = i_i * b;
    assign scaled = (product + 4096) >>> 13;
    assign clamped = (scaled > 255) ? 9'sd255 : ((scaled < -256) ? -9'sd256 : $signed(scaled[8:0]));
    assign addr = {~clamped[8], clamped[7:0]};

    always @(posedge clk, negedge rst_b) begin
        if (~rst_b) begin
            p_1 <= 0;
            lut_done <= 0;
        end
        else if (next_pb) begin
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
