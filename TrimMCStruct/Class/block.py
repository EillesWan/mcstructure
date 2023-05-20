from ..constant import COMPABILITY_VERSION

from dataclasses import dataclass
from json import dumps
from typing import Any, Optional, Tuple, Union, Dict


@dataclass(init=False)
class Block:
    """
    Attributes
    ----------
    base_name
        The name of the block.

    states
        The states of the block.

    Example
    -------
    .. code-block::

        Block("minecraft:wool", color = "red")
    """

    namespace: str
    base_name: str
    states: dict[str, Union[int, str, bool]]
    extra_data: dict[str, Union[int, str, bool]]

    def __init__(
        self,
        namespace: str,
        base_name: str,
        states: dict[str, Union[int, str, bool]] = {},
        extra_data: dict[str, Union[int, str, bool]] = {},
        compability_version: int = COMPABILITY_VERSION,
    ):
        """
        Parameters
        ----------
        namespace: str
            The namespace of the block (e.g. "minecraft").
        base_name: str
            The name of the block (e.g. "air").

        states
            The block states such as {'color': 'white'} or {"stone_type":1}.
            This varies by every block.

        extra_data
            [Optional] The additional data of the block.

        compability_version: int
            [Optional] The compability version of the block, now(1.19) is 17959425
        """
        self.namespace = namespace
        self.base_name = base_name
        self.states = states
        self.extra_data = extra_data
        self.compability_version = compability_version

    @classmethod
    def from_identifier(
        cls,
        identifier: str,
        compability_version: int = COMPABILITY_VERSION,
        **states: Union[int, str, bool],
    ):
        """
        Parameters
        ----------
        identifier: str
            The identifier of the block (e.g. "minecraft:wool").

        compability_version: int
            [Optional] The compability version of the block, now(1.19) is 17959425

        states:
            The block states such as "color" or "stone_type".
            This varies by every block.
        """

        if ":" in identifier:
            namespace, base_name = identifier.split(":", 1)
        else:
            namespace = "minecraft"
            base_name = identifier

        block = cls(
            namespace, base_name, states, compability_version=compability_version
        )

        return block

    def __str__(self) -> str:
        return self.stringify()

    def __dict__(self) -> dict:
        return self.dictionarify()

    def add_states(
        self,
        states: dict[str, Union[int, str, bool]],
    ) -> None:
        self.states.update(states)

    def add_extra_data(
        self,
        extra_data: dict[str, Union[int, str, bool]],
    ) -> None:
        self.extra_data.update(extra_data)

    def dictionarify(self, *, with_states: bool = True) -> Dict[str, Any]:
        result = {
            "name": self.identifier,
            "states": self.states if with_states else {},
            "version": self.compability_version,
        }

        return result

    def dictionarify_with_block_entity(
        self, *, with_states: bool = True
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        result = {
            "name": self.identifier,
            "states": self.states if with_states else {},
            "version": self.compability_version,
        }

        return result, self.extra_data

    def stringify(
        self,
        *,
        with_namespace: bool = True,
        with_states: bool = True,
    ) -> str:
        result = ""
        if with_namespace:
            result += self.namespace + ":"
        result += self.get_name()
        if with_states:
            result += f" [{dumps(self.states)[1:-1]}]"
        return result

    def get_namespace_and_name(self) -> tuple[str, str]:
        """
        Returns the namespace and the name of the block.
        """
        return self.namespace, self.base_name

    def get_identifier(self) -> str:
        """
        Returns the identifier of the block.
        """
        return self.namespace + ":" + self.base_name

    def get_name(self) -> str:
        """
        Returns the name of the block.
        """
        return self.base_name

    def get_namespace(self) -> Optional[str]:
        """
        Returns the namespace of the block.
        """
        return self.namespace

    @property
    def identifier(self) -> str:
        """
        The identifier of the block.
        """
        return self.get_identifier()

    def __eq__(self, obj) -> bool:
        if isinstance(obj, Block):
            if self.dictionarify() == obj.dictionarify():
                return True

        return False

    def copy(self):
        return Block(
            namespace=self.namespace,
            base_name=self.base_name,
            states=self.states,
            extra_data=self.extra_data,
            compability_version=self.compability_version,
        )

    def clear_extra_data(self):
        another_self = self.copy()
        another_self.extra_data = {}
        return another_self
