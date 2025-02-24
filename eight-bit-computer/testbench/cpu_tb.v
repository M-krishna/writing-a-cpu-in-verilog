module cpu_tb;
    // test signals
    reg clk;
    reg reset;
    wire [7:0] output_data;

    // Initialize module
    cpu _cpu(
        .clk(clk),
        .reset(reset),
        .output_data(output_data)
    );

    initial begin
        clk = 0; reset = 0;
        forever #2 clk = ~clk;
    end

    initial begin
        #3 reset = 1;
        #1 reset = 0;

        #50; // Run the simulation for some time
        $finish;
    end

    initial begin
        $monitor("[Time=%0t] clk=%0d reset=%0d pc=%b output_data=%0d", $time, clk, reset, _cpu.pc, output_data);
    end
endmodule