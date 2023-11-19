from TrimMCStruct import mcStructure

p = input("path:")
with open(p, "rb") as f:
    struct = mcStructure.load(f)


with open("output.mcstructure", "wb") as f:
    struct.dump(f)
