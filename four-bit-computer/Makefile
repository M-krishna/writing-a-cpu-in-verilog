assemble: ./assembler/assembler.py
	chmod +x ./assembler/assembler.py
	./assembler/assembler.py $(FILE)

build:
	iverilog -o ./output/cpu.o cpu.v cpu_tb.v
	vvp ./output/cpu.o

clean:
	rm -rf ./output/*.hex
	rm -rf ./output/*.bin
	rm -rf ./output/*.o