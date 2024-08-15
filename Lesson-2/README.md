# Representing Programs

- How do you represent a program? The classic options:
    - Concrete syntax
    - Abstract syntax (AST).
    - Instructions.

- We like the instruction representation for its regularity.
  To do anything useful with it, however, we need to extract higher-level representations.


- Basic Blocks
--------------

  - Replace single instructions as vertices in the CFG with little sequences
    of instructions.
  - Jumps and branches only happen at the end of a basic block.
    And you can only jump to the top of the basic block.
  - If any instruction in a basic block executes, all of its Instructions
    must execute.


### An Algorithm to form Basic Blocks 

```python

block = []
lblToBlock = {}
for i in instrs:
    if i is NOT a LABEL:
        block.append(i)
    if i is A LABEL or TERMINATOR(br/jmp):
        blocks.append(block)
        block = []

```

### An Algorithm to form CFG out of basic blocks


```python


for block in blocks:
    last = block[-1]
    if last is JMP:
        add edge from block to last.dest
    else if last is BR:
        ADD two edges: from block to last.true and last.false
    else
        Block does not have terminator.
        So ADD Edge to block +1 if it exists.


````



