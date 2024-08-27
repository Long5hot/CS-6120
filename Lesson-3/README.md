# Local Analysis & Optimization

### Local Optimization

- Works within single basic block.
- Don't have to think about control flow.
- just have to think about ordering of instrucitons(Linear Scan).

### Global Optimization

- Optimization on an entire function.
- Have to deal with the control flow.
- Much more complecated.

### Interprocedural Optimizations

- Local and Global Optimizations.


## Dead Code Elimination

- Removes code that can't possibly affect on output.
- instruciton can be deleted if it assigns to a variable, that is never used as argument,
  as long as that instruciton that has no side effects (No use in output).


```llvm
@main {
  a: int = const 4;
  b: int = const 2;
  c: int = const 1;
  d: int = add a b;
  print d;
}

@main {
  a: int = const 4;
  b: int = const 2;
  d: int = add a b;
  print d;
}

```

```python
used = []

for instrs in block:
    used +=instrs["args"]

for instrs in block:
    remove if instr.dest and instr.dest NOT in used.

```

- How to do dce in below?

```llvm
@main {
  a: int = const 4;
  b: int = const 2;
  c: int = const 1;
  d: int = add a b;
  e: int = add c d;
  print d;
}
```

- easy solution is run dce multiple times in that bb.

    ```python
        while program changed:
            run DCE
    ```

- run DCE in below

```llvm
@main {
  a: int = const 100;
  a: int = const 42;
  print a;
}
```
- previous algo will do nothing.

```python

used = []

for instrs in block:
    used +=instrs["args"]

for index, instr in enumarate(block):
    if dest in instr:
        remove instr.dest NOT in used.
    if block[index]["dest"] == block[index-1]["dest"]:
        remove block[index-1]



for index, instr in enumarate(block):
    if dest in instr:
        

```
