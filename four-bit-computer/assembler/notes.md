21st Feb 2025
---
colon(":") can't be a standalone token. It is part of the label identifier.

For example, 
```
JMP TEST_1
TEST_1:
    LOAD 1
    ADD 1
    JMP 0
```
Here `TEST_1:` should be parsed as a single token

### First pass and Second pass
In a two pass assembler, the assembler goes through the source code two times.

**Pass 1: Building the Symbol Table**

