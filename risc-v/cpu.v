module cpu(
    input clk,
    input reset,
    output [31:0] out
);
    reg [31:0] program_counter; // to hold the current address

    reg [31:0] instruction_memory [0:1023]; // 4KB instruction memory

    initial begin
        $readmemh("instruction.hex", instruction_memory);
    end

    wire [31:0] current_instruction;

    // Fetch the current instruction
    assign current_instruction = instruction_memory[program_counter >> 2];

    // Decode the current instruction
    wire [6:0] opcode = current_instruction[6:0];
    wire [4:0] rd = current_instruction[11:7];
    wire [2:0] funct3 = current_instruction[14:12];
    wire [4:0] rs1 = current_instruction[19:15];
    wire [4:0] rs2 = current_instruction[24:20];
    wire [6:0] funct7 = current_instruction[31:25];

    // Instruction Types ( Common RV32I Opcodes )
    localparam OP_IMM   = 7'b0010011;         // I-Type (ADDI, ANDI, etc.)
    localparam OP       = 7'b0110011;         // R-Type (ADD, SUB, etc.)
    localparam LOAD     = 7'b0000011;         // I-Type (LW, LB, etc.)
    localparam STORE    = 7'b0100011;         // S-Type (SW, SB, etc.)
    localparam BRANCH   = 7'b1100011;         // B-Type (BEQ, BNE, etc.)
    localparam LUI      = 7'b0110111;         // U-Type
    localparam JAL      = 7'b1101111;         // J-Type

    // Add register file instance
    wire [31:0] rs1_data; // Data from register rs1
    wire [31:0] rs2_data; // Data from register rs2

    register_file _rf(
        .read_addr1(rs1),
        .read_addr2(rs2),
        .write_addr1(rd),
        .write_data(),
        .write_enable(),
        .clk(clk),
        read_data1(rs1_data),
        read_data2(rs2_data)
    );

    // Add ALU instance
    wire [31:0] alu_result;
    wire [1:0] alu_op;

    alu _alu(
        .A(rs1_data),       // From register rs1
        .B(),               // rs2_data or immediate value
        .op(alu_op),        // Control signal
        .out(alu_result)    // To write_data
    );

    // PC Update logic (separate from instruction execution)
    always @(posedge clk or posedge reset) begin
        if (reset) begin    // Asynchronous reset
            program_counter <= 32'b0;
        end else begin
            program_counter <= program_counter + 4;
        end
    end

    // Instruction decode logic (combinational)
    always @(*) begin
        case (opcode)
            OP_IMM: begin end
            OP: begin end
            LOAD: begin end
            STORE: begin end
            BRANCH: begin end
            LUI: begin end
            JAL: begin end
            default: begin end
        endcase
    end
endmodule