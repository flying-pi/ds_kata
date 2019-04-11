import pandas as pd
import tensorflow as tf


class Regression:

    def __init__(self, feature_count: int) -> None:
        super().__init__()
        import pydevd
        pydevd.settrace('docker.for.mac.localhost', port=3758, stdoutToServer=True, stderrToServer=True)
        self._feature_count = feature_count

    def _build_learning_flow(self):
        x = tf.placeholder(tf.float32, shape=(None, self._feature_count))
        y = tf.placeholder(tf.float32, shape=(1, self._feature_count))
        theta = tf.Variable(tf.random_uniform([tf.shape(x)[0], 1], -1., 1.), name="theta", validate_shape=False)
        predict = tf.matmul(x, theta, name= 'prediction')
        error = predict - y



    def fit(self, x: pd.DataFrame, y: pd.DataFrame):
        m, n = x.shape
        x['bais'] = 1
