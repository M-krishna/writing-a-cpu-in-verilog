module regfile(
    input wire clk,
    input wire reset,
    input wire we, // Write enable
    input wire waddr, // 1-bit write address, 0 for R0, 1 for R1
    input wire [7:0] wdata, // Data to write
    input wire rsel, // 1-bit read select, 0 selects R0, 1 selects R1
    output wire [7:0] rdata // Data read from the selected register
);
    // Two 8-bit registers stored in an array
    reg [7:0] regs [0:1];

    // Read operation: Combinational read
    assign rdata = regs[rsel];

    // Write operation
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            regs[0] <= 8'b0;
            regs[1] <= 8'b0;
        end else if (we) begin
            regs[waddr] <= wdata;
        end
    end
endmodule