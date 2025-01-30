// ALU Module
module ALU(
    input wire [3:0] A,
    input wire [3:0] B,
    input wire [3:0] opcode,
    output reg [3:0] result,
    output wire zero_flag
);
    // Opcodes (this matches cpu instruction set code)
    localparam ADD  = 4'b0001;
    localparam SUB  = 4'b0010;
    localparam AND  = 4'b0011;
    localparam OR   = 4'b0100;
    localparam XOR  = 4'b0101;
    localparam NOT  = 4'b0110;
    localparam SHIFT_L = 4'b0111;
    localparam SHIFT_R = 4'b1000;

    always @(*) begin
        case (opcode)
            ADD:    result <= A + B;
            SUB:    result <= A - B;
            AND:    result <= A & B;
            OR:     result <= A | B;
            XOR:    result <= A ^ B;
            NOT:    result <= ~A;
            SHIFT_L:result <= A << 1;
            SHIFT_R:result <= A >> 1;
        endcase
    end

    assign zero_flag = (result == 4'b0);
endmodule

// CPU Module