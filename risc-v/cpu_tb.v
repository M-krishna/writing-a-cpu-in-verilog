module cpu_tb;
    reg [31:0] program_counter;

    initial begin
        $display("default value of program counter = %b", program_counter);

        program_counter = 32'hAA;
        $display("Value of program counter = %b", program_counter);
    end
endmodule