
from TrimMCStruct import Structure

with open(input(),'rb',) as f:
    struct = Structure.load(f)

# display stuffs in it  显示一些东西
print(struct._special_blocks)
print("\n\n")
print(struct.get_structure())