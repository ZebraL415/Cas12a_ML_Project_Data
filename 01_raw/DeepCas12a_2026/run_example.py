import argparse
from pathlib import Path

import pandas as pd
import torch

from DeepCas12a import Episgt, VisionTransformer


def parse_args():
    parser = argparse.ArgumentParser(description="Run DeepCas12a inference on example sequences.")
    parser.add_argument("--input", default="example/example_sequences.txt", help="Whitespace-delimited input file.")
    parser.add_argument("--model", default="trained_model/fold1.pth", help="Path to a trained fold checkpoint.")
    parser.add_argument("--output", default="example/predictions.csv", help="CSV file for prediction results.")
    parser.add_argument("--num-epi-features", type=int, default=2, help="Number of epigenetic feature columns.")
    parser.add_argument("--no-label", action="store_true", help="Use this flag when the input file has no label column.")
    return parser.parse_args()


def read_selected_columns(input_path, num_epi_features, with_label):
    raw_df = pd.read_csv(input_path, sep=r"\s+", header=None)
    num_cols = num_epi_features + 2 if with_label else num_epi_features + 1
    return raw_df.iloc[:, -num_cols:].copy()


def main():
    args = parse_args()
    with_label = not args.no_label
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    data = Episgt(args.input, num_epi_features=args.num_epi_features, with_y=with_label)
    dataset = data.get_dataset()
    if with_label:
        x, y = dataset
    else:
        x, y = dataset, None

    x = torch.tensor(x, dtype=torch.float32).unsqueeze(1).to(device)

    model = VisionTransformer().to(device)
    model.load_state_dict(torch.load(args.model, map_location=device))
    model.eval()

    with torch.no_grad():
        predictions = model(x).cpu().numpy()

    selected_df = read_selected_columns(args.input, args.num_epi_features, with_label)
    result_df = pd.DataFrame(
        {
            "sequence": selected_df.iloc[:, 0],
            "prediction": predictions,
        }
    )
    if with_label:
        result_df["label"] = y

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result_df.to_csv(output_path, index=False)

    print(result_df.to_string(index=False))
    print(f"\nSaved predictions to {output_path}")


if __name__ == "__main__":
    main()
