module CPU_4bit(
    input wire clk,
    input wire reset,
    output wire [3:0] output_data
);

    // Program counter - only needs 4 bit to address 16 instructions
    reg [3:0] pc;

    // Instruction memory - stores 16 instructions, each 8 bits wide.
    // Format: [7:4] = opcode, [3:0] = data
    reg [7:0] instruction_memory [0:15];

    // Two 4-bit registers (minimum needed for basic operations)
    reg [3:0] register_A;
    reg [3:0] register_B;

    // current instruction components
    wire [3:0] opcode;
    wire [3:0] data;

    // Fetch current instruction
    wire [7:0] current_instruction;
    assign current_instruction = instruction_memory[pc];

    // Breakdown instructions (Decode instructions)
    assign opcode = current_instruction[7:4];
    assign data = current_instruction[3:0];

    // Operation codes (To do basic CPU operations)
    localparam LOAD_A = 4'b0001; // Load value into register_A
    localparam LOAD_B = 4'b0010; // Load value into register_B
    localparam ADD = 4'b0011; // Add A and B and store it in A
    localparam JUMP = 4'b0100; // Jump to address
    localparam OUT = 4'b0101; // Output value from Register A

    // Output register
    reg [3:0] output_register;
    assign output_data = output_register;

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            // Reset everything to initial state
            pc <= 4'b0;
            register_A <= 4'b0;
            register_B <= 4'b0;
            output_register <= 4'b0;
        end else begin
            // Execute instruction
            case (opcode)
                LOAD_A: register_A <= data;
                LOAD_B: register_B <= data;
                ADD: register_A <= register_A + register_B;
                JUMP: pc <= data;
                OUT: output_register <= register_A;
            endcase

            // Increment program counter except for JUMP instruction
            if (opcode != JUMP) begin
                pc <= pc + 1;
            end
        end
    end
endmodule