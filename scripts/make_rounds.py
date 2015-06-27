import pandas as pd
from pathlib import Path

def make_combined_dataset(file_names, output_file):
    data_frames = [pd.read_csv(str(file_name), sep="\t") for file_name in file_names]
    D = pd.concat(data_frames)
    D.to_csv(str(output_file), sep="\t")

feat_dir = Path("data/feats")
make_combined_dataset(feat_dir.glob("round2*"), feat_dir / 'comb_round2.feats')
make_combined_dataset(feat_dir.glob("round3*"), feat_dir / 'comb_round3.feats')
make_combined_dataset(feat_dir.glob("round4*"), feat_dir / 'comb_round4.feats')
make_combined_dataset(feat_dir.glob("round*"), feat_dir / 'comb_round_all.feats')