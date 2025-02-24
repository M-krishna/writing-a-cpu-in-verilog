module alu(
    input wire [7:0] operand_A,
    input wire [7:0] operand_B,
    input wire [2:0] alu_control, // this is the operator(AND, SUB, AND, OR,... and so on)
    output reg [7:0] result
);

    localparam ADD      = 3'b001;
    localparam SUB      = 3'b010;
    localparam AND      = 3'b011;
    localparam OR       = 3'b100;
    localparam XOR      = 3'b101;

    always @(*) begin
        case (alu_control)
            ADD:        result <= operand_A + operand_B;
            SUB:        result <= operand_A - operand_B;
            AND:        result <= operand_A & operand_B;
            OR:         result <= operand_A | operand_B;
            XOR:        result <= operand_A ^ operand_B;
            default:    result <= 8'b0; 
        endcase
    end
endmodule