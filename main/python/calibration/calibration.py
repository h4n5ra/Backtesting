import queue
import numpy as np

from threading import Thread
from trade.simple_strats import above_under_ma_std


def calibrate_std(df, threaded=True):
    results = {}
    stds = list(np.arange(0, 2, 0.25))

    if threaded:
        threads = []
        for std in stds:
            thread = Thread(target=_store_in_dict, args=(results, std, above_under_ma_std, df, std, 14, False, False))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
    else:
        for std in stds:
            results[std] = above_under_ma_std(df, std, 14, False, False)

    date = str(df.iloc[-1].Date).split()[0]
    pnls = list(results.values())
    best_std = stds[pnls.index(max(pnls))]
    print('best std value for {} is {} which returned {}%'.format(date, best_std, results[best_std]))
    return best_std


def _store_in_dict(dict, key, func, *args):
    dict[key] = func(*args)
