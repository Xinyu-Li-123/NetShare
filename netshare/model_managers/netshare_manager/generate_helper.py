import copy
import subprocess
import sys
import time
import os
import json
import importlib
import random
import pandas as pd
import socket
import struct
import ipaddress
import argparse

import numpy as np
import pandas as pd

import netshare.ray as ray
from pathlib import Path
from tqdm import tqdm
from scapy.all import IP, ICMP, TCP, UDP
from scapy.all import wrpcap
from scipy.stats import rankdata
from pathlib import Path


@ray.remote(scheduling_strategy="SPREAD", max_calls=1)
def _generate_attr(
        create_new_model,
        configs,
        config_idx,
        log_folder):
    config = configs[config_idx]
    config["given_data_attribute_flag"] = False
    model = create_new_model(config)
    model.generate(
        input_train_data_folder=config["dataset"],
        input_model_folder=config["result_folder"],
        output_syn_data_folder=config["eval_root_folder"],
        log_folder=log_folder)


@ray.remote(scheduling_strategy="SPREAD", max_calls=1)
def _merge_attr(attr_raw_npz_folder, word2vec_size,
                pcap_interarrival, num_chunks):
    if not pcap_interarrival:
        bit_idx_flagstart = 128 + word2vec_size * 3
    else:
        bit_idx_flagstart = 128 + word2vec_size * 3 + 1

    print("PCAP_INTERARRIVAL:", pcap_interarrival)
    print("bit_idx_flagstart:", bit_idx_flagstart)

    attr_clean_npz_folder = os.path.join(
        str(Path(attr_raw_npz_folder).parents[0]), "attr_clean"
    )
    os.makedirs(attr_clean_npz_folder, exist_ok=True)

    dict_chunkid_attr = {}
    for chunkid in tqdm(range(num_chunks)):
        dict_chunkid_attr[chunkid] = []

    for chunkid in tqdm(range(num_chunks)):
        n_flows_startFromThisEpoch = 0

        if not os.path.exists(
            os.path.join(
                attr_raw_npz_folder,
                "chunk_id-{}.npz".format(chunkid))
        ):
            print(
                "{} not exists...".format(
                    os.path.join(
                        attr_raw_npz_folder,
                        "chunk_id-{}.npz".format(chunkid))
                )
            )
            continue

        raw_attr_chunk = np.load(
            os.path.join(
                attr_raw_npz_folder,
                "chunk_id-{}.npz".format(chunkid))
        )["data_attribute"]

        if num_chunks > 1:
            for row in raw_attr_chunk:
                # if row[bit_idx_flagstart] < row[bit_idx_flagstart+1]:
                if (
                    row[bit_idx_flagstart] < row[bit_idx_flagstart + 1]
                    and row[bit_idx_flagstart + 2 * chunkid + 2]
                    < row[bit_idx_flagstart + 2 * chunkid + 3]
                ):
                    # this chunk
                    row_this_chunk = list(
                        copy.deepcopy(row)[
                            :bit_idx_flagstart])
                    row_this_chunk += [0.0, 1.0]
                    row_this_chunk += [1.0, 0.0] * (chunkid + 1)
                    for i in range(chunkid + 1, num_chunks):
                        if (
                            row[bit_idx_flagstart + 2 * i + 2]
                            < row[bit_idx_flagstart + 2 * i + 3]
                        ):
                            row_this_chunk += [0.0, 1.0]
                        else:
                            row_this_chunk += [1.0, 0.0]
                    # dict_chunkid_attr[chunkid].append(row_this_chunk)
                    dict_chunkid_attr[chunkid].append(row)

                    # following chunks
                    # row_following_chunk = list(copy.deepcopy(row)[:bit_idx_flagstart])
                    # row_following_chunk += [1.0, 0.0]*(1+NUM_CHUNKS)
                    n_flows_startFromThisEpoch += 1
                    row_following_chunk = list(copy.deepcopy(row))
                    row_following_chunk[bit_idx_flagstart] = 1.0
                    row_following_chunk[bit_idx_flagstart + 1] = 0.0

                    for i in range(chunkid + 1, num_chunks):
                        if (
                            row[bit_idx_flagstart + 2 * i + 2]
                            < row[bit_idx_flagstart + 2 * i + 3]
                        ):
                            dict_chunkid_attr[i].append(row_following_chunk)
                            # dict_chunkid_attr[i].append(row)
        else:
            dict_chunkid_attr[chunkid] = raw_attr_chunk

        print(
            "n_flows_startFromThisEpoch / total flows: {}/{}".format(
                n_flows_startFromThisEpoch, raw_attr_chunk.shape[0]
            )
        )

    print("Saving merged attrs...")
    n_merged_attrs = 0
    for chunkid, attr_clean in dict_chunkid_attr.items():
        print("chunk {}: {} flows".format(chunkid, len(attr_clean)))
        n_merged_attrs += len(attr_clean)
        np.savez(
            os.path.join(
                attr_clean_npz_folder,
                "chunk_id-{}.npz".format(chunkid)),
            data_attribute=np.asarray(attr_clean),
        )

    print("n_merged_attrs:", n_merged_attrs)


@ray.remote(scheduling_strategy="SPREAD", max_calls=1)
# @ray.remote(scheduling_strategy="DEFAULT", max_calls=1)
def _generate_given_attr(create_new_model, configs, config_idx,
                         log_folder):

    config = configs[config_idx]
    config["given_data_attribute_flag"] = True
    model = create_new_model(config)
    model.generate(
        input_train_data_folder=config["dataset"],
        input_model_folder=config["result_folder"],
        output_syn_data_folder=config["eval_root_folder"],
        log_folder=log_folder)

# ===================== TODO: move merge_syn_df to postprocess ================


def get_per_chunk_df(chunk_folder):
    '''chunk_folder: "chunk_id-0"'''
    df_names = [file for file in os.listdir(
        chunk_folder) if file.endswith(".csv")]
    assert (len(df_names) > 0)
    df = pd.read_csv(os.path.join(chunk_folder, df_names[0]))

    return df
