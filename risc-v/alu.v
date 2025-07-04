module alu(
    input [31:0] A,
    input [31:0] B,
    input [1:0] op,
    output reg [31:0] out
);
    // OPERATIONS
    localparam ADD = 2'b00;
    localparam SUB = 2'b01;
    localparam AND = 2'b10;
    localparam OR = 2'b11;

    // the four operations are ADD, SUB, AND, OR
    always @(*) begin
        case (op)
            ADD: out <= A + B;
            SUB: out <= A - B;
            AND: out <= A & B;
            OR: out <= A | B;
        endcase
    end
endmodule