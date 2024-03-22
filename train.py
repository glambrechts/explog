import random
import explog as xl
import matplotlib.pyplot as plt

from argparse import ArgumentParser


def main(args):
    exp = xl.exp(config=args)

    for epoch in range(args.num_epochs):
        loss = random.random() * (1.05 ** (- epoch))
        metric = random.random()
        exp.log(epoch=epoch, loss=loss, metric=metric)

    if args.plot:
        df = exp.logs('epoch', 'loss')
        df.plot('epoch', 'loss')
        plt.show()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--plot', action='store_true')

    parser.add_argument('--num_epochs', type=int, default=100)
    parser.add_argument('--learning_rate', type=float, default=1e-3)
    parser.add_argument('--batch_size', type=int, default=32)

    args = parser.parse_args()
    main(args)
