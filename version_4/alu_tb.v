module alu_tb;
    // test signals
    reg [3:0] A;
    reg [3:0] B;
    reg [3:0] opcode;
    wire [3:0] result;
    wire zero_flag;

    // module initialization
    ALU alu(
        .A(A),
        .B(B),
        .opcode(opcode),
        .result(result),
        .zero_flag(zero_flag)
    );

    initial begin
        $display("Starting...");
        A=0; B=0; opcode=4'b0001;
        #10 A=10; B=3; opcode=4'b0001;
        #10 A=10; B=3; opcode=4'b0010;
        #10 A=1; B=2; opcode=4'b0011;
        #10 A=1; B=2; opcode=4'b0100;
        #10 A=1; B=2; opcode=4'b0101;
        #10 A=1; opcode=4'b0110;
        #100;
        $finish;
    end

    initial begin
        $monitor("[Time=%0t A=%0d B=%0d opcode=%4b result=%0d]", $time, A, B, opcode, result);
    end
endmodule