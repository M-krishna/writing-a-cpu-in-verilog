run: cpu.v cpu_tb.v
	iverilog -o cpu cpu.v cpu_tb.v
	vvp cpu

clear:
	rm cpu
