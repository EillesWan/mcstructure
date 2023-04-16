from TrimMCStruct import Structure

p = input("path:")
with open(p, "rb") as f:
    struct = Structure.load(f)


with open("output.mcstructure", "wb") as f:
    struct.dump(f)
