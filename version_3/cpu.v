module CPU(
    input wire clk,
    input wire reset,
    output wire [3:0] output_data
);

    // we need program counter to access instructions
    reg [3:0] pc;

    // instruction memory
    reg [7:0] instruction_memory [0:15];

    // Actual instructions (This is our "instruction set")
    localparam LOAD_A = 4'b0001; // Load to register A
    localparam LOAD_B = 4'b0010; // Load to register B
    localparam ADD    = 4'b0011; // Add register A and B and store the result in A
    localparam SUB    = 4'b0100; // Sub register B from A and store the result in A
    localparam AND    = 4'b0101; // Bitwise AND
    localparam OR     = 4'b0110; // Bitwise OR
    localparam XOR    = 4'b0111; // Bitwise XOR
    localparam NOT    = 4'b1000; // Bitwise NOT of A
    localparam SHIFT_L= 4'b1001; // Shift A left by 1
    localparam SHIFT_R= 4'b1010; // Shift A right by 1
    localparam JUMP   = 4'b1011; // Jump to address
    localparam JUMP_Z = 4'b1100; // Jump if zero
    localparam OUT    = 4'b1101; // Output A

    reg [3:0] register_A;
    reg [3:0] register_B;
    reg [3:0] output_register;
    reg zero_flag; // Added a zero_flag for conditional jumps


    // Instruction fetch and decode
    wire [7:0] current_instruction;
    assign current_instruction = instruction_memory[pc];

    // Decode
    wire [3:0] opcode = current_instruction[7:4];
    wire [3:0] data = current_instruction[3:0];

    // Set output
    assign output_data = output_register;

    // Embed instruction that we want to execute directly into code, rather than in testbench
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

    // CPU cycle
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            pc <= 4'b0;
            register_A <= 4'b0;
            register_B <= 4'b0;
            output_register <= 4'b0;
            zero_flag <= 1'b0;
        end else begin
            case (opcode)
                LOAD_A: begin
                    register_A <= data;
                    zero_flag <= (data == 4'b0);
                end

                LOAD_B: register_B <= data;

                ADD: begin
                    register_A <= register_A + register_B;
                    zero_flag <= ((register_A + register_B) == 4'b0);
                end

                SUB: begin
                    register_A <= register_A - register_B;
                    zero_flag <= ((register_A - register_B) == 4'b0);
                end

                AND: begin
                    register_A <= register_A & register_B;
                    zero_flag <= ((register_A & register_B) == 4'b0);
                end

                OR: begin
                    register_A <= register_A | register_B;
                    zero_flag <= ((register_A | register_B) == 4'b0);
                end

                XOR: begin
                    register_A <= register_A ^ register_B;
                    zero_flag <= ((register_A ^ register_B) == 4'b0);
                end

                NOT: begin
                    register_A <= ~register_A;
                    zero_flag <= (~register_A == 4'b0);
                end

                SHIFT_L: begin
                    register_A <= register_A << 1;
                    zero_flag <= ((register_A << 1) == 4'b0);
                end

                SHIFT_R: begin
                    register_A <= register_A >> 1;
                    zero_flag <= ((register_A >> 1) == 4'b0);
                end

                JUMP: pc <= data;

                JUMP_Z: begin
                    if (zero_flag) pc <= data;
                    else pc <= pc + 1;
                end

                OUT: output_register <= register_A;

                default: ; // Do nothing for unknown opcodes
            endcase

            // Increment PC for non-jump instructions
            if (opcode != JUMP && opcode != JUMP_Z) pc <= pc + 1;
        end
    end

endmodule