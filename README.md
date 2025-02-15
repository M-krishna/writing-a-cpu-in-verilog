# Writing a very basic CPU in Verilog

This is an experimental exercices for writing different CPUs in Verilog and Python

## Project Overview

This repository contains various implementations of CPUs

If you're interested in looking around, I would recommend you to start with `two_bit_computer`. Since it a very basic version, which comes with all the necessary command you need to playaround with it.

Checkout the `example_boilerplate_code_for_getting_started` folder to know how the project has been setup for writing and running Verilog programs

There are 3 basic versions of the CPU which you can look into if you'r ea beginner or you want to know how a CPU works. All of the code are written basic Verilog. So it would be easy to understand.

Checkout:
* `version_2`
* `version_3`
* `version_4`

## Things you need to run the programs
* Icarus Verilog
* Python

Checkout the `Makefile` in project directories to know more about the command to run

## Assembler code

For `two_bit_computer` and `three_bit_computer`, we have a custom `Assembler` written in python. You can write your assembly instructions in `instructions.txt` file and use the commands mentioned in the `Makefile` to assemble and run the programs on the CPU.

# License
This project is licensed under MIT.