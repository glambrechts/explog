import time
import explog as xl


def main():
    t1 = time.perf_counter()
    exps = xl.exps()
    t2 = time.perf_counter()
    print(f"{len(exps):,.0f} exps loaded in {t2-t1:.4f}s")

    t1 = time.perf_counter()
    logs = xl.logs('epoch', 'loss')
    t2 = time.perf_counter()
    print(f"{len(logs):,.0f} logs loaded in {t2-t1:.4f}s")


if __name__ == '__main__':
    main()
