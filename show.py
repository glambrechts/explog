import explog
import matplotlib.pyplot as plt

from argparse import ArgumentParser


def main(args):
    df = explog.logs('epoch', 'loss', num_epochs=100)
    df = df.groupby('epoch').agg(['mean', 'median', 'std', 'min', 'max'])

    fig, ax = plt.subplots()
    ax.plot(df.index, df.loss['median'])
    ax.fill_between(df.index, df.loss['min'], df.loss['max'], alpha=0.2)
    plt.show()


if __name__ == '__main__':
    parser = ArgumentParser()
    args = parser.parse_args()
    main(args)
