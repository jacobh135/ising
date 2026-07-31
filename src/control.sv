import ising_pkg::*;

module control (
    input wire clk, rst_b,

    input wire run,

    input wire updater_done,

    output reg next_color,
    output reg signed [BETA_W-1:0] b,

    output reg ising_done
);
    reg [COLOR_COUNT_W-1:0] color_count;
    reg [ROUND_COUNT_W-1:0] round_count;

    always @(posedge clk, negedge rst_b) begin
        if (~rst_b) begin
            color_count <= 0;
            round_count <= 0;
            b <= 0;
            next_color <= 0;
            ising_done <= 1;
        end
        else if (run && ising_done) begin
            next_color <= 1;
            ising_done <= 0;
        end
        else begin
            if (updater_done && ~next_color && ~ising_done) begin
                if (color_count < PBITS_PER_PLU_MAX-1) begin
                    color_count <= color_count + 1;
                    round_count <= round_count;
                    b <= b;
                    next_color <= 1;
                end
                else begin
                    color_count <= 0;
                    round_count <= round_count + 1;

                    if (b == 0) begin
                        b <= BETA_HOT;
                    end
                    else begin
                        if (round_count[BETA_SIGNAL-1:0] == 0) begin
                            b <= b + 1;
                        end
                    end

                    if (round_count >= ROUND_COUNT) begin
                        next_color <= 0;
                        ising_done <= 1;
                    end
                    else begin
                        next_color <= 1;
                    end
                end
            end
            else begin
                next_color <= 0;
            end
        end
    end

endmodule