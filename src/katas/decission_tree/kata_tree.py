import numpy as np
import pandas as pd


class DecisionTree:
    def __init__(self, dataset: pd.DataFrame, class_column: str) -> None:
        self.dataset = dataset
        self.class_column = class_column
        self.tree = self._build_tree()
        self.query = self._build_query()

    @staticmethod
    def _entropy(group: pd.Series) -> float:
        total_size = len(group)
        result = 0
        for i in set(group):
            p = sum(group == i) / total_size
            result += p * np.log(p)
        return -result

    def _get_best_split_fol_col(self, input_df: pd.DataFrame, column_name: str, subset_len: int):
        input_df = input_df.sort_values(by=[column_name]).reset_index(drop=True)
        classes = input_df[self.class_column]

        min_error = 1
        split_pos = -1
        for i in range(0, len(classes)):
            if i == 0 or classes[i] == classes[i - 1]:
                continue

            w = i / subset_len
            current_error = w * self._entropy(classes[:i]) + (1 - w) * self._entropy(classes[i:])
            if current_error < min_error:
                min_error = current_error
                split_pos = i

        return min_error, input_df[column_name][split_pos]

    def _get_split(self, input_df):
        current_entropy = self._entropy(input_df[self.class_column])
        df_len = len(input_df)
        best_column = ""
        best_split = None
        best_gain = -1
        for c in input_df.columns:
            if c == self.class_column:
                continue
            df = input_df[[c, self.class_column]]
            error, split_value = self._get_best_split_fol_col(df, c, df_len)
            current_gain = current_entropy - error
            if current_gain > best_gain:
                best_gain = current_gain
                best_column = c
                best_split = split_value

        return best_column, best_split

    def _build_tree(self, df=None):
        if df is None:
            df = self.dataset

        class_set = set(df[self.class_column])
        if len(class_set) == 1:
            return {
                'leaf': True,
                'value': class_set.pop()
            }
        col, value = self._get_split(df)
        return {
            'leaf': False,
            'col': col,
            'value': value,
            'left': self._build_tree(df[df[col] < value]),
            'right': self._build_tree(df[df[col] >= value]),
        }

    def _build_query(self):
        query_tuple_list = self._tree_to_query()
        result = {}
        for equation, value in query_tuple_list:
            str_equation = ' and '.join(equation)
            if value not in result:
                result[value] = str_equation
            else:
                result[value] = f'{result[value]} or ({str_equation})'
        return result

    def _tree_to_query(self, tree=None, query=None):
        if tree is None:
            tree = self.tree

        if query is None:
            query = []

        if tree['leaf']:
            return [(query, tree['value'])]
        return [
            *self._tree_to_query(tree['left'], [*query, f"({tree['col']} < {tree['value']})"]),
            *self._tree_to_query(tree['right'], [*query, f"({tree['col']} >= {tree['value']})"]),
        ]

    def predict(self, dataset:pd.DataFrame) -> pd.Series:
        result = pd.Series([None]*len(dataset))
        for equation, class_label in self.query.items():
            result[dataset.query(equation).index]=class_label
        return result
