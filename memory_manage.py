
def getPointerAddr(mem,base,offsets):
    addr = mem.read_int(base)
    for offset in offsets:
        if offset != offsets[-1]:
            addr = mem.read_int(addr + offset)
    addr = addr + offsets[-1]
    return addr
# class pointer():
#     def __init__(self, mem, base, offsets, dtype):
#         if(dtype == "int"):
#             self.point = mem.read_int(getPointerAddr(mem,base,offsets))
#         elif(dtype == "float"):
#             self.point = mem.read_float(getPointerAddr(mem,base,offsets))