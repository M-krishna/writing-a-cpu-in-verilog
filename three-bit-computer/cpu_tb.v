module cpu_tb;
    // Test signals
    reg clk;
    reg reset;
    wire [2:0] output_data;

    // Initialize module
    cpu _cpu(
        .clk(clk),
        .reset(reset),
        .output_data(output_data)
    );

    initial begin
        clk = 0;
        forever #2 clk = ~clk;
    end

    initial begin
        #2 reset = 1;
        #4 reset = 0;

        #30;
        $finish;
    end

    initial begin
        $monitor("[Time=%0t clk=%0d reset=%0d pc=%0d output_data=%0d]", $time, clk, reset, _cpu.pc, output_data);
    end
endmodule