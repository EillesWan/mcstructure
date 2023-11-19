from TrimMCStruct import mcStructure

with open(input("path:"), "rb") as f:
    struct = mcStructure.load(f)

print(struct)
print(struct.size)
