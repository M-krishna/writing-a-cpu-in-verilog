16-bit RISC CPU implementation
-------------------------

As usual the operations are,

* Fetch
* Decode
* Execute

Since our CPU is 16-bit, it must have 2^16 = 65,536 (0 to 65,535) instruction memory locations.

What about the data memory? How should we decide that? Can we have 4 GB of memory???

4 GB = 4096 MB

Instruction Set Architecture
----------------------------
How should we encode the instruction?