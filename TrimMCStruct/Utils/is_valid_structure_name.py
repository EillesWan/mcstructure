def is_valid_structure_name(name: str, *, with_prefix: bool = False) -> bool:
    """
    Validates the structure name.

    .. seealso: https://minecraft.fandom.com/wiki/Structure_Block

    Parameters
    ----------
    name
        The name of the structure.

    with_prefix
        Whether to take the prefix (e.g. ``mystructure:``)
        into account.
    """
    if with_prefix:
        name = name.replace(":", "", 1)

    return all((char.isalnum() and char in "-_") for char in name)
