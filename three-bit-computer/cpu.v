// 3-bit CPU
// 2^3 = 8 (so it can go from 0 to 7)

module cpu(
    input wire clk,
    input wire reset,
    output wire [2:0] output_data
);
    // Program counter
    reg [2:0] pc;

    // Instruction memory
    reg [2:0] instruction_memory [0:7];

    /* 
     Fetch instruction
     Instruction format =>
     First 2 bits starting from MSB is for opcode, so the opcodes are 00, 01, 10, 11
     The LSB is for data 
    */
    wire [2:0] current_instruction;
    assign current_instruction = instruction_memory[pc];

    // Decode instruction
    wire [1:0] opcode;
    wire data;

    assign opcode  = current_instruction[2:1];
    assign data	   = current_instruction[0];

    // Register file
    reg [2:0] register_A;

    assign output_data = register_A;

    initial begin
        $readmemh("instructions.hex", instruction_memory);
    end

    // Mnemonics
    localparam LOAD   = 2'b00;
    localparam ADD    = 2'b01;
    localparam SUB    = 2'b10;

    always @(posedge clk) begin
        if (reset) begin // Synchronous reset
            pc <= 3'b0;
            register_A <= 3'b0;
        end else begin
            case (opcode)
                LOAD   : register_A <= data;
                ADD    : register_A <= register_A + data;
                SUB    : register_A <= register_A - data;
            endcase
            pc <= pc + 1;
        end
    end
endmodule
