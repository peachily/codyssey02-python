import pandas as pd

ATTR_FILE = 'abalone_attributes.txt'
DATA_FILE = 'abalone.txt'


def load_attributes(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            attributes = [line.strip() for line in f.readlines()]
        return attributes
    except FileNotFoundError:
        raise FileNotFoundError('File open error.')
    except UnicodeError:
        raise UnicodeError('Decoding error.')

def load_data(path, columns):
    try:
        df = pd.read_csv(path, header=None, names=columns)
        return df
    except FileNotFoundError:
        raise FileNotFoundError('File open error.')
    except Exception as e:
        raise ValueError(f'Processing error: {e}')


def minmax_manual_scale(df):
    # scaled_df = df.copy()
    numeric_cols = df.select_dtypes(include='number').columns

    for col in numeric_cols:
        min_val = df[col].min()
        max_val = df[col].max()
        range_val = max_val - min_val

        if range_val == 0:
            df[col] = 0.0
        else:
            df[col] = (df[col] - min_val) / range_val
            
    return df

# if __name__ == "__main__":
# 문제