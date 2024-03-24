import explog as xl
import matplotlib.pyplot as plt


def main():
    logs = xl.logs('epoch', 'loss', num_epochs=100)
    logs = logs.groupby('epoch').agg(['mean', 'median', 'std', 'min', 'max'])

    fig, ax = plt.subplots()
    ax.plot(logs.index, logs.loss['median'])
    ax.fill_between(logs.index, logs.loss['min'], logs.loss['max'], alpha=0.2)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
