# Import Packages
import pandas as pd
import numpy as np
import yaml
import os

## Load parameters from params.yaml

params = yaml.safe_load(open("params.yaml"))["preprocess"]

## Prepcrocess function
def load_export(input_path, output_path):
    data = pd.read_csv(input_path)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    data.to_csv(output_path, index=False)
    print(f"Data loaded and exported to {output_path} successfully")


if __name__ == "__main__":
    load_export(params["input"], params["output"])

