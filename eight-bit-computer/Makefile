assemble: ./assembler/assembler.py
	chmod +x ./assembler/assembler.py
	./assembler/assembler.py $(FILE)

alu: alu.v ./testbench/alu_tb.v
	iverilog -o alu.o alu.v ./testbench/alu_tb.v
	vvp alu.o

regfile: regfile.v ./testbench/regfile_tb.v
	iverilog -o regfile.o regfile.v ./testbench/regfile_tb.v
	vvp regfile.o

cpu: cpu.v ./testbench/cpu_tb.v
	iverilog -o cpu.o cpu.v ./testbench/cpu_tb.v
	vvp cpu.o

clean:
	rm -rf *.o