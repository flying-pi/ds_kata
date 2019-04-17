import argparse
from pathlib import Path


import numpy as np
import pandas as pd


def parabola(x):
    return x ** 2


def add_noise(data: np.ndarray) -> np.ndarray:
    delta = (data.max() - data.min()) / 20
    return data + np.random.uniform(-delta, delta, data.shape[0])


def generate_set(x_range, function=parabola, random_level=0.02, set_size=1000):
    x_range = np.random.uniform(*x_range, set_size)
    y = function(x_range)
    return pd.DataFrame(data={'feature': add_noise(x_range), 'value': add_noise(y)})


def main():
    parser = argparse.ArgumentParser(
        description='Generate csv file with data for regression'
    )
    parser.add_argument(
        '--random_level', action="store", dest="random_level", type=float, default=0.05,
        help='level of the noise'
    )
    parser.add_argument(
        '--set_size', action="store", dest="set_size", type=float, default=1000,
        help='Count samples in the df'
    )
    parser.add_argument('--out_file', action="store", dest="out_file", type=str, help='output file size')
    parser.add_argument(
        '--x', action="store", dest="x_diapason", type=str, default='0;10',
        help='set diapason of the X in next format `min;max`'
    )
    arg = parser.parse_args()

    df = generate_set(
        [int(i) for i in arg.x_diapason.split(';')],
        lambda x: x * 2.2 + 3.2,
        arg.random_level,
        arg.set_size
    )
    Path('/'.join(arg.out_file.split('/')[:-1])).mkdir(parents=True, exist_ok=True)
    df.to_csv(arg.out_file, index=False)


if __name__ == '__main__':
    main()
