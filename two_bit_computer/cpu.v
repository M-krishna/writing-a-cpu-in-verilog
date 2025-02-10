// 2-bit computer
// At max it can hold 4 instructions (2^2 = 4)

module cpu(
    input wire clk,
    input wire reset,
    output wire [1:0] output_data
);
    // Program counter
    reg [1:0] pc;

    // Instruction memory
    // Instruction memory format => MSB is the opcode and LSB is the data
    // 10 means, 1 is the opcode and 0 is the data
    reg [1:0] instruction_memory [0:3];

    // Fetch and Decode
    wire [1:0] current_instruction;
    assign current_instruction = instruction_memory[pc];

    // Get the opcode and data
    wire opcode;
    wire data;

    assign opcode = current_instruction[1];
    assign data = current_instruction[0];

    // Register file
    reg [1:0] register_A; // the maximum decimal value you can store is 3

    // Assign output data
    assign output_data = register_A;

    localparam LOAD = 1'b0; // LOAD the data into register A
    localparam ADD  = 1'b1; // Adds the immediate value with the value in register A

    // Dumping the instruction directly into the code
    //initial begin
    //    instruction_memory[0] = {LOAD, 1'd1};
    //    instruction_memory[1] = {ADD, 1'd1};
    //    instruction_memory[2] = {LOAD, 1'b0}; // NOP equivalent
    //    instruction_memory[3] = {LOAD, 1'b0}; // NOP equivalent
    //    // It's okay to ignore instruction memory 2 & 3
    //end

    initial begin
	$readmemh("instructions.hex", instruction_memory);
    end

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            pc <= 2'b0;
            register_A <= 1'b0;
        end else begin
            case (opcode)
                LOAD : register_A <= data;
                ADD  : register_A <= register_A + data; 
            endcase
            // Increment program counter
            pc <= pc + 1;
        end
    end
endmodule
