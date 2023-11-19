"""
Read and write Minecraft .mcstructure files.
"""

# TODO: coordinates might be in wrong order (XYZ -> ZYX)
# TODO: make Structure._structure public
# TODO: test mirror
# TODO: test rotate
# TODO: second layer (waterlogged blocks)
# TODO: entities
# TODO: export as 3d model (might be extension)

from __future__ import annotations

from functools import partial
from itertools import repeat
from typing import Any, BinaryIO, Callable, Optional, Tuple, Union, Dict, AnyStr, List

import numpy as np
from numpy.typing import NDArray
import nbtlib

from .main import Block, MatrixStructure,COMPABILITY_VERSION,Coordinate,pyobj_into_nbttag


class mcStructure(MatrixStructure):
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
        self._palette: List[Block] = []
        self._special_blocks: Dict[int, Dict] = {}

        if fill is None:
            self.structure_indecis = np.full(size, nbtlib.Int(-1), dtype=np.intc)

        else:
            self.structure_indecis = np.zeros(size, dtype=np.intc)
            self._palette.append(fill)

        self.compability_version = compability_version

    @classmethod
    def loadf(cls, file_path: AnyStr):
        with open(
            file_path,
            "rb",
        ) as f:
            return cls.load(f)

    @classmethod
    def load(cls, file_: BinaryIO):
        """
        Loads an mcstructure file.

        Parameters
        ----------
        file
            File object to read.
        """
        nbt = nbtlib.File.from_fileobj(file_, byteorder="little")
        size: tuple[int, int, int] = (nbt["size"][0], nbt["size"][1], nbt["size"][2])

        struct = cls(size)

        # see https://wiki.bedrock.dev/nbt/mcstructure.html
        # of a .mcstructure file's NBT format
        # while Chinese developers could see my translation at
        # ../docs/mcstructure%E6%96%87%E4%BB%B6%E7%BB%93%E6%9E%84.md

        struct.structure_indecis = np.array(
            nbt["structure"]["block_indices"][0],
            dtype=np.intc,
        ).reshape(size)

        struct._palette.extend(
            [
                Block.from_identifier(
                    block["name"],
                    **block["states"],
                    compability_version=block["version"],
                )
                for block in nbt["structure"]["palette"]["default"]["block_palette"]
            ]
        )

        for block_index, block_extra_data in nbt["structure"]["palette"]["default"][
            "block_position_data"
        ].items():
            struct._special_blocks[int(block_index)] = block_extra_data

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

    def nbtfilize(
        self,
    ) -> nbtlib.File:
        return nbtlib.File(
            dict(
                format_version=nbtlib.Int(1),
                size=pyobj_into_nbttag(self._size),
                structure=nbtlib.Compound(
                    block_indices=nbtlib.List(
                        [
                            pyobj_into_nbttag(
                                self.structure_indecis.flatten(),
                            ),
                            nbtlib.List(
                                list(
                                    repeat(nbtlib.Int(-1), self.structure_indecis.size),
                                ),
                            ),
                        ],
                    ),
                    entities=nbtlib.List([]),
                    palette=nbtlib.Compound(
                        default=nbtlib.Compound(
                            block_palette=nbtlib.List(
                                [
                                    pyobj_into_nbttag(block.dictionarify())
                                    for block in self._palette
                                ],
                            ),
                            block_position_data=pyobj_into_nbttag(
                                self._special_blocks, sort_=lambda a: a[0]
                            ),
                        )
                    ),
                ),
                structure_world_origin=pyobj_into_nbttag((0, 0, 0)),
            ),
            gzipped=False,
            byteorder="little",
        )

    def dumpf(self, file_path: AnyStr) -> None:
        """
        Serialize the structure as a file.

        Parameters
        ----------
        file_path
            File path to write to.
        """
        self.nbtfilize().save(file_path, byteorder="little", gzipped=False)

    def dump(self, file_: BinaryIO) -> None:
        """
        Serialize the structure as a ``mcstructure`` file.

        Parameters
        ----------
        file
            File object to write to.
        """
        self.nbtfilize().write(file_, byteorder="little")

    def mirror(self, axis: str) -> MatrixStructure:
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
        elif axis in "Yy":
            self.structure_indecis = self.structure_indecis[:, ::-1, :]
        else:
            raise ValueError(f"invalid argument for 'rotation' ({axis!r})")
        return self

    def rotate(self, by: int) -> MatrixStructure:
        """
        Rotates the structure.

        Parameters
        ----------
        by
            Rotates the structure by ``90``, ``180``
            or ``270`` degrees.
        """
        if by == 90:
            self.structure_indecis = np.rot90(self.structure_indecis, k=1, axes=(0, 1))
        elif by == 180:
            self.structure_indecis = np.rot90(self.structure_indecis, k=2, axes=(0, 1))
        elif by == 270:
            self.structure_indecis = np.rot90(self.structure_indecis, k=3, axes=(0, 1))
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
    ) -> MatrixStructure:
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
        if block:
            if block.extra_data:
                self._special_blocks[
                    x * self.size[2] * self.size[1] + y * self.size[2] + z
                ] = block.extra_data
        return self

    def fill_blocks(
        self,
        from_coordinate: Coordinate,
        to_coordinate: Coordinate,
        block: Optional[Block],
    ) -> MatrixStructure:
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
        self.structure_indecis[fx : tx + 1, fy : ty + 1, fz : tz + 1] = np.array(
            [
                [
                    [ident for k in range(abs(fz - tz) + 1)]
                    for j in range(abs(fy - ty) + 1)
                ]
                for i in range(abs(fx - tx) + 1)
            ],
            dtype=np.intc,
        ).reshape([abs(i) + 1 for i in (fx - tx, fy - ty, fz - tz)])

        if block:
            if block.extra_data:
                self._special_blocks.update(
                    dict(
                        zip(
                            [
                                (x * self.size[2] * self.size[1] + y * self.size[2] + z)
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
