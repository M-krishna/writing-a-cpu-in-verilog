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
module cpu(
    input wire clk,
    input wire reset,
    output wire [3:0] output_data
);
    // Program counter
    reg [3:0] pc;

    // instruction memory
    reg [7:0] instruction_memory [0:15];

    // registers
    reg [3:0] register_A;
    reg [3:0] register_B;
    reg [3:0] output_register;

    // Instruction set
    localparam LOAD_A = 4'b0001;
    localparam LOAD_B = 4'b0010;
    localparam ADD    = 4'b0011;
    localparam SUB    = 4'b0100;
    localparam AND    = 4'b0101;
    localparam OR     = 4'b0110;
    localparam NOT    = 4'b0111;
    localparam SHIFT_L= 4'b1000;
    localparam SHIFT_R= 4'b1001;
    localparam JUMP   = 4'b1010;
    localparam JUMP_Z = 4'b1011;
    localparam OUT    = 4'b1100;

    // Fetch instruction
    wire [7:0] current_instruction;
    assign current_instruction = instruction_memory[pc];

    // Decode
    wire [3:0] opcode;
    wire [3:0] data;
    assign opcode = current_instruction[7:4];
    assign data   = current_instruction[3:0];

    // ALU Signals
    wire [3:0] alu_result;
    wire alu_zero_flag;

    // ALU Initialization
    ALU alu(
        .A(register_A),
        .B(register_B),
        .opcode(opcode),
        .result(alu_result),
        .zero_flag(alu_zero_flag)
    );

    // Set output
    assign output_data = output_register;

    // Program code
    initial begin
        instruction_memory[0] = {LOAD_A, 4'd10};
        instruction_memory[1] = {LOAD_B, 4'd3};
        instruction_memory[2] = {ADD, 4'd0};
        instruction_memory[3] = {SHIFT_L, 4'd0};
        instruction_memory[4] = {OUT, 4'd0};
        instruction_memory[5] = {SUB, 4'd0};
        instruction_memory[6] = {OUT, 4'd0};
        instruction_memory[7] = {JUMP, 4'd0};
    end

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            pc <= 4'b0;
            register_A = 4'b0;
            register_B = 4'b0;
            output_register = 4'b0;
        end else begin
            case (opcode)
                LOAD_A: register_A <= data;
                LOAD_B: register_B <= data;
                OUT: output_register <= register_A;
                JUMP: pc <= data;
                JUMP_Z: begin
                    if (alu_zero_flag) pc <= data;
                    else pc <= pc + 1;
                end
            endcase

            // Increment PC for non-jump instructions
            if (opcode != JUMP && opcode != JUMP_Z) pc <= pc + 1;
        end
    end
endmodule