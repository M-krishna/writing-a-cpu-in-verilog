module register_file(
    input [4:0] read_addr1,
    input [4:0] read_addr2,
    input [4:0] write_addr1,
    input [31:0] write_data,
    input write_enable,
    input clk,
    output [31:0] read_data1,
    output [31:0] read_data2
);
    // Create a registers array to hold registers
    reg [31:0] registers [0:31];    // 32 registers, each 32-bit wide

    localparam register0 = 5'b0;

    assign read_data1 = (read_addr1 == register0) ? 32'b0 : registers[read_addr1];
    assign read_data2 = (read_addr2 == register0) ? 32'b0 : registers[read_addr2];

    always @(posedge clk) begin
        if (write_addr1 != register0 && write_enable) begin
            registers[write_addr1] <= write_data;
        end
    end
endmodule