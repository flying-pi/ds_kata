from unittest import TestCase
import tensorflow as tf

class TreeTest(TestCase):

    def test_get_split(self):
        import pydevd
        pydevd.settrace('docker.for.mac.localhost', port=3758, stdoutToServer=True, stderrToServer=True)
        print('hello')
        assert True

