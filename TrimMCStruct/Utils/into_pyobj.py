from typing import Any
from pynbt import BaseTag, TAG_Compound, TAG_List


def _into_pyobj(tag: BaseTag) -> Any:
    """
    Turns an NBT tree into a python tree.
    """
    if isinstance(tag, (TAG_Compound, dict)):
        res = {}
        for key, value in tag.items():
            if isinstance(value, BaseTag):
                value = _into_pyobj(value)
            res[key] = value
        return res

    elif isinstance(tag, (TAG_List, list)):
        res = []
        for value in tag:
            if isinstance(value, BaseTag):
                value = _into_pyobj(value)
            res.append(value)
        return res

    elif isinstance(tag, BaseTag):
        return tag.value

    return tag
