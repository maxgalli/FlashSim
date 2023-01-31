# the loop for generating new events starting from gen-level information in the files

import ROOT
import uproot
import numpy as np
import pandas as pd
from tqdm import tqdm
import torch
from torch.utils.data import Dataset, DataLoader
import nflows
import time
import os
import awkward as ak
import mynflow
import nbd_func
import pathlib

if __name__ == "__main__":

    # specify old/new root
    root = "data/apply"
    new_root = "data/apply/new"
    files_paths = [
        f for f in os.listdir(root) if f.endswith(".root")
    ]  # = [x for x in pathlib.Path(root).glob('**/*')]

    # take remaining files if loop crashes
    print(f"We will process a total of {len(files_paths)} files")

    # specify device and load models
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    jet_flow, _, _, _, trh, tsh = mynflow.load_model(
        "saves", 
        "model_jets_final_@epoch_0.pt"
    )
    muon_flow, _, _, _, trh, tsh = mynflow.load_model(
        "saves", 
        "model_muons_final_@epoch_10.pt"
    )

    # generation loop
    for path in tqdm(files_paths):
        path_str = str(path)  # shouldn't be needed
        nbd_func.nbd(jet_flow, muon_flow, root, path_str, new_root)
