module CPU (
    input clk, reset
);
    // Fetch the instruction
    // Decode the instruction
    // Execute the instruction
    // Increment the program counter
    

    reg [15:0] instruction_memory [0:15]; // 16-bit instruction memory
    reg [3:0] program_counter; // 4-bit program counter (to address 16 instructions)

    // This is the CPU cycle
    always @(posedge clk or posedge reset) begin
	if (reset) begin
	    program_counter <= 4'b0000; // reset the program counter to 0
	end else begin
	    program_counter <= program_counter + 1;
	end
    end
endmodule
