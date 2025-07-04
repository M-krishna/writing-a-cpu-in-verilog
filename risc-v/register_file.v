module register_file(
    input clk,
    input [4:0] read_addr1,             // Address for the first read port
    input [4:0] read_addr2,             // Address for the second read port
    input [4:0] write_addr,             // Address for write port
    input [31:0] write_data,            // Data to write
    input write_enable,                 // Enable writing
    output [31:0] read_data1,           // Data from first read port
    output [31:0] read_data2            // Data from second read port
)
endmodule