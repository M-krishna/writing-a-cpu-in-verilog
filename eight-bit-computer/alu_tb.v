module alu_tb;
    // test signals
    reg [7:0] operand_A;
    reg [7:0] operand_B;
    reg [2:0] alu_control;
    wire [7:0] alu_result;

    // Module initialization
    alu _alu(
        .operand_A(operand_A),
        .operand_B(operand_B),
        .alu_control(alu_control),
        .result(alu_result)
    );

    localparam ADD      = 3'b001;
    localparam SUB      = 3'b010;
    localparam AND      = 3'b011;
    localparam OR       = 3'b100;
    localparam XOR      = 3'b101;

    initial begin
        #0 alu_control = ADD; operand_A = 8'b00000010; operand_B = 8'b00000001;
        #1 alu_control = SUB; operand_A = 8'b00000010; operand_B = 8'b00000001;
        #1 alu_control = AND; operand_A = 8'b00000010; operand_B = 8'b00000001;
        #1 alu_control = OR; operand_A = 8'b00000010; operand_B = 8'b00000001;
        #1 alu_control = XOR; operand_A = 8'b00000010; operand_B = 8'b00000001;
        #10;
        $finish;
    end

    initial begin
        $monitor("[Time=%0t] operand_A: %0d operand_b: %0d alu_control: %3b alu_result: %0d", $time, operand_A, operand_B, alu_control, alu_result);
    end

endmodule