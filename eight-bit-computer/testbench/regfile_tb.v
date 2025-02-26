module regfile_tb;
    // Test signals
    reg clk;
    reg reset;
    reg write_enable;
    reg write_address;
    reg [7:0] write_data;
    reg read_select;
    wire [7:0] read_data;

    // Initialize module
    regfile _regfile(
        .clk(clk),
        .reset(reset),
        .we(write_enable),
        .waddr(write_address),
        .wdata(write_data),
        .rsel(read_select),
        .rdata(read_data)
    );

    always #5 clk = ~clk;

    initial begin
        // set the initial value
        clk = 0;
        reset = 0;
        write_enable = 0;
        write_address = 0;
        write_data = 8'b0;
        read_select = 0;

        reset = 1;
        #10;
        reset = 0;
        #10;

        // Set and get the value of register 0
        write_data = 8'hAA;
        write_address = 0;
        write_enable = 1;
        #10;
        write_enable = 0;
        read_select = 0; // Get the value from register 0

        // Set and get the value of register 1
        write_data = 8'hFF;
        write_address = 1;
        write_enable = 1;
        #10;
        write_enable = 0;
        read_select = 1; // Get the value from register 1

        #20;
        $finish; // Finish simulation
    end

    initial begin
        $monitor("[Time = %0t] selected_register = %b reg = %h", $time, read_select, read_data);
    end
endmodule