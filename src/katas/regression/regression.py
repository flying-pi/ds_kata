import pandas as pd
import tensorflow as tf


class Regression:

    learning_theta = None

    def __init__(self, feature_count: int, epoch_count = 1000, learning_rate=0.01) -> None:
        super().__init__()
        self._learning_rate = learning_rate
        self._epoch_count = epoch_count
        self.activation_function = self._liner_activation_function
        import pydevd
        pydevd.settrace('docker.for.mac.localhost', port=3758, stdoutToServer=True, stderrToServer=True)
        self._feature_count = feature_count

        self.x = tf.placeholder(tf.float32, shape=(None, self._feature_count))
        self.y = tf.placeholder(tf.float32, shape=(1, self._feature_count))
        self.theta = self._get_theta()
        self.predict = self.activation_function(self.x, self.theta)
        self.error = self.predict - self.y
        self.mse = tf.reduce_mean(tf.square(self.error), name='mse')
        self.gradient  = 2/tf.shape(self.x)[0] * tf.matmul(tf.transpose(self.x), self.error)
        self.train_operation = tf.assign(self.theta, self.theta - self._learning_rate * self.gradient)


    @staticmethod
    def _liner_activation_function(x, theta):
        return  tf.matmul(x, theta, name= 'prediction')

    def _get_theta(self):
        if self.learning_theta:
            return self.learning_theta
        else:
            return tf.Variable(
                tf.random_uniform([tf.shape(self.x)[0], 1], -1., 1.),
                name="theta",
                validate_shape=False
            )

    def fit(self, x: pd.DataFrame, y: pd.DataFrame):
        m, n = x.shape
        x['bais'] = 1
