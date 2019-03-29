import pandas as pd
import tensorflow as tf

class DecissionTree:
    def __init__(self, dataset:pd.DataFrame) -> None:
        self.dataset = dataset

    def _get_split(self, dataset):
