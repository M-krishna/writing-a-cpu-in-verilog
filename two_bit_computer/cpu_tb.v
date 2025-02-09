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
        forever #5 clk = ~clk;
    end

    initial begin
        reset = 1;
        #10; // give it some time
        reset = 0;

        #100;
        $finish; // finish the simulation
    end

    initial begin
        $monitor("[Time=%0t clk=%0d reset=%0d output_data=%0d]", $time, clk, reset, output_data);
    end
endmodule