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

### Dead Code Elimination

- above examples.

### Copy Propogation

```llvm
@main {
    x : int = const 4;
    copy1: int = id x;
    copy2: int = id copy1;
    copy3: int = id copy2;
    print copy3;
}
```

- For above case we can just print value x.

```llvm
@main {
    x : int = const 4;
    copy1: int = id x;
    copy2: int = id x;
    copy3: int = id x;
    print x;
}
```

### Commom Subexpression Elimination

```llvm
@main {
    a: int = const 4;
    b: int = const 2;
    sum1: int = add a b;
    sum2: int = add a b;
    prod: int = mul sum1 sum2;
    print prod;
}
```
- sum1 and sum2 represent the same value.
```llvm
@main {
    a: int = const 4;
    b: int = const 2;
    sum1: int = add a b;
    prod: int = mul sum1 sum1;
    print prod;
}
```

### Constant Propogation

```llvm
@main {
    x : int = const 4;
    copy1: int = id x;
    copy2: int = id copy1;
    copy3: int = id copy2;
    print x;
}
```
 will be transfered to
```llvm
@main {
    x : int = const 4;
    copy1: int = id 4;
    copy2: int = id 4;
    copy3: int = id 4;
    print x;
}
```

### Constant Folding

```llvm
@main {
    a: int = const 4;
    b: int = const 2;

    sum1: int = add a b;
    sum2: int = add a b;
    prod1: int = mul sum1 sum2;

    sum1: int = const 0;
    sum2: int = const 0;

    sum3: int = add a b;
    prod2: int  = mul sum3 sum3;

    print prod2;
}
```

```llvm
@main {
    prod2: int = const 36;
    print prod2;
}
```


### How LVN Works?

```llvm
@main {
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


| # |     Value     | Destination (current canonical home) |
|---|---------------|---------------|
| 1 | const 4       | a             |
| 2 | const 2       | b             |
| 3 | (add, #1, #2) | sum1          |
| 4 | (mul, #3, #3) | prod          |
|   |               |               |
-------------------------------------

```python
table = mapping from value tuples to canonical variables,
  with each row numbered
var2num = mapping from variable names to their current
  value numbers (i.e., rows in table)

for instr in block:
    value = (instr.op, var2num[instr.args[0]], ...)

    if value in table:
        # The value has been computed before; reuse it.
        num, var = table[value]
        replace instr with copy of var

    else:
        # A newly computed value.
        num = fresh value number

        dest = instr.dest
        if instr will be overwritten later:
             dest = fresh variable name
             instr.dest = dest
        else:
             dest = instr.dest

        table[value] = num, dest

        for a in instr.args:
            replace a with table[var2num[a]].var

    var2num[instr.dest] = num
```

 
