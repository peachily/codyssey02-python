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

def main():
    try:
        columns = load_attributes(ATTR_FILE)
        df = load_data(DATA_FILE, columns)
        print(df.shape)

        df['label'] = df['Sex']
        df = df.drop(columns=['Sex'])
        print(df['label'].value_counts().to_dict())

        data_to_scale = df.drop(columns=['label'])
        scaled_data = minmax_manual_scale(data_to_scale)
        print(scaled_data.describe().loc[['min', 'max']].round(6).to_dict())

    except (FileNotFoundError, UnicodeError) as e:
        print(e.args[0])
        return
    except (ValueError, Exception):
        print(f"Processing error.")
        return

if __name__ == "__main__":
    main()