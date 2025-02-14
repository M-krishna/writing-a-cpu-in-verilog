assemble: assembler.py
	chmod +x assembler.py
	./assembler.py

build: cpu.v cpu_tb.v
	iverilog -o cpu.o cpu.v cpu_tb.v
	vvp cpu.o

clean:
	rm -rf *.o
	rm -rf *.hex
	rm -rf *.bin
