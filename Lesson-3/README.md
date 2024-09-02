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


```

# Local Value Numbering

- Build a table to track unique canonical sources for every value we compute.
- Step through the code, keeping track of the value number for each variable at a given point in time.

```llvm
main {
    a: int = const 4;
    b: int = const 2;
    sum1: int = add a b;
    sum2: int = add a b;
    prod: int = mul sum1 sum2;
    print prod;
}
```

- for sum1 and sum2 we need to create a tuple, so like we are using
  #1 and #2 here.
  It would be (add, #1, #2).
- Now sum1 and sum2 will point to the same row which is #3.


| # |     Value     | Destination   |
|---|---------------|---------------|
| 1 | const 4       | a             |
| 2 | const 2       | b             |
| 3 | (add, #1, #2) | sum1          |
| 4 | (mul, #3, #3) | prod          |
|   |               |               |
-------------------------------------

 
