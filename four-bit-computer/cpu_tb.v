module cpu_tb;
    // Test signals
    reg clk;
    reg reset;
    wire [3:0] output_data;

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
        #8 reset = 0;
        #100;
        $display("Finishing simulation...");
        $finish;
    end

    initial begin
        $monitor("[Time=%0t] clk=%0t reset=%0t pc=%0t output_data=%0t", $time, clk, reset, _cpu.pc, output_data);
    end
endmodule