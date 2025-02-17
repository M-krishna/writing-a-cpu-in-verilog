module cpu_tb;
    // Test signals
    reg clk;
    reg reset;
    wire [1:0] output_data;

    // Module initialization
    cpu _cpu(
        .clk(clk),
        .reset(reset),
        .output_data(output_data)
    );

    initial begin
        clk = 0;
        reset = 1;
        forever #2 clk = ~clk;
    end

    initial begin
        #10; // give it some time
        reset = 0;
	#60
        $finish; // finish the simulation
    end

    initial begin
        $monitor("[Time=%0t clk=%0d reset=%0d pc=%b output_data=%0d]", $time, clk, reset, _cpu.pc, output_data);
    end
endmodule
