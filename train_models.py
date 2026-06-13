import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

FEATURE_COLUMNS = [
    "Gender",
    "Age",
    "Weight (kg)",
    "Height (m)",
    "Water_Intake (liters)",
    "Experience_Level",
    "Workout_Frequency (days/week)",
    "Resting_BPM",
]
CLASS_TARGET = "Fitness_Goal"
REG_TARGET = "Calories"
DEFAULT_DATA_FILE = "Final_data_with_goal.csv"
MODEL_GOAL = "fitness_goal_model.pkl"
MODEL_CAL = "calories_model.pkl"


def create_synthetic_data(n_samples: int = 20000, random_state: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)

    gender = rng.integers(0, 2, size=n_samples)
    age = rng.integers(18, 70, size=n_samples)
    height = np.clip(rng.normal(1.72, 0.09, size=n_samples), 1.45, 2.05)
    bmi = np.clip(rng.normal(24.0, 4.5, size=n_samples), 15.0, 38.0)
    weight = np.round(bmi * height ** 2, 1)
    water = np.clip(rng.normal(2.4, 0.7, size=n_samples), 0.8, 4.5)
    experience = rng.integers(1, 4, size=n_samples)
    workout = np.clip(
        (experience * 2 + rng.integers(-1, 2, size=n_samples)).astype(int), 0, 7
    )
    resting_bpm = np.clip(
        np.round(rng.normal(75 - experience * 2 + gender * 2, 8, size=n_samples)),
        45,
        105,
    ).astype(int)

    fitness_goal = np.where(bmi < 18.5, 1, np.where(bmi >= 25.0, 2, 0))

    height_cm = height * 100
    bmr = np.where(
        gender == 1,
        10 * weight + 6.25 * height_cm - 5 * age + 5,
        10 * weight + 6.25 * height_cm - 5 * age - 161,
    )
    activity_factor = np.where(
        workout <= 1,
        1.2,
        np.where(workout <= 3, 1.375, np.where(workout <= 5, 1.55, 1.725)),
    )
    calories = bmr * activity_factor + np.where(fitness_goal == 1, 350, np.where(fitness_goal == 2, -350, 0))
    calories = np.clip(calories + rng.normal(0, 120, size=n_samples), 1200, 3600)
    calories = np.round(calories).astype(int)

    return pd.DataFrame(
        {
            "Gender": gender,
            "Age": age,
            "Weight (kg)": weight,
            "Height (m)": np.round(height, 2),
            "Water_Intake (liters)": np.round(water, 2),
            "Experience_Level": experience,
            "Workout_Frequency (days/week)": workout,
            "Resting_BPM": resting_bpm,
            "Fitness_Goal": fitness_goal,
            "Calories": calories,
        }
    )


def validate_dataset_columns(df: pd.DataFrame) -> None:
    missing = [col for col in FEATURE_COLUMNS + [CLASS_TARGET, REG_TARGET] if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in dataset: {missing}")


def enforce_numeric_types(df: pd.DataFrame) -> pd.DataFrame:
    for column in FEATURE_COLUMNS + [CLASS_TARGET, REG_TARGET]:
        if column in df.columns and not pd.api.types.is_numeric_dtype(df[column]):
            df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def load_training_data(filename: str, allow_synthetic: bool = True, verbose: bool = False) -> pd.DataFrame:
    path = Path(filename)
    if path.exists():
        if verbose:
            print(f"Loading training data from {path.resolve()}")
        df = pd.read_csv(path)
        validate_dataset_columns(df)
        df = enforce_numeric_types(df)
        return df

    if not allow_synthetic:
        raise FileNotFoundError(f"Dataset {filename!r} not found and synthetic data is disabled.")

    print(f"Dataset {filename!r} not found. Generating synthetic training data instead.")
    return create_synthetic_data()


def train_classification_model(data: pd.DataFrame, test_size: float = 0.30, random_state: int = 37) -> LogisticRegression:
    x = data[FEATURE_COLUMNS]
    y = data[CLASS_TARGET]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=test_size, random_state=random_state
    )
    model = LogisticRegression(max_iter=5000, solver="lbfgs")
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    print("Classification accuracy:", accuracy_score(y_test, y_pred))
    return model


def train_regression_model(data: pd.DataFrame, test_size: float = 0.30, random_state: int = 37) -> RandomForestRegressor:
    x2 = data[FEATURE_COLUMNS]
    y2 = data[REG_TARGET]
    x_train2, x_test2, y_train2, y_test2 = train_test_split(
        x2, y2, test_size=test_size, random_state=random_state
    )
    model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=random_state)
    model.fit(x_train2, y_train2)
    y_pred7 = model.predict(x_test2)
    print("Regression MAE:", mean_absolute_error(y_test2, y_pred7))
    print("Regression MSE:", mean_squared_error(y_test2, y_pred7))
    print("Regression R2:", r2_score(y_test2, y_pred7))
    return model


def save_models(classifier: LogisticRegression, regressor: RandomForestRegressor, base_path: str = ".") -> None:
    base = Path(base_path)
    base.mkdir(parents=True, exist_ok=True)
    joblib.dump(classifier, base / MODEL_GOAL)
    joblib.dump(regressor, base / MODEL_CAL)
    print(f"Saved models to {base / MODEL_GOAL} and {base / MODEL_CAL}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train and save nutrition recommendation models.")
    parser.add_argument(
        "--data-file",
        default=DEFAULT_DATA_FILE,
        help="Path to the dataset CSV file containing training data.",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory where trained models will be saved.",
    )
    parser.add_argument(
        "--save-generated-data",
        action="store_true",
        help="Save generated synthetic data to disk when the real dataset is missing.",
    )
    parser.add_argument(
        "--no-synthetic",
        action="store_true",
        help="Fail if the real dataset is missing instead of generating synthetic data.",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random seed for synthetic data generation and train/test splits.",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.30,
        help="Test split size for model evaluation.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print additional debug information.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = load_training_data(args.data_file, allow_synthetic=not args.no_synthetic, verbose=args.verbose)

    if args.save_generated_data and not Path(args.data_file).exists():
        generated_path = Path(args.output_dir) / "generated_training_data.csv"
        data.to_csv(generated_path, index=False)
        print(f"Saved generated synthetic dataset to {generated_path}")

    classifier = train_classification_model(data, test_size=args.test_size, random_state=args.random_state)
    regressor = train_regression_model(data, test_size=args.test_size, random_state=args.random_state)
    save_models(classifier, regressor, base_path=args.output_dir)


if __name__ == "__main__":
    main()
