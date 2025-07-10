module alu(
    input [31:0] A,
    input [31:0] B,
    input [2:0] op,
    output reg [31:0] out
);
    // OPERATIONS
    localparam ADD = 3'b000;
    localparam SLL = 3'b001;
    localparam SLT = 3'b010;
    localparam SLTU = 3'b011;
    localparam XOR = 3'b100;
    localparam SRL = 3'b101;
    localparam OR = 3'b110;
    localparam AND = 3'b111;

    // the four operations are ADD, SUB, AND, OR
    always @(*) begin   // Combinational
        case (op)
            ADD: out = A + B;
            SLL: out = A << B[4:0];
            SLT: out = ($signed(A) < $signed(B)) ? 1 : 0;
            SLTU: out = (A < B) ? 1 : 0;
            XOR: out = A ^ B;
            SRL: out = A >> B[4:0];
            OR: out = A | B;
            AND: out = A & B;
            default: out = 32'b0;
        endcase
    end
endmodule