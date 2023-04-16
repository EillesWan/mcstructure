[int]: https://wiki.bedrock.dev/assets/images/nbt/int.png
[string]: https://wiki.bedrock.dev/assets/images/nbt/string.png
[list]: https://wiki.bedrock.dev/assets/images/nbt/list.png
[compound]: https://wiki.bedrock.dev/assets/images/nbt/compound.png



# 目录
- [`目录`](#目录)
- [`说明`](#说明)
- [`.Mcstructure 文件结构`](#mcstructure-文件结构)
- [`代码样例`](#代码样例)
    - [`样例 Ⅰ`](#样例-ⅰ)
    - [`样例 Ⅱ`](#样例-ⅱ)
    - [`样例 Ⅱ`](#样例-ⅲ)


# 说明
- 来源
    - 此文档译自 https://wiki.bedrock.dev/nbt/mcstructure.html _[有部分改动]_
- 编撰
    - 译者 —— _@EillesWan_
    - 修订 —— _@Happy2018new_
- 版式
    - 当前为第 `2` 版



# `.Mcstructure` 文件结构



`mcstructure` 文件是未经压缩的 [`NBT` 文件](https://wiki.vg/NBT#Specification)，也正如 `《我的世界：基岩版》` 的所有 `NBT` 文件一样，其皆以 `小端字节序`（又称 `小端序`）存储。以下是此类文件的 `NBT 标签` 结构。



- ![int] `整型(TAG_Int32) - format_version` —— 当前总为 `1`



- ![list] `列表(TAG_List) - size` —— 是一个 `整数列表(TAG_List[TAG_Int32])` ，用于表示 `结构` 的 `尺寸` ，即 `大小`
    - ![int] `整型(TAG_Int32)` —— `结构` 在 `X` 轴的 `尺寸`
    - ![int] `整型(TAG_Int32)` —— `结构` 在 `Y` 轴的 `尺寸`
    - ![int] `整型(TAG_Int32)` —— `结构` 在 `Z` 轴的 `尺寸`



- ![compound] `复合(TAG_Compound) - structure` —— 实际存储结构的数据组
   - ![list] `列表(TAG_List) - block_indices`
        > 1. `structure` 表示结构中存储的 `方块索引` 。
        > 2. 此索引表一共包含两个 `列表` ，第一个 `列表` 为实际 `方块` 数据，第二个 `列表` 对应第一个 `列表` 中 `方块` 在 `内含层(Second Layer)` 的 `方块` 数据。
        > 3. 每一个 `方块` 都以一个 `整型` 数据来表示，而它对应 `方块池(palette)` 中的 `索引下标(Index)` 。
        > 4. `方块` 通过一个 `一维` 的 `密集矩阵(亦称“列表”)` 来存储。`结构` 中每个 `方块` 按照 `Z` 轴到 `Y` 轴到 `X` 轴且均沿轴正方向的顺序一字排开形成 `列表` 。
        > 5. 例如，若 `结构尺寸(结构大小)` 为 `[2,3,4]`，则每一层(即包括 `内含层(Second Layer)` 也是一样的顺序)的 `24` 个方块(这个数量是由 `结构尺寸(结构大小)` 决定的，也就是 `结构尺寸(结构大小)` 所表示的 `体积`)分别对应着如下 `相对坐标` 位置的 `方块` 。<br/>
        > `[(0,0,0), (0,0,1), (0,0,2), (0,0,3), (0,1,0), (0,1,1), (0,1,2), (0,1,3), (0,2,0), (0,2,1), (0,2,2), (0,2,3), (1,0,0), (1,0,1), (1,0,2), (1,0,3), (1,1,0), (1,1,1), (1,1,2), (1,1,3), (1,2,0), (1,2,1), (1,2,2), (1,2,3)]`
        > 6. 若 `索引下标(Index)` 为 `-1` 则表示此处不存在 `方块` (对应 `结构空位`)。因此，该处在 `结构` 被加载时就会保留其原有 `方块` 而不会发生替换。我们用 `结构方块` 保存 `结构` 时很容易出现这样的现象，另外，对于表示 `方块` 的 `内含层(Second Layer)` 的列表，其中所记录的 `整型值` 也大多指代 `无方块(结构空位)` 。
        > 7. 两个层的 `方块` 共享一个 `方块池(palette)` 。<br/>
        - ![list] `of` ![int] `整型列表(TAG_List[TAG_Int32])` —— `首层(Primary Layer)` 方块列表
        - ![list] `of` ![int] `整型列表(TAG_List[TAG_Int32])` —— `内含层(Second Layer)` 方块列表。此层通常为空，但若您存储的是《白蛇传》中的水漫金山场景就另当别论了

    - ![compound] `复合(TAG_Compound) - entities` —— 以 `NBT` 存储的实体列表，其存储格式与在地图文件中存储 `实体` 的形式一致。类似 `Pos` 与 `UniqueID` 这样的独立于不同世界中的 `标签` 亦会被保存下来，但是 `《我的世界》` 加载这样的标签时会将它们 `覆写` 为实际值

    - ![compound] `复合(TAG_Compound) - palette` —— 理论上可以包含多种不同名字的 `方块池(palette)` ，似乎这样设计是可能要支持以后的对于同一种 `结构` 的变体形态。但需要说明的是，目前游戏内仅保存和加载名称为 `default` 的 `方块池`
        - ![compound] `复合(TAG_Compound) - default`
            - ![list] `列表(TAG_List) - block_palette` —— 包含 `方块` 及其 `方块状态(Block State)` 的 `列表` ，即包含了 `方块索引block_indices[0~1]` 中那些 `索引下标(index)` 所指代的 `方块`
                - ![compound] `复合(TAG_Compound)` —— 单 `方块` 及其 `方块状态(Block States)`
                    - ![string] `字符串(TAG_String) - name` —— `方块 ID (identifier)` ，形如 `minecraft:planks`
                    - ![compound] `复合(TAG_Compound) - states` —— `方块状态(Block States)`，以 `键值对` 的形式出现，形如 `"wood_type": "acacia"`、`wood_type: "acacia"`、`bite_counter: 3` 和 `open_bit: 1b` 。
                        - 其 `值` 将转换为有效的 `NBT 标签` ，以下是一些 `转换规则`
                            - `枚举值(Enum Values)` 将被转换为 `字符串(TAG_String)`
                            - `标量(Scalar Numbers)` 将被转换为 `整型(TAG_Int32)`
                            - `布尔值(Boolean Values)` 会被转为 `字节型(TAG_Byte)`
                    - ![int] `整型(TAG_Int32) - version` —— 指代 `兼容版本(Compatibility Versioning Number)`
                        - 此文撰写时所对应的版本号是 `17959425` ，即游戏版本 `1.19`
            - ![compound] `复合(TAG_Compound) - block_position_data` —— 包含 `结构` 中各个 `方块` 的 `附加数据(Additional Data)` 。每一个 `键(Key)` 皆为`block_indices` 中 `下标索引(index)` 所对应的方块，数据类型当然为 `整型(TAG_Int32)` 。此处不会保有多层方块的指代，因为这个字段可以在 `值(Value)` 中被描述
                - ![compound] `复合(TAG_Compound) - 方块索引(Index)值` —— 相应 `方块` 的 `附加数据(Additional Data)`
                    - ![compound] `复合(TAG_Compound) - block_entity_data` ——  以 `NBT` 存储的 `方块实体` 数据(`block entity data`)，其存储格式与在地图文件中存储实体的形式一致。同上述 `实体标签` 的理，其 `位置标签(Position Tag)` 亦会被保存下来，但是 `《我的世界》` 加载这样的标签时会将它们覆写为实际 `值` 。不过这时候也不会有其他什么东西跟这玩意手拉手出现了 _[译注：此处原文为 `No other objects seem to exist adjacent to this one at this time.` ，应该是说，与 `entities` 那么多其他的独立于各个世界的标签相比，在 `方块实体` 中的算少的了]_
                    - ![compound] `复合(TAG_Compound)` —— 这些是 `键` 名不为 `block_entity_data` 的 `复合(TAG_Compound)` 。它们将可能用于 `计划刻` 等数据 _[需要验证]_ 。对于 `命令方块` 来说，它将会是一个用于记录下次执行命令的时刻的数据(仅 `延迟型命令方块`)。该字段在一般情况下不会存在



- ![list] `列表(TAG_List) - structure_world_origin` —— `结构` 最初保存时的 `起始点坐标(Origin Position)` ，以三个 `整型(TAG_Int32)` 组成的 `列表` 的形式来体现。 `坐标` 的值对应 `结构方块` 保存时的 `坐标` 加上我们在 `结构方块` 里填写的 `偏移量` 。此 `坐标` 用于 计算(确定) `实体` 在被加载时所生成的位置，它等于 `实体` 原本在 `结构` 中存储的 `原始坐标` 减去 `结构` 最初保存时的 `起始点坐标(Origin Position)` 再加上 `加载起始点` 的 `坐标`
    - ![int] `整型(TAG_Int32)` —— `结构` 原本的 `X` 轴坐标
    - ![int] `整型(TAG_Int32)` —— `结构` 原本的 `Y` 轴坐标
    - ![int] `整型(TAG_Int32)` —— `结构` 原本的 `Z` 轴坐标



# 代码样例
_Code Provider - @EillesWan_

以下是一些例子(以 `Python` 的数据结构为模拟)。

## 样例 Ⅰ
```python
# 大小为 1x3x1 (XYZ) 的
# 从下往上分别是一个指令方块、一个铁块和一个空气方块的
# 结构 NBT 数据
{
    'format_version': TAG_Int(1, 'format_version'),
    'size': [TAG_Int(1, None), TAG_Int(3, None), TAG_Int(1, None)],
    'structure': {
        'block_indices': [
            [TAG_Int(0, None), TAG_Int(1, None), TAG_Int(2, None)],
            [TAG_Int(-1, None), TAG_Int(-1, None), TAG_Int(-1, None)]
        ],
        'entities': [],
        'palette': {
            'default': {
                'block_palette': [
                    {
                        'name': TAG_String('minecraft:command_block', 'name'),
                        'states': {
                            'conditional_bit': TAG_Byte(0, 'conditional_bit'),
                            'facing_direction': TAG_Int(1, 'facing_direction')
                        },
                        'version': TAG_Int(17959425, 'version')
                    },
                    {
                        'name': TAG_String('minecraft:iron_block', 'name'),
                        'states': {},
                        'version': TAG_Int(17959425, 'version')
                    },
                    {
                        'name': TAG_String('minecraft:air', 'name'),
                        'states': {},
                        'version': TAG_Int(17959425, 'version')
                    }
                ],
                'block_position_data': {
                    '0': {
                            'Command': TAG_String('help 4', 'Command'),
                            'CustomName': TAG_String('', 'CustomName'),
                            'ExecuteOnFirstTick': TAG_Byte(0, 'ExecuteOnFirstTick'),
                            'LPCommandMode': TAG_Int(0, 'LPCommandMode'),
                            'LPCondionalMode': TAG_Byte(0, 'LPCondionalMode'),
                            'LPRedstoneMode': TAG_Byte(0, 'LPRedstoneMode'),
                            'LastExecution': TAG_Long(0, 'LastExecution'),
                            'LastOutput': TAG_String('', 'LastOutput'),
                            'LastOutputParams': [],
                            'SuccessCount': TAG_Int(0, 'SuccessCount'),
                            'TickDelay': TAG_Int(0, 'TickDelay'),
                            'TrackOutput': TAG_Byte(1, 'TrackOutput'),
                            'Version': TAG_Int(25, 'Version'),
                            'auto': TAG_Byte(0, 'auto'),
                            'conditionMet': TAG_Byte(0, 'conditionMet'),
                            'conditionalMode': TAG_Byte(0, 'conditionalMode'),
                            'id': TAG_String('CommandBlock', 'id'),
                            'isMovable': TAG_Byte(1, 'isMovable'),
                            'powered': TAG_Byte(0, 'powered'),
                            'x': TAG_Int(1, 'x'),
                            'y': TAG_Int(1, 'y'),
                            'z': TAG_Int(1, 'z')
                        }
                }
            }
        }
    },
    'structure_world_origin': [TAG_Int(0, None), TAG_Int(0, None), TAG_Int(0, None)],
}
```



## 样例 Ⅱ
```python
# 大小为 2x2x2 (XYZ) 的
# 全是白色羊毛的
# 结构 NBT 数据
{
    'format_version': TAG_Int(1, 'format_version'),
    'size': [TAG_Int(2, None), TAG_Int(2, None), TAG_Int(2, None)],
    'structure': {
        'block_indices': [
            [
                TAG_Int(0, None),
                TAG_Int(0, None),
                TAG_Int(0, None),
                TAG_Int(0, None),
                TAG_Int(0, None),
                TAG_Int(0, None),
                TAG_Int(0, None),
                TAG_Int(0, None)
            ],
            [
                TAG_Int(-1, None),
                TAG_Int(-1, None),
                TAG_Int(-1, None),
                TAG_Int(-1, None),
                TAG_Int(-1, None),
                TAG_Int(-1, None),
                TAG_Int(-1, None),
                TAG_Int(-1, None)
            ]
        ],
        'entities': [],
        'palette': {
            'default': {
                'block_palette': [
                    {
                        'name': TAG_String('minecraft:wool', 'name'),
                        'states': {'color': TAG_String('white', 'color')},
                        'version': TAG_Int(17959425, 'version')
                    }
                ],
                'block_position_data': {}
            }
        }
    },
    'structure_world_origin': [TAG_Int(0, None), TAG_Int(0, None), TAG_Int(0, None)]
}
```


## 样例 Ⅲ
```python
# 大版本 1.19 
# 一个竖列放置9个指令方块
# 分别为 脉冲无条件红石驱动 脉冲有条件始终执行 脉冲无条件始终执行 剩下六个以此类推为链式和循环的
# 从下往上前四个朝上放置，从上往下四个朝下放置，中间的朝着X轴正方向
{
    'format_version': TAG_Int(1, 'format_version'),
    'size': [TAG_Int(1, None), TAG_Int(9, None), TAG_Int(1, None)],
    'structure': {
        'block_indices': [
            [
                TAG_Int(0, None),
                TAG_Int(1, None),
                TAG_Int(0, None),
                TAG_Int(2, None),
                TAG_Int(3, None),
                TAG_Int(4, None),
                TAG_Int(5, None),
                TAG_Int(6, None),
                TAG_Int(5, None)
            ],
            [
                TAG_Int(-1, None),
                TAG_Int(-1, None),
                TAG_Int(-1, None),
                TAG_Int(-1, None),
                TAG_Int(-1, None),
                TAG_Int(-1, None),
                TAG_Int(-1, None),
                TAG_Int(-1, None),
                TAG_Int(-1, None)
            ]
        ],
        'entities': [],
        'palette': {
            'default': {
                'block_palette': [
                    {
                        'name': TAG_String('minecraft:command_block', 'name'),
                        'states': {
                            'conditional_bit': TAG_Byte(0, 'conditional_bit'),
                            'facing_direction': TAG_Int(1, 'facing_direction')
                        },
                        'version': TAG_Int(18040335, 'version')
                    },
                    {
                        'name': TAG_String('minecraft:command_block', 'name'),
                        'states': {
                            'conditional_bit': TAG_Byte(1, 'conditional_bit'),
                            'facing_direction': TAG_Int(1, 'facing_direction')
                        },
                        'version': TAG_Int(18040335, 'version')
                    },
                    {
                        'name': TAG_String('minecraft:chain_command_block', 'name'),
                        'states': {
                            'conditional_bit': TAG_Byte(0, 'conditional_bit'),
                            'facing_direction': TAG_Int(1, 'facing_direction')
                        },
                        'version': TAG_Int(18040335, 'version')
                    },
                    {
                        'name': TAG_String('minecraft:chain_command_block', 'name'),
                        'states': {
                            'conditional_bit': TAG_Byte(1, 'conditional_bit'),
                            'facing_direction': TAG_Int(5, 'facing_direction')
                        },
                        'version': TAG_Int(18040335, 'version')
                    },
                    {
                        'name': TAG_String('minecraft:chain_command_block', 'name'),
                        'states': {
                            'conditional_bit': TAG_Byte(0, 'conditional_bit'),
                            'facing_direction': TAG_Int(0, 'facing_direction')
                        },
                        'version': TAG_Int(18040335, 'version')
                    },
                    {
                        'name': TAG_String('minecraft:repeating_command_block', 'name'),
                        'states': {
                            'conditional_bit': TAG_Byte(0, 'conditional_bit'),
                            'facing_direction': TAG_Int(0, 'facing_direction')
                        },
                        'version': TAG_Int(18040335, 'version')
                    },
                    {
                        'name': TAG_String('minecraft:repeating_command_block', 'name'),
                        'states': {
                            'conditional_bit': TAG_Byte(1, 'conditional_bit'),
                            'facing_direction': TAG_Int(0, 'facing_direction')
                        },
                        'version': TAG_Int(18040335, 'version')
                    }
                ],
                'block_position_data': {
                    '0': {
                        'block_entity_data': {
                            'Command': TAG_String('', 'Command'),
                            'CustomName': TAG_String('', 'CustomName'),
                            'ExecuteOnFirstTick': TAG_Byte(0, 'ExecuteOnFirstTick'),
                            'LPCommandMode': TAG_Int(0, 'LPCommandMode'),
                            'LPCondionalMode': TAG_Byte(0, 'LPCondionalMode'),
                            'LPRedstoneMode': TAG_Byte(0, 'LPRedstoneMode'),
                            'LastExecution': TAG_Long(0, 'LastExecution'),
                            'LastOutput': TAG_String('', 'LastOutput'),
                            'LastOutputParams': [],
                            'SuccessCount': TAG_Int(0, 'SuccessCount'),
                            'TickDelay': TAG_Int(0, 'TickDelay'),
                            'TrackOutput': TAG_Byte(1, 'TrackOutput'),
                            'Version': TAG_Int(32, 'Version'),
                            'auto': TAG_Byte(0, 'auto'),
                            'conditionMet': TAG_Byte(0, 'conditionMet'),
                            'conditionalMode': TAG_Byte(0, 'conditionalMode'),
                            'id': TAG_String('CommandBlock', 'id'),
                            'isMovable': TAG_Byte(1, 'isMovable'),
                            'powered': TAG_Byte(0, 'powered'),
                            'x': TAG_Int(0, 'x'),
                            'y': TAG_Int(-60, 'y'),
                            'z': TAG_Int(0, 'z')
                        }
                    },
                    '1': {
                        'block_entity_data': {
                            'Command': TAG_String('', 'Command'),
                            'CustomName': TAG_String('', 'CustomName'),
                            'ExecuteOnFirstTick': TAG_Byte(0, 'ExecuteOnFirstTick'),
                            'LPCommandMode': TAG_Int(0, 'LPCommandMode'),
                            'LPCondionalMode': TAG_Byte(0, 'LPCondionalMode'),
                            'LPRedstoneMode': TAG_Byte(0, 'LPRedstoneMode'),
                            'LastExecution': TAG_Long(0, 'LastExecution'),
                            'LastOutput': TAG_String('', 'LastOutput'),
                            'LastOutputParams': [],
                            'SuccessCount': TAG_Int(0, 'SuccessCount'),
                            'TickDelay': TAG_Int(0, 'TickDelay'),
                            'TrackOutput': TAG_Byte(1, 'TrackOutput'),
                            'Version': TAG_Int(32, 'Version'),
                            'auto': TAG_Byte(1, 'auto'),
                            'conditionMet': TAG_Byte(0, 'conditionMet'),
                            'conditionalMode': TAG_Byte(1, 'conditionalMode'),
                            'id': TAG_String('CommandBlock', 'id'),
                            'isMovable': TAG_Byte(1, 'isMovable'),
                            'powered': TAG_Byte(0, 'powered'),
                            'x': TAG_Int(0, 'x'),
                            'y': TAG_Int(-59, 'y'),
                            'z': TAG_Int(0, 'z')
                        }
                    },
                    '2': {
                        'block_entity_data': {
                            'Command': TAG_String('', 'Command'),
                            'CustomName': TAG_String('', 'CustomName'),
                            'ExecuteOnFirstTick': TAG_Byte(0, 'ExecuteOnFirstTick'),
                            'LPCommandMode': TAG_Int(0, 'LPCommandMode'),
                            'LPCondionalMode': TAG_Byte(0, 'LPCondionalMode'),
                            'LPRedstoneMode': TAG_Byte(0, 'LPRedstoneMode'),
                            'LastExecution': TAG_Long(0, 'LastExecution'),
                            'LastOutput': TAG_String('', 'LastOutput'),
                            'LastOutputParams': [],
                            'SuccessCount': TAG_Int(0, 'SuccessCount'),
                            'TickDelay': TAG_Int(0, 'TickDelay'),
                            'TrackOutput': TAG_Byte(1, 'TrackOutput'),
                            'Version': TAG_Int(32, 'Version'),
                            'auto': TAG_Byte(1, 'auto'),
                            'conditionMet': TAG_Byte(0, 'conditionMet'),
                            'conditionalMode': TAG_Byte(0, 'conditionalMode'),
                            'id': TAG_String('CommandBlock', 'id'),
                            'isMovable': TAG_Byte(1, 'isMovable'),
                            'powered': TAG_Byte(0, 'powered'),
                            'x': TAG_Int(0, 'x'),
                            'y': TAG_Int(-58, 'y'),
                            'z': TAG_Int(0, 'z')
                        }
                    },
                    '3': {
                        'block_entity_data': {
                            'Command': TAG_String('', 'Command'),
                            'CustomName': TAG_String('', 'CustomName'),
                            'ExecuteOnFirstTick': TAG_Byte(0, 'ExecuteOnFirstTick'),
                            'LPCommandMode': TAG_Int(0, 'LPCommandMode'),
                            'LPCondionalMode': TAG_Byte(0, 'LPCondionalMode'),
                            'LPRedstoneMode': TAG_Byte(0, 'LPRedstoneMode'),
                            'LastExecution': TAG_Long(0, 'LastExecution'),
                            'LastOutput': TAG_String('', 'LastOutput'),
                            'LastOutputParams': [],
                            'SuccessCount': TAG_Int(0, 'SuccessCount'),
                            'TickDelay': TAG_Int(0, 'TickDelay'),
                            'TrackOutput': TAG_Byte(1, 'TrackOutput'),
                            'Version': TAG_Int(32, 'Version'),
                            'auto': TAG_Byte(0, 'auto'),
                            'conditionMet': TAG_Byte(0, 'conditionMet'),
                            'conditionalMode': TAG_Byte(0, 'conditionalMode'),
                            'id': TAG_String('CommandBlock', 'id'),
                            'isMovable': TAG_Byte(1, 'isMovable'),
                            'powered': TAG_Byte(0, 'powered'),
                            'x': TAG_Int(0, 'x'),
                            'y': TAG_Int(-57, 'y'),
                            'z': TAG_Int(0, 'z')
                        }
                    },
                    '4': {
                        'block_entity_data': {
                            'Command': TAG_String('', 'Command'),
                            'CustomName': TAG_String('', 'CustomName'),
                            'ExecuteOnFirstTick': TAG_Byte(0, 'ExecuteOnFirstTick'),
                            'LPCommandMode': TAG_Int(0, 'LPCommandMode'),
                            'LPCondionalMode': TAG_Byte(0, 'LPCondionalMode'),
                            'LPRedstoneMode': TAG_Byte(0, 'LPRedstoneMode'),
                            'LastExecution': TAG_Long(0, 'LastExecution'),
                            'LastOutput': TAG_String('', 'LastOutput'),
                            'LastOutputParams': [],
                            'SuccessCount': TAG_Int(0, 'SuccessCount'),
                            'TickDelay': TAG_Int(0, 'TickDelay'),
                            'TrackOutput': TAG_Byte(1, 'TrackOutput'),
                            'Version': TAG_Int(32, 'Version'),
                            'auto': TAG_Byte(1, 'auto'),
                            'conditionMet': TAG_Byte(0, 'conditionMet'),
                            'conditionalMode': TAG_Byte(1, 'conditionalMode'),
                            'id': TAG_String('CommandBlock', 'id'),
                            'isMovable': TAG_Byte(1, 'isMovable'),
                            'powered': TAG_Byte(0, 'powered'),
                            'x': TAG_Int(0, 'x'),
                            'y': TAG_Int(-56, 'y'),
                            'z': TAG_Int(0, 'z')
                        }
                    },
                    '5': {
                        'block_entity_data': {
                            'Command': TAG_String('', 'Command'),
                            'CustomName': TAG_String('', 'CustomName'),
                            'ExecuteOnFirstTick': TAG_Byte(0, 'ExecuteOnFirstTick'),
                            'LPCommandMode': TAG_Int(0, 'LPCommandMode'),
                            'LPCondionalMode': TAG_Byte(0, 'LPCondionalMode'),
                            'LPRedstoneMode': TAG_Byte(0, 'LPRedstoneMode'),
                            'LastExecution': TAG_Long(0, 'LastExecution'),
                            'LastOutput': TAG_String('', 'LastOutput'),
                            'LastOutputParams': [],
                            'SuccessCount': TAG_Int(0, 'SuccessCount'),
                            'TickDelay': TAG_Int(0, 'TickDelay'),
                            'TrackOutput': TAG_Byte(1, 'TrackOutput'),
                            'Version': TAG_Int(32, 'Version'),
                            'auto': TAG_Byte(1, 'auto'),
                            'conditionMet': TAG_Byte(0, 'conditionMet'),
                            'conditionalMode': TAG_Byte(0, 'conditionalMode'),
                            'id': TAG_String('CommandBlock', 'id'),
                            'isMovable': TAG_Byte(1, 'isMovable'),
                            'powered': TAG_Byte(0, 'powered'),
                            'x': TAG_Int(0, 'x'),
                            'y': TAG_Int(-55, 'y'),
                            'z': TAG_Int(0, 'z')
                        }
                    },
                    '6': {
                        'block_entity_data': {
                            'Command': TAG_String('', 'Command'),
                            'CustomName': TAG_String('', 'CustomName'),
                            'ExecuteOnFirstTick': TAG_Byte(1, 'ExecuteOnFirstTick'),
                            'LPCommandMode': TAG_Int(0, 'LPCommandMode'),
                            'LPCondionalMode': TAG_Byte(0, 'LPCondionalMode'),
                            'LPRedstoneMode': TAG_Byte(0, 'LPRedstoneMode'),
                            'LastExecution': TAG_Long(0, 'LastExecution'),
                            'LastOutput': TAG_String('', 'LastOutput'),
                            'LastOutputParams': [],
                            'SuccessCount': TAG_Int(0, 'SuccessCount'),
                            'TickDelay': TAG_Int(0, 'TickDelay'),
                            'TrackOutput': TAG_Byte(1, 'TrackOutput'),
                            'Version': TAG_Int(32, 'Version'),
                            'auto': TAG_Byte(0, 'auto'),
                            'conditionMet': TAG_Byte(0, 'conditionMet'),
                            'conditionalMode': TAG_Byte(0, 'conditionalMode'),
                            'id': TAG_String('CommandBlock', 'id'),
                            'isMovable': TAG_Byte(1, 'isMovable'),
                            'powered': TAG_Byte(0, 'powered'),
                            'x': TAG_Int(0, 'x'),
                            'y': TAG_Int(-54, 'y'),
                            'z': TAG_Int(0, 'z')
                        }
                    },
                    '7': {
                        'block_entity_data': {
                            'Command': TAG_String('', 'Command'),
                            'CustomName': TAG_String('', 'CustomName'),
                            'ExecuteOnFirstTick': TAG_Byte(1, 'ExecuteOnFirstTick'),
                            'LPCommandMode': TAG_Int(0, 'LPCommandMode'),
                            'LPCondionalMode': TAG_Byte(0, 'LPCondionalMode'),
                            'LPRedstoneMode': TAG_Byte(0, 'LPRedstoneMode'),
                            'LastExecution': TAG_Long(0, 'LastExecution'),
                            'LastOutput': TAG_String('', 'LastOutput'),
                            'LastOutputParams': [],
                            'SuccessCount': TAG_Int(0, 'SuccessCount'),
                            'TickDelay': TAG_Int(0, 'TickDelay'),
                            'TrackOutput': TAG_Byte(1, 'TrackOutput'),
                            'Version': TAG_Int(32, 'Version'),
                            'auto': TAG_Byte(1, 'auto'),
                            'conditionMet': TAG_Byte(0, 'conditionMet'),
                            'conditionalMode': TAG_Byte(1, 'conditionalMode'),
                            'id': TAG_String('CommandBlock', 'id'),
                            'isMovable': TAG_Byte(1, 'isMovable'),
                            'powered': TAG_Byte(0, 'powered'),
                            'x': TAG_Int(0, 'x'),
                            'y': TAG_Int(-53, 'y'),
                            'z': TAG_Int(0, 'z')
                        },
                        'tick_queue_data': [{'tick_delay': TAG_Int(0, 'tick_delay')}]
                    },
                    '8': {
                        'block_entity_data': {
                            'Command': TAG_String('', 'Command'),
                            'CustomName': TAG_String('', 'CustomName'),
                            'ExecuteOnFirstTick': TAG_Byte(1, 'ExecuteOnFirstTick'),
                            'LPCommandMode': TAG_Int(0, 'LPCommandMode'),
                            'LPCondionalMode': TAG_Byte(0, 'LPCondionalMode'),
                            'LPRedstoneMode': TAG_Byte(0, 'LPRedstoneMode'),
                            'LastExecution': TAG_Long(0, 'LastExecution'),
                            'LastOutput': TAG_String('', 'LastOutput'),
                            'LastOutputParams': [],
                            'SuccessCount': TAG_Int(0, 'SuccessCount'),
                            'TickDelay': TAG_Int(0, 'TickDelay'),
                            'TrackOutput': TAG_Byte(1, 'TrackOutput'),
                            'Version': TAG_Int(32, 'Version'),
                            'auto': TAG_Byte(1, 'auto'),
                            'conditionMet': TAG_Byte(1, 'conditionMet'),
                            'conditionalMode': TAG_Byte(0, 'conditionalMode'),
                            'id': TAG_String('CommandBlock', 'id'),
                            'isMovable': TAG_Byte(1, 'isMovable'),
                            'powered': TAG_Byte(0, 'powered'),
                            'x': TAG_Int(0, 'x'),
                            'y': TAG_Int(-52, 'y'),
                            'z': TAG_Int(0, 'z')
                        },
                        'tick_queue_data': [{'tick_delay': TAG_Int(0, 'tick_delay')}]
                    }
                }
            }
        }
    },
    'structure_world_origin': [TAG_Int(0, None), TAG_Int(-60, None), TAG_Int(0, None)]
}
```