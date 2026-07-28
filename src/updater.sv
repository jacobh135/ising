import ising_pkg::*;

module updater (
    input wire next_color, clk, rst_b,
    input wire [PLU_COUNT-1:0] pbit_valid, plu_done, spin_i, 
    input wire [PLU_COUNT-1:0][PBIT_INDEX_W-1:0] pbit_i_index,
    output wire updater_done,
    output reg [PBIT_NUM_MAX-1:0] spins
);
    reg [PLU_COUNT-1:0] updated;

    assign updater_done = &updated;

    always @(posedge clk, negedge rst_b) begin
        if (~rst_b) begin
            updated <= 0;
            spins <= 0;
        end
        else if (next_color) begin
            updated <= 0;
        end
        else begin
            for (int i = 0; i < PLU_COUNT; i = i + 1) begin
                if (plu_done[i] && ~updated[i]) begin
                    updated[i] <= 1;
                    if (pbit_valid[i]) begin
                        spins[pbit_i_index[i]] <= spin_i[i];
                    end
                end
            end
        end
    end

endmodule