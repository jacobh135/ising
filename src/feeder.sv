import ising_pkg::*;

module feeder (
    input wire next_color, clk, rst_b,
    input wire [PBIT_NUM_MAX-1:0] spins,
    output reg pbit_valid, term_spin_j, term_spin_k, fetch_done,
    output reg [1:0] term_type,
    output reg [PBIT_INDEX_W-1:0] pbit_i_index,
    output reg signed [TERM_WEIGHT_W-1:0] term_weight
);
    reg [INDEX_STRING_W-1:0] indices [0:PBITS_PER_PLU_MAX-1];
    reg [INDEX_STRING_W-1:0] next_index_string;
    reg [INDEX_W-1:0] pbit_current;

    reg [PBIT_PROFILE_ADDRESS_W-1:0] pbit_profile_address;
    reg [PBIT_TERM_COUNT_W-1:0] pbit_term_count;

    reg next_pbit_valid;
    reg [PBIT_INDEX_W-1:0] next_pbit_i_index;
    reg [PBIT_PROFILE_ADDRESS_W-1:0] next_pbit_profile_address;
    reg [PBIT_TERM_COUNT_W-1:0] next_pbit_term_count;

    reg [TERM_STRING_W-1:0] terms [0:TERM_TOTAL_MAX-1];
    reg [TERM_STRING_W-1:0] term_string;
    reg [PBIT_TERM_COUNT_W-1:0] term_current;

    reg [PBIT_INDEX_W-1:0] term_pbit_j_index;
    reg [PBIT_INDEX_W-1:0] term_pbit_k_index;

    initial begin
        $readmemh("indices.hex", indices);
        $readmemh("terms.hex", terms);
    end

    always @(*) begin
        next_pbit_valid = next_index_string[PBIT_TERM_COUNT_W + PBIT_PROFILE_ADDRESS_W + PBIT_INDEX_W +: 1];
        next_pbit_i_index = next_index_string[PBIT_TERM_COUNT_W + PBIT_PROFILE_ADDRESS_W +: PBIT_INDEX_W];
        next_pbit_profile_address = next_index_string[PBIT_TERM_COUNT_W +: PBIT_PROFILE_ADDRESS_W];
        next_pbit_term_count = next_index_string[0 +: PBIT_TERM_COUNT_W];

        term_type = term_string[PBIT_INDEX_W + PBIT_INDEX_W + TERM_WEIGHT_W +: 2];
        term_weight = term_string[PBIT_INDEX_W + PBIT_INDEX_W +: TERM_WEIGHT_W];
        term_pbit_j_index = term_string[PBIT_INDEX_W +: PBIT_INDEX_W];
        term_pbit_k_index = term_string[0 +: PBIT_INDEX_W];

        term_spin_j = spins[term_pbit_j_index];
        term_spin_k = spins[term_pbit_k_index];
    end
    
    always @(posedge clk, negedge rst_b) begin
        if (~rst_b) begin
            next_index_string <= indices[0];
            pbit_current <= PBITS_PER_PLU-1;

            pbit_valid <= 0;
            pbit_i_index <= 0;
            pbit_profile_address <= 0;
            pbit_term_count <= 0;

            term_string <= 0;
            term_current <= 0;

            fetch_done <= 1;
        end
        else if (next_color) begin
            if (pbit_current < PBITS_PER_PLU-2) begin
                next_index_string <= indices[pbit_current + 2];
                pbit_current <= pbit_current + 1;
            end
            else if (pbit_current < PBITS_PER_PLU-1) begin
                next_index_string <= indices[0];
                pbit_current <= pbit_current + 1;
            end
            else begin
                next_index_string <= indices[1];
                pbit_current <= 0;
            end

            pbit_valid <= next_pbit_valid;
            pbit_i_index <= next_pbit_i_index;
            pbit_profile_address <= next_pbit_profile_address;
            pbit_term_count <= next_pbit_term_count;

            term_string <= terms[next_pbit_profile_address];
            term_current <= 0;

            fetch_done <= ~next_pbit_valid;
        end
        else begin
            if (~fetch_done) begin
                if (term_current < pbit_term_count-2) begin
                    term_string <= terms[pbit_profile_address + term_current + 1];
                    term_current <= term_current + 1;

                    fetch_done <= 0;
                end
                else begin
                    term_string <= terms[pbit_profile_address + term_current + 1];
                    term_current <= term_current + 1;

                    fetch_done <= 1;
                end
            end
        end

    end

endmodule