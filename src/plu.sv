import ising_pkg::*;

module plu #(parameter [31:0] SEED = 32'd0) (
    input wire term_spin_j, term_spin_k, fetch_done, next_color, clk, rst_b,
    input wire [1:0] term_type,
    input wire signed [TERM_WEIGHT_W-1:0] term_weight,
    input wire signed [SUM_W-1:0] b,
    output wire spin_i, plu_done
);
    wire signed [SUM_W-1:0] sum;
    wire [PROBABILITY_W-1:0] p_1, rnd;
    wire mac_done, lut_done;

    mac plu_mac(.term_spin_j(term_spin_j), .term_spin_k(term_spin_k), .fetch_done(fetch_done), .next_color(next_color), .clk(clk), .rst_b(rst_b), .term_type(term_type), .term_weight(term_weight), .sum(sum), .mac_done(mac_done));
    lut plu_lut(.sum(sum), .b(b), .mac_done(mac_done), .next_color(next_color), .clk(clk), .rst_b(rst_b), .p_1(p_1), .lut_done(lut_done));
    lfsr #(.SEED(SEED)) plu_lfsr(.clk(clk), .rst_b(rst_b), .rnd(rnd));
    comparator plu_comparator(.next_color(next_color), .lut_done(lut_done), .clk(clk), .rst_b(rst_b), .p_1(p_1), .rnd(rnd), .spin_i(spin_i), .comparator_done(plu_done));

endmodule