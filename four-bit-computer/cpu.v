// 4-bit CPU
// 2^4 => 16 Memory locations
// 4 unique instructions, if we take two bits from instruction memory as opcodes
// 8 unique instructions, if we take three bits from instruction memory as opcodes

/* 
    * So far I have played around with 4 unique instructions with 2-bits of instruction memory
    * And 2-bits data memory.
    * So in this implementation, I am choosing to use three bits for opcode. This will give us 8 unique instructions
    * And only 1 bit for data
*/


module cpu(
    input wire clk,
    input wire reset,
    output wire [3:0] output_data
);

    // Program counter
    reg [3:0] pc;

    // Instruction memory
    reg [3:0] instruction_memory [0:15];

    // Fetch and Decode instructions
    // What is the instruction encoding format?
    /*
    * 0000
    * 0001
    * 0010
    * 0011
    * 0100
    * 0101
    * 0110
    * 0111
    * 1000
    * 1001
    * 1010
    * 1011
    * 1100
    * 1101
    * 1110
    * 1111
    */

    /*
        * We are going to use 3-bits for opcode
        * And 1-bit for data
        * So, we will get 8 unique instructions for opcode. That is
        * 000
        * 001
        * 010
        * 011
        * 100
        * 101
        * 110
        * 111

        * There will be only 1 bit for data, so the numbers 0 and 1 are the only numbers we are playaround with
    */

    wire [2:0] opcode;
    wire data;

    wire [3:0] current_instruction = instruction_memory[pc];

    reg [3:0] register_A;

    assign output_data = register_A;

    localparam LOAD     = 3'b000;
    localparam ADD      = 3'b001; 
    localparam SUB      = 3'b010;
    localparam AND      = 3'b011; // Bitwise AND
    localparam OR       = 3'b100; // Bitwise OR
    localparam XOR      = 3'b101;
    localparam JMP      = 3'b110;
    localparam HLT      = 3'b111;

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            pc <= 4'b0;
            register_A <= 4'b0;
        end else begin
            case (opcode)
                LOAD:   register_A <= data;
                ADD:    register_A <= register_A + data;
                SUB:    register_A <= register_A - data;
                AND:    register_A <= register_A & data;
                OR:     register_A <= register_A | data;
                XOR:    register_A <= register_A ^ data;
                JMP:    pc <= data;
                HLT:    begin
                            $display("HLT encountered. Stopping CPU");
                            $finish;
                        end
                default: ; // Do nothing for default case.
            endcase

            // If the opcode is not JMP, then increment the program counter
            if (opcode != JMP) begin
                pc <= pc + 1;
            end
        end
    end
endmodule