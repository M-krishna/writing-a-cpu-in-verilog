module cpu(
    input clk,
    input reset,
    output [31:0] out
);
    // ============= PROGRAM COUNTER =======================
    reg [31:0] program_counter; // to hold the current address
    reg pc_src;                 // Program counter source

    always @(posedge clk or posedge reset) begin
        if (reset) begin    // Asynchronous reset
            program_counter <= 32'b0;
        end else begin
            if (pc_src)
                program_counter <= program_counter + imm_j;     // JAL Jump
            else
                program_counter <= program_counter + 4;         // Normal increment
        end
    end

    // =========== INSTRUCTION MEMORY ==========================
    reg [31:0] instruction_memory [0:1023]; // 4KB instruction memory

    initial begin
        $readmemh("instruction.hex", instruction_memory);
    end

    // ================ INSTRUCTION FETCH ========================
    wire [31:0] current_instruction;
    assign current_instruction = instruction_memory[program_counter >> 2];

    // ================= INSTRUCTION DECODE =======================
    // Decode the current instruction (R-Type)
    wire [6:0] opcode = current_instruction[6:0];
    wire [4:0] rd = current_instruction[11:7];
    wire [2:0] funct3 = current_instruction[14:12];
    wire [4:0] rs1 = current_instruction[19:15];
    wire [4:0] rs2 = current_instruction[24:20];
    wire [6:0] funct7 = current_instruction[31:25];

    // Immediate extraction (I-type)
    wire [31:0] imm_i = {{20{current_instruction[31]}}, current_instruction[31:20]}; // Sign extension
    wire [31:0] imm_u = {current_instruction[31:12], 12'b0};
    wire [31:0] imm_j = {
        {20{current_instruction[31]}}
    }

    // Instruction Types ( Common RV32I Opcodes )
    localparam OP_IMM   = 7'b0010011;         // I-Type (ADDI, ANDI, etc.)
    localparam OP       = 7'b0110011;         // R-Type (ADD, SUB, etc.)
    localparam LOAD     = 7'b0000011;         // I-Type (LW, LB, etc.)
    localparam STORE    = 7'b0100011;         // S-Type (SW, SB, etc.)
    localparam BRANCH   = 7'b1100011;         // B-Type (BEQ, BNE, etc.)
    localparam LUI      = 7'b0110111;         // U-Type
    localparam JAL      = 7'b1101111;         // J-Type

    // ============== CONTROL SIGNALS ======================
    reg write_enable;
    reg [31:0] alu_b_input;
    reg [2:0] alu_op;
    reg [1:0] write_data_src;
    
    // ============== WRITE DATA MULTIPLEXER =================
    reg [31:0] write_data;

    always @(*) begin
        case (write_data_src)
            2'b00: write_data = alu_result;
            2'b01: write_data = imm_u;
            2'b10: write_data = program_counter + 4;
            2'b11: write_data = 32'b0;
            default: write_data = 32'b0;
        endcase
    end


    // ============== REGISTER FILE =========================
    wire [31:0] rs1_data; // Data from register rs1
    wire [31:0] rs2_data; // Data from register rs2

    register_file _rf(
        .read_addr1(rs1),
        .read_addr2(rs2),
        .write_addr1(rd),
        .write_data(write_data),
        .write_enable(write_enable),
        .clk(clk),
        .read_data1(rs1_data),
        .read_data2(rs2_data)
    );

    // =============== ALU =========================
    wire [31:0] alu_result;

    alu _alu(
        .A(rs1_data),       // From register rs1
        .B(alu_b_input),    // rs2_data or immediate value
        .op(alu_op),        // Control signal
        .funct7(funct7),
        .out(alu_result)    // To write_data
    );


    // ================= CONTROL LOGIC ===================
    always @(*) begin
        // Default values
        write_enable = 0;
        alu_b_input = 32'b0;
        alu_op = 3'b0;
        write_data_src = 2'b0;
        pc_src = 0;

        case (opcode)
            OP_IMM: begin
                write_enable = 1;
                alu_b_input = imm_i;
                alu_op = funct3;
                write_data_src = 2'b0;
            end
            OP: begin
                write_enable = 1;
                alu_b_input = rs2_data;
                alu_op = funct3;
                write_data_src = 2'b0;
            end
            LOAD: begin end
            STORE: begin end
            BRANCH: begin end
            LUI: begin
                write_enable = 1;
                write_data_src = 2'b01;
            end
            JAL: begin 
                write_enable = 1;
                write_data_src = 2'b10;
                pc_src = 1;
            end
            default: begin end
        endcase
    end
endmodule