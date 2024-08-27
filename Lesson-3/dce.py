#!/usr/bin/python3.11

import json
import sys
from collections import OrderedDict

TERMINATORS = ('jmp', 'br', 'ret')

def form_blocks(instrs):
    cur_block = []
    blocks = []
    for instr in instrs:
        if 'op' in instr:  # An actual instruction
            cur_block.append(instr)
            
            # Check for terminators.
            if instr['op'] in TERMINATORS:
                blocks.append(cur_block)
                cur_block = []
        else:
            """If 'op' is not present currnet isntr is a Label.
               If last instr was br then block is already appended"""
            if not cur_block:
                continue
            blocks.append(cur_block)
            cur_block = [instr]
    # Append last block, which just ends without any label or TERMINATORS.
    blocks.append(cur_block)
    return blocks

def block_map(blocks):
    out = OrderedDict()

    for block in blocks:
        
        if 'label' in block[0]:
            name = block[0]['label']
            block = block[1:]
        else:
            name = 'b{}'.format(len(out))
        
        out[name] = block
    
    return out


def get_cfg(name2block):
    """Given in name2block map, produce a mapping from block names to
       successor block names."""
    out = {}

    for index, (name, block) in enumerate(name2block.items()):
        last = block[-1]
        if last['op'] in ('jmp', 'br'):
            succ = last['labels']
        elif last['op'] == 'ret':
            succ = []
        else:
            if index == len(name2block) - 1:
                succ = []
            else:
                succ = [list(name2block.keys())[index+1]]

        out[name] = succ
    return out

def dce(block, is_single_bb):
    used = []
    last_def = {}
    BlockChanged = 1
    
    while BlockChanged:
        index, BlockChanged = 0 , 0
        blockLength = len(block)
        while index < blockLength:
            instr = block[index]
            if "dest" in instr:
                if instr["dest"] in last_def and instr["dest"] not in used:
                    index -= 1
                    blockLength -= 1
                    block.remove(last_def[instr["dest"]])
                last_def[instr["dest"]] = instr
    
            if "args" in instr:
                for arg in instr["args"]:
                    used.append(arg)
            index += 1
   
        for instr in block:
            if "dest" in instr and instr["dest"] not in used and is_single_bb:
                block.remove(instr)
                BlockChanged = 1
        used.clear()
        last_def.clear()



def runOptimization(name2block):
    """Run Optimizations"""

    for name, block in name2block.items():
        is_single_bb = len(name2block.items()) == 1
        dce(block, is_single_bb)



def run():
    #program = json.load(sys.stdin)
    
    program = json.load(open('temp.json',))

    for func in program['functions']:
        name2block = block_map(form_blocks(func['instrs']))
        cfg = get_cfg(name2block)
        
        print("Before Optimizations, Block:")
        for name, block in name2block.items():
            print(name, ' -> ', block)
        
        runOptimization(name2block)
        
        print("")
        print("")
        print("After Optimizations, Block:")
        for name, block in name2block.items():
            print(name, ' -> ', block)
        
    
    

if __name__ == "__main__":
    run()
