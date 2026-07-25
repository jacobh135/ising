import ising_pkg::*;

module comparator (
    input wire next_color, lut_done, clk, rst_b,
    input wire [PROBABILITY_W-1:0] p_1, rnd,
    output reg s_i, comparator_done
);
    always @(posedge clk, negedge rst_b) begin
        if (~rst_b) begin
            s_i <= 0;
            comparator_done <= 0;
        end
        else if (next_color) begin
            s_i <= 0;
            comparator_done <= 0;
        end
        else begin
            if (lut_done) begin
                s_i <= (p_1 > rnd) ? 1 : 0;
                comparator_done <= 1;
            end
        end
    end

endmodule