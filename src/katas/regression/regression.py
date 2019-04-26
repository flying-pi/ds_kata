import pandas as pd
import tensorflow as tf


class Regression:

    learning_theta = None

    def __init__(self, feature_count: int, epoch_count = 1000, learning_rate=0.01) -> None:
        super().__init__()
        self._learning_rate = learning_rate
        self._epoch_count = epoch_count
        self.activation_function = self._liner_activation_function
        self._feature_count = feature_count


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
        import pydevd
        pydevd.settrace('host.docker.internal', port=3758, stdoutToServer=True, stderrToServer=True)

        m, n = x.shape
        x['bais'] = 1

        self.x = tf.placeholder(tf.float32, shape=(None, self._feature_count+1))
        self.y = tf.placeholder(tf.float32, shape=(1, self._feature_count))
        self.theta = self._get_theta()
        self.predict = self.activation_function(self.x, self.theta)
        self.error = self.predict - self.y
        self.mse = tf.reduce_mean(tf.square(self.error), name='mse')
        self.gradient  = 2/m * tf.matmul(tf.transpose(self.x), self.error)
        self.train_operation = tf.assign(self.theta, self.theta - self._learning_rate * self.gradient)
        init = tf.global_variables_initializer()

        with tf.Session() as sess:
            sess.run(init, feed_dict={self.x: x, self.y: y})

            for i in range(self._epoch_count):
                sess.run(self.train_operation)

            best_theta = self.theta.eval()

    def get_prediction(self, features:pd.DataFrame):
        pass
