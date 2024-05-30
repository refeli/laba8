from dataloader.coinbaseloader import CoinbaseLoader, Granularity
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import os
import yaml
import logging.config
from datetime import datetime

def setup_logging(path='logger.yml', level=logging.INFO, env_key='LOG_CONFIG'):
    path = os.getenv(env_key, path)
    if (os.path.exists(path)):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)

def main():
    loader = CoinbaseLoader()
    df_1 = loader.get_historical_data("btc-usdt", "2023-01-01", "2023-01-02", Granularity.FIVE_MINUTES)
    df_2 = loader.get_historical_data("sol-usdt", "2023-01-01", "2023-01-02", Granularity.FIVE_MINUTES)
    df_3 = loader.get_historical_data("near-usdt", "2023-01-01", "2023-01-02", Granularity.FIVE_MINUTES)
    df_1['Середні20'] = df_1['close'].rolling(window=20).mean()
    df_1['Середні50'] = df_1['close'].rolling(window=50).mean()
    
    df_2['Середні20'] = df_2['close'].rolling(window=20).mean()
    df_2['Середні50'] = df_2['close'].rolling(window=50).mean()

    df_3['Середні20'] = df_3['close'].rolling(window=20).mean()
    df_3['Середні50'] = df_3['close'].rolling(window=50).mean()

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
    fig.set_figwidth(14)
    fig.set_figheight(7)

    ax1.plot(df_1.close, label='Ціна закриття')
    ax1.plot(df_1.Середні20, label='Середня 20 днів')
    ax1.plot(df_1.Середні50, label='Середня 50 днів')
    ax1.grid()

    ax2.plot(df_2.close, label='Ціна закриття')
    ax2.plot(df_2.Середні20, label='Середня 20 днів')
    ax2.plot(df_2.Середні50, label='Середня 50 днів')
    ax2.grid()

    ax3.plot(df_3.close, label='Ціна закриття')
    ax3.plot(df_3.Середні20, label='Середня 20 днів')
    ax3.plot(df_3.Середні50, label='Середня 50 днів')
    ax3.grid()

    plt.show()

    df = pd.merge(df_1, pd.merge(df_2, df_3, left_index=True, right_index=True), left_index=True, right_index=True)

    cm = df[['close_x', 'close_y']].corr()
    sns.heatmap(cm, annot=True)
    plt.show()

    df_1['ЛР'] = np.log(df_1.close/df_1.close.shift(1))
    plt.plot(df_1.ЛР)
    plt.grid()
    plt.show()

    print(f"волатильність: {df_1.ЛР.std():0.4f}")

    df_2['ЛР'] = np.log(df_2.close/df_2.close.shift(1))
    plt.plot(df_2.ЛР)
    plt.grid()
    plt.show()

    print(f"волатильність: {df_2.ЛР.std():0.4f}")

    df_3['ЛР'] = np.log(df_3.close/df_3.close.shift(1))
    plt.plot(df_3.ЛР)
    plt.grid()
    plt.show()
    print(f"волатильність: {df_3.ЛР.std():0.4f}")

if __name__ == "__main__":
    setup_logging()
    main()
