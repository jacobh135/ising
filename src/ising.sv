import ising_pkg::*;

module ising (
    input wire clk, rst_b,

    input wire load_enable,
    input wire load_mem_sel,
    input wire [PLU_INDEX_W-1:0] load_unit_sel,
    input wire [WADDRESS_W-1:0] load_address,
    input wire [WDATA_W-1:0] load_data,

    input wire run,

    output wire ising_done,
    output wire [PBIT_NUM_MAX-1:0] spins
);
    wire next_color;
    wire signed [BETA_W-1:0] b;
    wire updater_done;

    wire [PLU_COUNT-1:0] indices_wenable;
    wire [PLU_COUNT-1:0] terms_wenable;
    wire [WADDRESS_W-1:0] waddress;
    wire [WDATA_W-1:0] wdata;

    wire [PLU_COUNT-1:0] pbit_valid;
    wire [PLU_COUNT-1:0][PBIT_INDEX_W-1:0] pbit_i_index;

    wire [PLU_COUNT-1:0][1:0] term_type;
    wire signed [PLU_COUNT-1:0][TERM_WEIGHT_W-1:0] term_weight;
    wire [PLU_COUNT-1:0] term_spin_j, term_spin_k;
    wire [PLU_COUNT-1:0] fetch_done;

    wire [PLU_COUNT-1:0] spin_i;
    wire [PLU_COUNT-1:0] plu_done;

    control con (
        .clk(clk), .rst_b(rst_b),
        .run(run),
        .updater_done(updater_done),
        .next_color(next_color),
        .b(b),
        .ising_done(ising_done)
    );

    demux dmx (
        .clk(clk),
        .enable(load_enable),
        .mem_sel(load_mem_sel),
        .unit_sel(load_unit_sel),
        .address(load_address),
        .data(load_data),
        .indices_wenable(indices_wenable),
        .terms_wenable(terms_wenable),
        .waddress(waddress),
        .wdata(wdata)
    );

    genvar i;
    generate
        for (i = 0; i < PLU_COUNT; i = i + 1) begin : lane
            feeder feed (
                .clk(clk), .rst_b(rst_b),
                .next_color(next_color),
                .spins(spins),
                .ising_done(ising_done),

                .indices_wenable(indices_wenable[i]),
                .indices_waddress(waddress[INDEX_W-1:0]),
                .indices_wdata(wdata[INDEX_STRING_W-1:0]),

                .terms_wenable(terms_wenable[i]),
                .terms_waddress(waddress[PBIT_PROFILE_ADDRESS_W-1:0]),
                .terms_wdata(wdata[TERM_STRING_W-1:0]),

                .pbit_valid(pbit_valid[i]),
                .pbit_i_index(pbit_i_index[i]),

                .term_type(term_type[i]),
                .term_weight(term_weight[i]),
                .term_spin_j(term_spin_j[i]),
                .term_spin_k(term_spin_k[i]),

                .fetch_done(fetch_done[i])
            );

            plu #(.SEED(32'h12345678 + (i * 32'h9E3779B9))) p (
                .term_spin_j(term_spin_j[i]),
                .term_spin_k(term_spin_k[i]),
                .fetch_done(fetch_done[i]),
                .next_color(next_color),
                .clk(clk), .rst_b(rst_b),
                .term_type(term_type[i]),
                .term_weight(term_weight[i]),
                .b(b),
                .spin_i(spin_i[i]),
                .plu_done(plu_done[i])
            );
        end
    endgenerate

    updater upd (
        .next_color(next_color),
        .clk(clk), .rst_b(rst_b),
        .pbit_valid(pbit_valid),
        .plu_done(plu_done),
        .spin_i(spin_i),
        .pbit_i_index(pbit_i_index),
        .updater_done(updater_done),
        .spins(spins)
    );

endmodule
