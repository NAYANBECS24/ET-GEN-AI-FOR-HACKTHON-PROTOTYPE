from app.utils.synthetic_data import generate_dataset


if __name__ == "__main__":
    path = generate_dataset(200, "intent_training.jsonl")
    print(f"Generated synthetic dataset at {path}")
