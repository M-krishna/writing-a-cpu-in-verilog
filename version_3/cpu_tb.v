module CPU_tb;
    // signals
    reg clk;
    reg reset;
    wire [3:0] output_data;

    // Initialize module
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
        $display("Starting simulation...");
        reset = 1;
        #10;
        reset = 0;

        #200; // Let the program run

        $display("Simulation finished");
        $finish;
    end

    initial begin
        $monitor("[Time=%0t] clk=%0d reset=%0d output_data=%0d", $time, clk, reset, output_data);
    end
endmodule