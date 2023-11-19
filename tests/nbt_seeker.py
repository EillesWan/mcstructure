
'''This is only for seeing what shall be inside a .mcstructure file'''

from rich.console import Console
from typing import Any, Literal, Optional, TextIO


JustifyMethod = Literal["default", "left", "center", "right", "full"]
OverflowMethod = Literal["fold", "crop", "ellipsis", "ignore"]


MainConsole = Console()



def format_ipt(
    notice: str,
    fun,
    err_note: str = "",
    *extraArg,
):
    """循环输入，以某种格式
    notice: 输入时的提示
    fun: 格式函数
    err_note: 输入不符格式时的提示
    *extraArg: 对于函数的其他参数"""
    while True:
        MainConsole.print(notice,style="#F0F2F4 on #121110",)
        result = MainConsole.input()
        # noinspection PyBroadException
        try:
            fun_result = fun(result, *extraArg)
            break
        # noinspection PyBroadException
        except BaseException:
            MainConsole.print(err_note,style="#F0F2F4 on #121110",)
            continue
    return result, fun_result


import json
from typing import Any, BinaryIO, Optional, Tuple

import numpy as np
from numpy.typing import NDArray
from pynbt import BaseTag, NBTFile, TAG_Compound, TAG_Int, TAG_List, TAG_String, TAG_Byte,TAG_Long  # type: ignore

import os

file_path = format_ipt("file_path: ",os.path.exists,"Err: not found")[0]

with open(file_path,'rb+') as f:
    nbt = NBTFile(f, little_endian=True)

from TrimMCStruct.main import nbtag_into_pyobj

MainConsole.print(nbtag_into_pyobj(nbt),style="#F0F2F4 on #121110",)

# def deep(sth):
#     if type(sth) == TAG_List:
#         return [deep(i) for i in sth]
#     elif type(sth) == TAG_Compound:
#         return dict(zip(sth.keys(),[deep(i) for i in sth.values()]))
#     else:
#         return sth
    

# prt(deep(dict(zip(nbt.keys(),[deep(i) for i in nbt.values()]))))


