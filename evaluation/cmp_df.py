from  netshare.pre_post_processors.netshare import util

import pandas as pd
from pprint import pprint
import os 

dataset = "dc"

dataset = os.path.join("data", dataset)

raw_df = pd.read_csv(os.path.join(
        dataset, "raw.csv") )
syn_8000_df = pd.read_csv(os.path.join(
        dataset, "syn.csv") )
# syn_40_df = pd.read_csv(os.path.join(
#         dataset, "syn_40.csv") )


result = util.compute_metrics_pcap_v3(raw_df, syn_8000_df)
print("Dataset: {}\n".format(dataset))
pprint(result)
# result = util.compute_metrics_pcap_v3(raw_df, syn_40_df)
# pprint(result)
result = util.compute_metrics_pcap_v3(raw_df, raw_df)
pprint(result)