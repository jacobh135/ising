import ising_pkg::*;

module feeder (
    input wire next_color, clk, rst_b,
    input wire [PBIT_NUM_MAX-1:0] spins,
    output reg term_spin_j, term_spin_k, fetch_done, pbit_valid,
    output reg [1:0] term_type,
    output reg signed [TERM_WEIGHT_W-1:0] term_weight,
    output reg [PBIT_INDEX_W-1:0] pbit_i_index
);
    reg next_pbit_valid;
    reg [INDEX_W-1:0] pbit_current;
    reg [PBIT_TERM_COUNT_W-1:0] term_current;
    reg [INDEX_STRING_W-1:0] indices [0:PBITS_PER_PLU_MAX-1];
    reg [TERM_STRING_W-1:0] terms [0:TERM_TOTAL_MAX-1];
    reg [INDEX_STRING_W-1:0] index_string, next_index_string;
    reg [TERM_STRING_W-1:0] term_string;

    reg [PBIT_TERM_COUNT_W-1:0] pbit_term_count;
    reg [PBIT_PROFILE_ADDRESS_W-1:0] pbit_profile_address, next_pbit_profile_address;

    reg [PBIT_INDEX_W-1:0] term_pbit_j_index, term_pbit_k_index;

    initial begin
        $readmemh("indices.hex", indices);
        $readmemh("terms.hex", terms);
    end
    
    always @(*) begin
        if (pbit_current >= PBITS_PER_PLU-1) begin
            next_index_string = indices[0];
        end
        else begin
            next_index_string = indices[pbit_current + 1];
        end

        next_pbit_valid = next_index_string[PBIT_TERM_COUNT_W + PBIT_PROFILE_ADDRESS_W + PBIT_INDEX_W +: 1];
        next_pbit_profile_address = next_index_string[PBIT_TERM_COUNT_W +: PBIT_PROFILE_ADDRESS_W];

        index_string = indices[pbit_current];

        pbit_i_index = index_string[PBIT_TERM_COUNT_W + PBIT_PROFILE_ADDRESS_W +: PBIT_INDEX_W];
        pbit_profile_address = index_string[PBIT_TERM_COUNT_W +: PBIT_PROFILE_ADDRESS_W];
        pbit_term_count = index_string[0 +: PBIT_TERM_COUNT_W];

        term_type = term_string[PBIT_INDEX_W + PBIT_INDEX_W + TERM_WEIGHT_W +: 2];
        term_weight = term_string[PBIT_INDEX_W + PBIT_INDEX_W +: TERM_WEIGHT_W];
        term_pbit_j_index = term_string[PBIT_INDEX_W +: PBIT_INDEX_W];
        term_pbit_k_index = term_string[0 +: PBIT_INDEX_W];

        term_spin_j = spins[term_pbit_j_index];
        term_spin_k = spins[term_pbit_k_index];
    end

    always @(posedge clk, negedge rst_b) begin
        if (~rst_b) begin
            pbit_current <= PBITS_PER_PLU-1;
            term_current <= 0;
            term_string <= terms[0];
            fetch_done <= 1;
            pbit_valid <= 0;
        end
        else if (next_color) begin
            if (pbit_current >= PBITS_PER_PLU-1) begin
                pbit_current <= 0;
            end
            else begin
                pbit_current <= pbit_current + 1;
            end
            term_current <= 0;
            term_string <= terms[next_pbit_profile_address];
            fetch_done <= ~next_pbit_valid;
            pbit_valid <= next_pbit_valid;
        end
        else begin
            if (~fetch_done) begin
                if (term_current+1 >= pbit_term_count) begin
                    term_string <= term_string;
                    term_current <= term_current;
                    fetch_done <= 1;
                end
                else begin
                    term_string <= terms[pbit_profile_address + term_current + 1];
                    term_current <= term_current + 1;
                    fetch_done <= 0;
                end
            end
        end
    end


endmodule