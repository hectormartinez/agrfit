from pathlib import Path

datasets = ['comb_round2.feats', 'comb_round3.feats', 'comb_round4.feats', 'comb_round_all.feats',
            'da_semcor.feats', 'en_framenet.feats',
            'en_masc_crowdsourced.feats', 'en_ritter_sst.feats', 'eu_semcor.feats']

dataset_dir = (Path(__file__).parent / '../data/feats').resolve()
namespaces = {'a', 'b', 'c', 'd', 'z'}

for dataset_name in datasets:
    dataset_path = dataset_dir / dataset_name
    print("python source/regress.py {} --logit".format(dataset_path))

    for ns in namespaces:
        print("python source/regress.py {} --logit --ignore {}".format(dataset_path, ns))
        print("python source/regress.py {} --logit --keep {}".format(dataset_path, ns))