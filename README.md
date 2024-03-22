# ExpLog - A Minimal Experiment Logger

## Installation

```sh
pip install explog
```

## Logging

Use `exp = explog.exp(config)` to initialize an experiment and `exp.log(...)` to log statistics.

```python3
import explog as xl
import random

config = {'num_epochs': 100, 'learning_rate': 1e-3, 'batch_size': 32}

exp = xl.exp(config)

for epoch in range(config['num_epochs']):
    loss = random.random() * 1.05 ** (- epoch)
    exp.log(epoch=epoch, loss=loss)
```

## Exploring runs

Retrieve dataframe of experiments using `explog.exps()`.

```ipython
> import explog as xl
> xl.exps()
          num_epochs  learning_rate  batch_size
_id
w1gf6deg         100          0.001          32
6mwn9cno         100          0.001          32
hdakmy0l         100          0.001          32
```

## Exploring logs

Retrieve dataframe of logs using `explog.logs()`.

```ipython
> import explog as xl
> xl.logs()
                epoch      loss  num_epochs  learning_rate  batch_size
_id      _step
w1gf6deg 0          0  0.901695         100          0.001          32
         1          1  0.676328         100          0.001          32
         2          2  0.194963         100          0.001          32
         3          3  0.345743         100          0.001          32
         4          4  0.645544         100          0.001          32
...               ...       ...         ...            ...         ...
hdakmy0l 95        95  0.003342         100          0.001          32
         96        96  0.000132         100          0.001          32
         97        97  0.003763         100          0.001          32
         98        98  0.008314         100          0.001          32
         99        99  0.004589         100          0.001          32
```

## Plotting

Use dataframe of logs from `explog.logs()` to make your plots.

```python3
import explog as xl
import matplotlib.pyplot as plt

logs = xl.logs('epoch', 'loss')
logs = logs.groupby('epoch').mean()

plt.plot(logs.index, logs['loss'])
plt.show()
```
