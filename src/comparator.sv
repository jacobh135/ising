module comparator (
    input wire next_pb, lut_done, clk, rst_b,
    input wire [11:0] p_1, rnd,
    output reg spin, comparator_done
);
    always @(posedge clk, negedge rst_b) begin
        if (~rst_b) begin
            spin <= 0;
            comparator_done <= 0;
        end
        else if (next_pb) begin
            spin <= 0;
            comparator_done <= 0;
        end
        else begin
            if (lut_done) begin
                spin <= (p_1 > rnd) ? 1 : 0;
                comparator_done <= 1;
            end
        end
    end

endmodule