def extract_list_of_dicts(D_features, expand_bag, ignore, keep):
    ignore_set = set(ignore)
    keep_set = set(keep)
    numeric_and_cat_cols = [name for name in D_features.columns
                            if name.endswith("_n") or name.endswith("_s")
                            if not name.startswith("i_")
                            if not name.startswith("y_")
                            if name != 'b_stemcoverage_n'
                            if not name[0] in ignore_set
                            if (keep_set and name[0] in keep_set) or not keep_set
                            ]

    bag_cols = [name for name in D_features.columns
                if name.endswith("_b")
                if not name.startswith("i_")
                if not name[0] in ignore_set
                if (keep_set and name[0] in keep_set) or not keep_set
                ]

    dict_list = []
    for idx, row in D_features.iterrows():
        org_dict = {k: v for k, v in row.to_dict().items()}
        row_dict = {k: v for k, v in org_dict.items() if k in numeric_and_cat_cols}

        if expand_bag:
            for bag_col in bag_cols:
                if bag_col in org_dict:
                    bag_contents = str(org_dict[bag_col]).split(" ")
                    row_dict.update({bag_col + '_' + name: 1 for name in bag_contents})

        dict_list.append(row_dict)

    return dict_list
