assemble: assembler.py
	chmod +x ./assembler.py
	./assembler

build:
	iverilog -o cpu.o cpu.v cpu_tb.v
	vvp cpu.o

clean:
	rm -rf *.hex
	rm -rf *.bin
	rm -rf *.o