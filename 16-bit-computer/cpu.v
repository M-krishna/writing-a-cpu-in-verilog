module cpu(
    input wire clk,
    input wire reset,
    output wire [15:0] output_data
);
    // Program counter
    reg [15:0] pc;

    // Instruction memory
    reg [15:0] instruction_memory [0:65535];

    // Fetch and decode instructions
endmodule