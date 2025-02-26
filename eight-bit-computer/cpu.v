// 8-bit CPU

module cpu(
    input wire clk,
    input wire reset,
    output wire [7:0] output_data
);
    // Program counter
    reg [7:0] pc;

    // Instruction memory
    // First 3 bits are used for opcode, starting from MSB
    // The next bit is used for mode, it is to decide whether are next bits are immediate value or register
    // The last 4 bits can be either an immediate value or register
    reg [7:0] instruction_memory [0:255];

    // Fetch and Decode
    wire [7:0] current_instruction;

    assign current_instruction = instruction_memory[pc]; // Fetch the current instruction

    wire [2:0] opcode;
    wire mode;  // Used to decide whether the next four bits are immediate value or registers
    wire [3:0] op_field;  // either immediate value or register

    // Decode the current instruction
    assign opcode = current_instruction[7:5];
    assign mode = current_instruction[4];
    assign op_field = current_instruction[3:0];

    // Signals for Register file
    reg write_enable;
    reg write_address;
    reg [7:0] write_data;
    reg read_select;
    wire [7:0] read_data;

    // Initialize Register file module
    regfile _regfile(
      .we(write_enable),
      .waddr(write_address),
      .wdata(write_data),
      .rsel(read_select),
      .rdata(read_data)  
    );

    reg [7:0] r0; // register 0
    reg [7:0] r1; // register 1

    // Signals for ALU
    reg [7:0] operand_A;
    reg [7:0] operand_B;
    reg [2:0] alu_control;
    wire [7:0] alu_result;

    // Intitialize the ALU module
    alu _alu(
        .operand_A(operand_A),
        .operand_B(operand_B),
        .alu_control(alu_control),
        .result(alu_result)
    );

    assign output_data = register_A;

    // Get the program instructions for an instruction file
    initial begin
        $readmemh("instructions.hex", instruction_memory);
    end

    localparam LOAD     = 3'b000;
    localparam ADD      = 3'b001;
    localparam SUB      = 3'b010;
    localparam AND      = 3'b011;
    localparam OR       = 3'b100;
    localparam XOR      = 3'b101;
    localparam JMP      = 3'b110;
    localparam HLT      = 3'b111;

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            pc <= 8'b0;
            register_A <= 8'b0;
        end else begin
            case (opcode)
                LOAD:   register_A <= data;
                ADD, SUB, AND, OR, XOR: begin
                    operand_A <= register_A;
                    operand_B <= {3'b0, data};
                    case (opcode)
                        ADD:    alu_control <= ADD;
                        SUB:    alu_control <= SUB;
                        AND:    alu_control <= AND;
                        OR:     alu_control <= OR;
                        XOR:    alu_control <= XOR;
                    endcase
                    register_A <= alu_result;
                end
                JMP:    pc <= {3'b0, data}; // jump to a specific address mentioned in the data
                HLT:    begin
                            $display("HLT instruction encountered. Stopping CPU.");
                            $finish;
                        end
            endcase

            // Increment the program counter if the opcode is not a JMP instruction
            if (opcode != JMP) pc <= pc + 1
        end
    end
endmodule