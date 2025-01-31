alu: cpu.v alu_tb.v
	iverilog -o alu.o cpu.v alu_tb.v
	vvp alu.o

cpu: cpu.v
	iverilog -o cpu.o cpu.v cpu_tb.v
	vvp cpu.o

clear:
	rm -rf *.o