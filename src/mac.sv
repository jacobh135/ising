module mac (
    input wire s_j, s_k, fetch_done, next_pb, clk, rst_b,
    input wire [1:0] kjh,
    input wire signed [7:0] k_ijk, j_ij, h_i,
    output reg signed [15:0] i_i,
    output reg mac_done
);
    parameter h = 2'b00;
    parameter j = 2'b01;
    parameter k = 2'b10;

    always @(posedge clk, negedge rst_b) begin
        if (~rst_b) begin
            i_i <= 0;
            mac_done <= 0;
        end
        else if (next_pb) begin
            i_i <= 0;
            mac_done <= 0;
        end
        else begin
            if (~mac_done) begin
                case (kjh)
                    h: i_i <= i_i + h_i;
                    j:
                        if (s_j)
                            i_i <= i_i + j_ij;
                        else
                            i_i <= i_i - j_ij;
                    k:
                        if (s_j ~^ s_k)
                            i_i <= i_i + k_ijk;
                        else
                            i_i <= i_i - k_ijk;
                    default: i_i <= 16'bx; // should never happen
                endcase
            end
            if (fetch_done) begin
                mac_done <= 1;
            end
        end
    end

endmodule
