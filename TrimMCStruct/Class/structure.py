from ..constant import Coordinate, COMPABILITY_VERSION
from ..Utils.into_pyobj import _into_pyobj
from ..Utils.into_tag import _into_tag

from .block import Block

from functools import partial
from itertools import repeat
from numpy.typing import NDArray
from pynbt import NBTFile, TAG_Compound, TAG_Int, TAG_List, TAG_String
from typing import Any, BinaryIO, Optional, Dict

import numpy as np


class Structure:
    """
    Class representing a Minecraft structure that
    consists of blocks and entities.

    Attributes
    ----------
    size
        The size of the structure.
    """

    structure_indecis: NDArray[np.intc]

    def __init__(
        self,
        size: tuple[int, int, int],
        fill: Optional[Block] = None,
        compability_version: int = COMPABILITY_VERSION,
    ):
        """
        Parameters
        ----------
        size
            The size of the structure.

        fill
            Fill the structure with this block at
            creation of a new structure object.

            However, extra datas of blocks cannot be filled.

            If this is set to ``None`` the structure
            is filled with "Structure Void" blocks.

            "None" is used as default.
        """

        self.structure_indecis: NDArray[np.intc]

        self._size = size
        self._palette: list[Block] = []
        self._special_blocks: Dict[int, Dict] = {}

        if fill is None:
            self.structure_indecis = np.full(size, -1, dtype=np.intc)

        else:
            self.structure_indecis = np.zeros(size, dtype=np.intc)
            self._palette.append(fill)

        self.compability_version = compability_version

    @classmethod
    def load(cls, file: BinaryIO):
        """
        Loads an mcstructure file.

        Parameters
        ----------
        file
            File object to read.
        """
        nbt = NBTFile(file, little_endian=True)
        size: tuple[int, int, int] = tuple(
            x.value for x in nbt["size"])

        struct = cls(size)

        # see https://wiki.bedrock.dev/nbt/mcstructure.html
        # of a .mcstructure file's NBT format
        # while Chinese developers could see my translation at
        # ../docs/mcstructure%E6%96%87%E4%BB%B6%E7%BB%93%E6%9E%84.md

        struct.structure_indecis = np.array(
            [_into_pyobj(x) for x in nbt["structure"]["block_indices"][0]],
            dtype=np.intc,
        ).reshape(size)

        struct._palette.extend(
            [
                Block.from_identifier(
                    block["name"].value,
                    **_into_pyobj(block["states"].value),
                    compability_version=_into_pyobj(block["version"]),
                )
                for block in nbt["structure"]["palette"]["default"]["block_palette"]
            ]
        )

        for block_index, block_extra_data in nbt["structure"]["palette"]["default"][
            "block_position_data"
        ].items():
            struct._special_blocks[int(block_index)] = _into_pyobj(
                block_extra_data)

        return struct

    @property
    def size(self) -> tuple[int, int, int]:
        return self._size

    def __repr__(self) -> str:
        return repr(self._get_str_array())

    def __str__(self) -> str:
        return str(self._get_str_array())

    def _get_str_array(
        self, *, with_namespace: bool = False, with_states: bool = False
    ) -> NDArray[Any]:
        """
        Returns a numpy array where each entry is a
        readable string of the corresponding block.

        Parameters
        ----------
        with_namespace
            Adds the namespace to the string if present.

        with_states
            Adds the block states to the string if present.
        """
        arr = self.get_structure().copy()
        vec = np.vectorize(
            partial(
                Block.stringify, with_namespace=with_namespace, with_states=with_states
            )
        )
        return vec(arr)

    def _add_block_to_palette(self, block: Optional[Block]) -> int:
        """
        Adds a block to the palette.

        Parameters
        ----------
        block
            The block to add. If this is set to ``None``
            "Structure Void" will be used.

        Returns
        -------
        The position of the block in the palette. This is
        ``-1`` when ``None`` is used as ``block``.
        """
        if block is None:
            return -1

        same_block = block.clear_extra_data()
        if same_block in self._palette:
            return self._palette.index(same_block)

        self._palette.append(same_block)
        return len(self._palette) - 1

    def dump(self, file: BinaryIO) -> None:
        """
        Serialize the structure as a ``mcstructure``.

        Parameters
        ----------
        file
            File object to write to.
        """
        NBTFile(
            value=dict(
                format_version=TAG_Int(1),
                size=TAG_List(TAG_Int, map(TAG_Int, self._size)),
                structure=TAG_Compound(
                    dict(
                        block_indices=TAG_List(
                            TAG_List,
                            [
                                TAG_List(
                                    TAG_Int,
                                    map(TAG_Int, self.structure_indecis.flatten()),
                                ),
                                TAG_List(
                                    TAG_Int,
                                    map(
                                        TAG_Int, repeat(-1,
                                                        self.structure_indecis.size)
                                    ),
                                ),
                            ],
                        ),
                        entities=TAG_List(TAG_Compound, []),
                        palette=TAG_Compound(
                            dict(
                                default=TAG_Compound(
                                    dict(
                                        block_palette=TAG_List(
                                            TAG_Compound,
                                            [
                                                TAG_Compound(
                                                    dict(
                                                        name=TAG_String(
                                                            block.identifier
                                                        ),
                                                        states=TAG_Compound(
                                                            {
                                                                state_name: _into_tag(
                                                                    state_value
                                                                )
                                                                for state_name, state_value in block.states.items()
                                                            }
                                                        ),
                                                        version=TAG_Int(
                                                            block.compability_version
                                                        ),
                                                    )
                                                )
                                                for block in self._palette
                                            ],
                                        ),
                                        block_position_data=TAG_Compound(
                                            dict(
                                                sorted(
                                                    [
                                                        (
                                                            str(block_index),
                                                            _into_tag(
                                                                extra_data),
                                                        )
                                                        for block_index, extra_data in self._special_blocks.items()
                                                    ],
                                                    key=lambda a: a[0],
                                                )
                                            )
                                        ),
                                    )
                                )
                            )
                        ),
                    )
                ),
                structure_world_origin=TAG_List(TAG_Int, [0, 0, 0]),
            ),
            little_endian=True,
        ).save(file, little_endian=True)

    def mirror(self, axis: str):
        """
        Flips the structure.

        Parameters
        ----------
        axis
            Turn the structure either the ``X`` or ``Z`` axis.
            Use ``"X"``, ``"x"``,``"Z"`` or ``"z"``.
        """
        if axis in "Xx":
            self.structure_indecis = self.structure_indecis[::-1, :, :]
        elif axis in "Zz":
            self.structure_indecis = self.structure_indecis[:, :, ::-1]
        else:
            raise ValueError(f"invalid argument for 'rotation' ({axis!r})")
        return self

    def rotate(self, by: int):
        """
        Rotates the structure.

        Parameters
        ----------
        by
            Rotates the structure by ``90``, ``180``
            or ``270`` degrees.
        """
        if by == 90:
            self.structure_indecis = np.rot90(
                self.structure_indecis, k=1, axes=(0, 1))
        elif by == 180:
            self.structure_indecis = np.rot90(
                self.structure_indecis, k=2, axes=(0, 1))
        elif by == 270:
            self.structure_indecis = np.rot90(
                self.structure_indecis, k=3, axes=(0, 1))
        else:
            raise ValueError(f"invalid argument for 'by' ({by!r})")
        return self

    def get_block(self, coordinate: Coordinate) -> Optional[Block]:
        """
        Returns the block in a specific position.

        Parameters
        ----------
        coordinate
            The coordinte of the block.
        """
        x, y, z = coordinate
        block = self._palette[self.structure_indecis[x, y, z]].copy()
        block_index = x * self.size[2] * self.size[1] + y * self.size[2] + z
        if block_index in self._special_blocks.keys():
            block.add_extra_data(self._special_blocks[block_index])
        return block

    def get_structure(self) -> NDArray[Any]:
        """
        Returns the structure as a numpy array filled
        with the corresponding `Block` objects.
        """
        arr = np.full(
            self.structure_indecis.shape,
            Block(
                "minecraft",
                "structure_void",
                compability_version=self.compability_version,
            ),
            dtype=object,
        )
        for key, block in enumerate(self._palette):
            arr[self.structure_indecis == key] = block

        for index, exdata in self._special_blocks.items():
            arr[int(index / (self.size[2] * self.size[1]))][
                int(index % (self.size[2] * self.size[1]) / self.size[2])
            ][
                (index % (self.size[2] * self.size[1]) % self.size[2])
            ].extra_data = exdata

        return arr

    def set_block(
        self,
        coordinate: Coordinate,
        block: Optional[Block],
    ):
        """
        Puts a block into the structure.

        Parameters
        ----------
        coordinate
            Relative coordinates of the block's position.

        block
            The block to place. If this is set to ``None``
            "Structure Void" blocks will be used.
        """
        x, y, z = coordinate

        ident = self._add_block_to_palette(block)

        self.structure_indecis[x, y, z] = ident
        if block.extra_data:  # type: ignore
            self._special_blocks[
                x * self.size[2] * self.size[1] + y * self.size[2] + z
            ] = block.extra_data  # type: ignore
        return self

    def fill_blocks(
        self,
        from_coordinate: Coordinate,
        to_coordinate: Coordinate,
        block: Block,
    ):
        """
        Puts multiple blocks into the structure.

        Notes
        -----
        Both start and end points are filled.

        Parameters
        ----------
        from_coordinate
            Relative coordinates of the start corner.

        to_coordinate
            Relative coordinates of the end corner.

        block
            The block to place. If this is set to ``None``
            "STructure Void" blocks will be used to fill.
        """
        fx, fy, fz = from_coordinate
        tx, ty, tz = to_coordinate

        ident = self._add_block_to_palette(block)

        # print([[[ident for k in range(abs(fz-tz)+1) ]for j in range(abs(fy-ty)+1)]for i in range(abs(fx-tx)+1)])
        self.structure_indecis[fx: tx + 1, fy: ty + 1, fz: tz + 1] = np.array(
            [
                [
                    [ident for k in range(abs(fz - tz) + 1)]
                    for j in range(abs(fy - ty) + 1)
                ]
                for i in range(abs(fx - tx) + 1)
            ],
            dtype=np.intc,
        ).reshape([abs(i) + 1 for i in (fx - tx, fy - ty, fz - tz)])

        if block.extra_data:
            self._special_blocks.update(
                dict(
                    zip(
                        [
                            (x * self.size[2] * self.size[1] +
                             y * self.size[2] + z)
                            for x in range(fx, tx)
                            for y in range(fy, ty)
                            for z in range(fz, tz)
                        ],
                        [
                            block.extra_data
                            for i in range(
                                abs((fz - tz) + 1)
                                * (abs(fy - ty) + 1)
                                * (abs(fx - tx) + 1)
                            )
                        ],
                    )
                )
            )
        return self
