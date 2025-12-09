import pandas as pd

def load_attributes(path='a.txt'):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        print("File open error: a.txt")
        return None
    except UnicodeDecodeError:
        print("Decoding error in a.txt")
        return None
    except Exception:
        print("Unknown error in a.txt")
        return None


def load_data(cols, path='b.txt'):
    try:
        df = pd.read_csv(path, header=None)
        df.columns = cols
        return df
    except FileNotFoundError:
        print("File open error: b.txt")
        return None
    except UnicodeDecodeError:
        print("Decoding error in b.txt")
        return None
    except Exception:
        print("Unknown error in b.txt")
        return None


def make_label(df):
    df["label"] = df["sex"]
    df = df.drop(columns=["sex"])
    return df


def minmax_manual(df):
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    scaled = df.copy()
    for col in numeric_cols:
        minimum = df[col].min()
        maximum = df[col].max()
        if maximum - minimum == 0:
            scaled[col] = 0.0
        else:
            scaled[col] = (df[col] - minimum) / (maximum - minimum)
    return scaled


def main():
    attrs = load_attributes()
    if attrs is None:
        return

    df = load_data(attrs)
    if df is None:
        return

    df = make_label(df)
    print(df.shape)
    print(df['label'].value_counts().to_dict())

    scaled = minmax_manual(df)
    print(scaled.describe().loc[['min', 'max']].round(6).to_dict())


if __name__ == "__main__":
    main()
