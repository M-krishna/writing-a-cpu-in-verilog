module cpu(
    input clk,
    input reset,
    output [31:0] out
);
    reg [31:0] program_counter; // to hold the current address

    reg [31:0] instruction_memory [0:1024]; // 1KB instruction memory

    initial begin
        $readmemh("instruction.hex", instruction_memory);
    end

    wire [31:0] current_instruction;

    assign current_instruction = instruction_memory[program_counter];

    always @(posedge clk or posedge reset) begin
        if (reset) begin    // Asynchronous reset
            program_counter <= 32'b0;
        end else begin
            program_counter <= program_counter + 4
        end
    end
endmodule