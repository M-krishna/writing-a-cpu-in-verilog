module alu_tb;
    reg [31:0] A;
    reg [31:0] B;
    reg [1:0] op;
    wire [31:0] out;

    alu _alu(
        .A(A),
        .B(B),
        .op(op),
        .out(out)
    );

    // OPERATIONS
    localparam ADD = 2'b00;
    localparam SUB = 2'b01;
    localparam AND = 2'b10;
    localparam OR = 2'b11;

    initial begin
        #0 op = ADD; A = 32'hA; B = 32'hB;
        #1 op = SUB; A = 32'hB; B = 32'hA;
        #1 op = AND; A = 32'h4; B = 32'h5;
        #1 op = OR; A = 32'h4; B = 32'h5;
    end

    initial
        $monitor("Time = [%0t], A=%0d B=%0d op=%b out=%0d", $time, A, B, op, out);
endmodule