module plu #(parameter [31:0] SEED = 32'd0) (
    input wire s_j, s_k, term_valid, fetch_done, next_color, clk, rst_b,
    input wire [1:0] term_type,
    input wire signed [7:0] weight,
    input wire signed [15:0] b,
    output wire s_i, plu_done
);
    wire signed [15:0] i_i;
    wire [11:0] p_1, rnd;
    wire mac_done, lut_done;

    mac plu_mac(.s_j(s_j), .s_k(s_k), .term_valid(term_valid), .fetch_done(fetch_done), .next_color(next_color), .clk(clk), .rst_b(rst_b), .term_type(term_type), .weight(weight), .i_i(i_i), .mac_done(mac_done));
    lut plu_lut(.i_i(i_i), .b(b), .mac_done(mac_done), .next_color(next_color), .clk(clk), .rst_b(rst_b), .p_1(p_1), .lut_done(lut_done));
    lfsr #(.SEED(SEED)) plu_lfsr(.clk(clk), .rst_b(rst_b), .rnd(rnd));
    comparator plu_comparator(.next_color(next_color), .lut_done(lut_done), .clk(clk), .rst_b(rst_b), .p_1(p_1), .rnd(rnd), .s_i(s_i), .comparator_done(plu_done));

endmodule