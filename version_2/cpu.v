// A 4-bit CPU
module CPU(
    input wire clk,
    input wire reset,
    output wire [3:0] output_data
);

    // Our 4-bit CPU will have the following
    // PC = Program counter
    // Instruction memory = Where we store our instructions for our CPU to execute
    // Registers = To do basic operations with the data we fetch from instruction memory
    // Control flow = Decode the instructions and execute it.

    // Since this is a 4-bit CPU, our PC needs to be 4-bit wide and it can address upto 16 instructions
    reg [3:0] pc;

    // Instruction memory, total 16 instructions and each 8-bit wide
    // Format: [7:4] = Opcode, [3:0] = data
    reg [7:0] instruction_memory [0:15];

    // Now we have our instruction memory in place, 
    // lets put in some instructions for the CPU to execute
    /*
    * We'll decide what instructions we want. Just some basic stuffs
    * LOAD_A = Loads data into register A
    * LOAD_B = Loads data into register B
    * ADD = Adds register A and B and store it in register A
    * JUMP = Jump to an instruction
    * OUT = output data which will be present in register A

    * LOAD_A = 0001
    * LOAD_B = 0010
    * ADD    = 0011
    * JUMP   = 0100
    * OUT    = 0101
    */
    initial begin
        instruction_memory[0] = {4'b0001, 4'd10}; // LOAD 10 to register A
        instruction_memory[1] = {4'b0010, 4'd1}; // LOAD 1 to register B
        instruction_memory[2] = {4'b0011, 4'd0}; // ADD 10 + 1 and store the result in register A
        instruction_memory[3] = {4'b0101, 4'd0}; // Output the content in register A
        instruction_memory[4] = {4'b0100, 4'b0}; // Jump to instruction 0
    end


    // Now we have the instruction in place, let's create our two registers.
    // the registers are 4-bits wide
    reg [3:0] register_A;
    reg [3:0] register_B;
    reg [3:0] output_register; // to store the result of the operation


    // We have basic stuffs in place, let's begin fetching the instruction from memory and do something
    wire [7:0] current_instruction;
    assign current_instruction = instruction_memory[pc];

    // Now we have our current instruction, let's decode it and get the opcode and data from the instruction
    wire [3:0] opcode = current_instruction[7:4];
    wire [3:0] data = current_instruction[3:0];

    assign output_data = output_register;

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            // Reset the state of our CPU, we can do that by...
            pc <= 4'b0;
            register_A <= 4'b0;
            register_B <= 4'b0;
            output_register <= 4'b0;
        end else begin
            case (opcode)
                4'b0001: register_A <= data;
                4'b0010: register_B <= data;
                4'b0011: register_A <= register_A + register_B;
                4'b0101: output_register <= register_A;
                4'b0100: pc <= data;
            endcase

            // If it's not a JUMP instruction, increment the program counter
            if (opcode != 4'b0100) begin
                pc <= pc + 1;
            end
        end
    end
endmodule