build: cpu.v cpu_tb.v
	iverilog -o cpu.o cpu.v cpu_tb.v
	vvp cpu.o

clean:
	rm -rf cpu.o
