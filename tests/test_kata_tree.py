from unittest.mock import MagicMock

import numpy as np
import pandas as pd
import pytest
import pytest as pt

from katas.decission_tree.kata_tree import DecisionTree


@pytest.mark.parametrize(
    'input_df, expected_result',
    [
        (pd.Series([1, 1, ]), 0),
        (pd.Series([1, 1, -1]), 0.63),
    ]
)
def test_entropy(input_df, expected_result):
    assert expected_result == pt.approx(DecisionTree._entropy(input_df), rel=1e-1)

def test_get_split():
    input_data = np.array(
        [
            [41, 1, 0],
            [-1, 1, 0],
            [12, 2, 1],
            [-4, 2, 0],
            [42, 3, 1],
            [55, 1, 0],
        ]
    )
    input_df = pd.DataFrame(data=input_data, columns=['a', 'b', 'class'])
    tree = DecisionTree(input_df, 'class')
    expected_tree = {
        'leaf': False, 'col': 'b', 'value': 2,
        'left': {'leaf': True, 'value': 0},
        'right': {
            'leaf': False, 'col': 'a', 'value': 12,
            'left': {'leaf': True, 'value': 0},
            'right': {'leaf': True, 'value': 1}
        }
    }
    assert tree.tree == expected_tree
