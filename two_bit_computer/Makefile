build: cpu.v cpu_tb.v
	iverilog -o cpu.out cpu.v cpu_tb.v
	vvp cpu.out

clean:
	rm -rf cpu.out
