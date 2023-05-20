from typing import Any
from pynbt import BaseTag, TAG_Compound, TAG_Int, TAG_List, TAG_String, TAG_Byte


def _into_tag(obj: Any) -> BaseTag:
    """
    Turn a python tree into an NBT tree.
    """
    if isinstance(obj, (TAG_Compound, dict)):
        res = {}
        for key, value in obj.items():
            if not isinstance(value, BaseTag):
                value = _into_tag(value)
            res[key] = value
        return TAG_Compound(res)

    elif isinstance(obj, (TAG_List, list)):
        res = []
        for value in obj:
            if not isinstance(value, BaseTag):
                value = _into_tag(value)
            res.append(value)
        return TAG_List(
            tag_type=(type(_into_tag(obj[0])) if obj else TAG_String), value=res
        )

    elif isinstance(obj, bool):
        return TAG_Byte(obj)

    elif isinstance(obj, int):
        return TAG_Int(obj)

    elif isinstance(obj, str):
        return TAG_String(obj)

    return obj
