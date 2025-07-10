// TODO: Improve the testbench
module register_file_tb;
    reg [4:0] read_addr1;
    reg [4:0] read_addr2;
    reg [4:0] write_addr;
    reg [31:0] write_data;
    reg write_enable;
    reg clk;
    wire [31:0] read_data1;
    wire [31:0] read_data2; 

    register_file _rf(
        .read_addr1(read_addr1),
        .read_addr2(read_addr2),
        .write_addr1(write_addr),
        .write_data(write_data),
        .write_enable(write_enable),
        .clk(clk),
        .read_data1(read_data1),
        .read_data2(read_data2)
    );

    initial begin
        clk = 0;    // Initial data for clk
    end

    always #4 clk <= ~clk;  // Toggle clk value forever with 3 time units delay

    initial begin
        // we will write data to registers and read from it
        #1; write_enable = 1'b1; write_addr = 5'b00001; write_data = 32'hAF;
        #3; read_addr1 = 5'b00001;
        #5; $finish;
    end

    initial begin
        // We will fetch data from x0 (register 0) to check the value
        #3; read_addr1 = 5'b00000;
    end

    initial begin
        // we will try to write to register 0 and check the data of it
        #2; write_addr = 5'b0; write_data = 32'hAA;
    end

    initial
        $monitor("[Time = %0t], clk=%0d, read_addr1=%0d, read_addr2=%0d, write_addr=%0d, write_data=%0d, write_enable=%0d, read_data1=%0d, read_data2=%0d", $time, clk, read_addr1, read_addr2, write_addr, write_data, write_enable, read_data1, read_data2);
endmodule