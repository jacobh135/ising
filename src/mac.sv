import ising_pkg::*;

module mac (
    input wire s_j, s_k, term_valid, fetch_done, next_color, clk, rst_b,
    input wire [1:0] term_type,
    input wire signed [7:0] weight,
    output reg signed [15:0] i_i,
    output reg mac_done
);
    localparam H = 2'b00;
    localparam J = 2'b01;
    localparam K = 2'b10;

    always @(posedge clk, negedge rst_b) begin
        if (~rst_b) begin
            i_i <= 0;
            mac_done <= 0;
        end
        else if (next_color) begin
            i_i <= 0;
            mac_done <= 0;
        end
        else begin
            if (~mac_done && term_valid) begin
                case (term_type)
                    H: i_i <= i_i + weight;
                    J:
                        if (s_j)
                            i_i <= i_i + weight;
                        else
                            i_i <= i_i - weight;
                    K:
                        if (s_j ~^ s_k)
                            i_i <= i_i + weight;
                        else
                            i_i <= i_i - weight;
                    default: i_i <= i_i;
                endcase
            end
            if (fetch_done) begin
                mac_done <= 1;
            end
        end
    end

endmodule
