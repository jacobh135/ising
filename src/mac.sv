import ising_pkg::*;

module mac (
    input wire term_spin_j, term_spin_k, fetch_done, next_color, clk, rst_b,
    input wire [1:0] term_type,
    input wire signed [TERM_WEIGHT_W-1:0] term_weight,
    output reg signed [SUM_W-1:0] sum,
    output reg mac_done
);
    localparam H = 2'b00;
    localparam J = 2'b01;
    localparam K = 2'b10;

    always @(posedge clk, negedge rst_b) begin
        if (~rst_b) begin
            sum <= 0;
            mac_done <= 0;
        end
        else if (next_color) begin
            sum <= 0;
            mac_done <= 0;
        end
        else begin
            if (~mac_done) begin
                case (term_type)
                    H: sum <= sum + term_weight;
                    J:
                        if (term_spin_j)
                            sum <= sum + term_weight;
                        else
                            sum <= sum - term_weight;
                    K:
                        if (term_spin_j ~^ term_spin_k)
                            sum <= sum + term_weight;
                        else
                            sum <= sum - term_weight;
                    default: sum <= sum;
                endcase
                if (fetch_done) begin
                    mac_done <= 1;
                end
            end
        end
    end

endmodule
