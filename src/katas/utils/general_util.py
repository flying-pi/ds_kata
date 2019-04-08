import tensorflow as tf

def tf_namespace(func, name = None):
    if name is None:
        name = func.__name__
    def result(*args, **kwargs):
        with tf.name_scope(name):
            return func(*args, **kwargs)

    return result