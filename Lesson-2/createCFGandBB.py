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
        else:   # A Label.
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

def mycfg():
    program = json.load(sys.stdin)

    for func in program['functions']:
        name2block = block_map(form_blocks(func['instrs']))

        for name, block in name2block.items():
            print(name)
            print('     ', block)
        cfg = get_cfg(name2block)
        
        print(cfg)




if __name__ == "__main__":
    mycfg()
