module CPU_4bit_tb();

    reg clk;
    reg reset;
    wire [3:0] output_data;

    // Instantiate the CPU
    CPU_4bit cpu (
        .clk(clk),
        .reset(reset),
        .output_data(output_data)
    );

    // Clock generation
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    // Test sequence
    initial begin
        // start with reset = 1
        reset = 1;
        #10; // wait for 10ns
        reset = 0;

        // Load test program into instruction memory
        // Program: Add 3 + 4 and output result
        $display("something...");
        cpu.instruction_memory[0] = {4'b0001, 4'd3}; // LOAD_A 3
        cpu.instruction_memory[1] = {4'b0010, 4'd4}; // LOAD_B 4
        cpu.instruction_memory[2] = {4'b0011, 4'd0}; // ADD
        cpu.instruction_memory[3] = {4'b0101, 4'd0}; // OUT
        cpu.instruction_memory[4] = {4'b0100, 4'd0}; // JMP to 0

        // Run for several clock cycles
        #100; // wait for program to execute

        // Display results
        $display("Time=%0t output_data=%d", $time, output_data);

        // End simulation
        $finish;
    end

    // Monitor changes
    initial begin
        $monitor("Time=%0t reset=%0b pc=%d regA=%d regB=%d output=%d",
            $time, reset, cpu.pc, cpu.register_A, cpu.register_B, output_data
        );
    end
endmodule