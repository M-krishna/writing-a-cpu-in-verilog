module cpu_tb();
    
    // Test signals
    reg clk;
    reg reset;
    wire [3:0] output_data;

    // Initialize our CPU
    CPU cpu(
        .clk(clk),
        .reset(reset),
        .output_data(output_data)
    );

    initial begin
      clk = 0;
      forever #5 clk = ~clk;
    end

    initial begin
        reset = 1;
        #10; // wait for 10ns
        reset = 0;

        // Give it some time for the program to run
        #200;

        $finish; // End of Simulation
    end

    initial begin
        $monitor("[Time=%0t] clk=%d reset=%d output_data=%d", $time, clk, reset, output_data);
    end
endmodule