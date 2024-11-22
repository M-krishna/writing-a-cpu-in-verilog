module my_basic_cpu_tb;
    reg clk, reset;

    CPU  cpu (
	.clk(clk),
	.reset(reset)
    );

    always #2 clk <= ~clk;

endmodule
