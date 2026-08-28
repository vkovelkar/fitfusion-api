import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

RAW_DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "workout_data.csv"
)

PROCESSED_DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "workout_data.csv"
)


def preprocess_data():
    """
    Load raw workout data, clean it, encode categorical
    features, and save the processed dataset.
    """

    print("Loading raw data...")

    df = pd.read_csv(RAW_DATA_PATH)

    print(f"Raw data shape: {df.shape}")

    # Remove duplicate records
    df = df.drop_duplicates()

    # Remove rows with missing values
    df = df.dropna()

    # Encode workout type
    encoder = LabelEncoder()

    df["workout_type"] = encoder.fit_transform(
        df["workout_type"]
    )

    # Create processed directory if needed
    os.makedirs(
        os.path.dirname(PROCESSED_DATA_PATH),
        exist_ok=True
    )

    # Save processed data
    df.to_csv(
        PROCESSED_DATA_PATH,
        index=False
    )

    print("Data preprocessing completed.")
    print(
        f"Processed data saved to: "
        f"{PROCESSED_DATA_PATH}"
    )

    return df


if __name__ == "__main__":
    preprocess_data()