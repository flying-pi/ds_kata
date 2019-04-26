from sklearn.model_selection import train_test_split

from src.katas.regression.regression import Regression
from src.katas.regression.utils.liner_regression_generator import generate_set

import numpy as np
import pandas as pd


def test_base_liner_regression():
    """
    Functional test for base implementation of the linear regression.
    """
    function = lambda x: 2*x+10
    set = generate_set([-10, 10], function, random_level=0.1, set_size=1000)
    regression = Regression(feature_count=1)
    regression.fit(set[['feature']], set[['value']])
    input_x = np.random.uniform(-100, 100, 100)
    expected_y = [function(x) for x in input_x]
    predict_result = regression.get_prediction(pd.DataFrame(input_x))
    score = np.abs(predict_result-expected_y)