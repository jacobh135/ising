import ising_pkg::*;

module ising (
    input wire clk, rst_b,

    input wire indices_wenable,
    input wire [INDEX_W-1:0] indices_waddress,
    input wire [INDEX_STRING_W-1:0] indices_wdata,

    input wire terms_wenable,
    input wire [PBIT_PROFILE_ADDRESS_W-1:0] terms_waddress,
    input wire [TERM_STRING_W-1:0] terms_wdata,

    input wire run,

    input wire updater_done
);
    wire next_color;
    wire signed [BETA_W-1:0] b;
    wire [PBIT_NUM_MAX-1:0] spins;

    wire ising_done;

    wire pbit_valid;
    wire [PBIT_INDEX_W-1:0] pbit_i_index;

    wire [1:0] term_type;
    wire signed [TERM_WEIGHT_W-1:0] term_weight;

    wire term_spin_j, term_spin_k;

    wire fetch_done;

    control con (clk, rst_b, run, updater_done, next_color, b, ising_done);
    feeder feed (clk, rst_b, next_color, spins, ising_done, indices_wenable, indices_waddress, indices_wdata, terms_wenable, terms_waddress, terms_wdata, pbit_valid, pbit_i_index, term_type, term_weight, term_spin_j, term_spin_k, fetch_done);


endmodule