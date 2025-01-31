module cpu_tb;

    // test signals
    reg clk;
    reg reset;
    wire [3:0] output_data;

    // CPU initialization
    cpu cpu_(
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
        #10;
        reset = 0;

        #100;
        $finish;
    end

    initial begin
        $monitor("[Time=%0t clk=%0d reset=%0d output_data=%0d]", $time, clk, reset, output_data);
    end
endmodule