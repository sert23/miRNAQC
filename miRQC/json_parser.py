import json
from collections import OrderedDict

input_file = "/Users/ernesto/PycharmProjects/miRQC/miRQC/variables.json"
output_file = "/Users/ernesto/PycharmProjects/miRQC/miRQC/variables.md"

with open(input_file,"r") as ij:
    with open(output_file,"w") as out_f:
        out_f.write("#Quality features\n")
        features = json.load(ij, object_pairs_hook=OrderedDict)

        for k in features.keys():
            #title
            c_dict = features[k]
            out_f.write("**<u>{}</u>** ({}): {}".format(c_dict.get("full_name"), c_dict.get("short_name"),
                                                        c_dict.get("description")))
            out_f.write("\n")
            out_f.write("\n")

            print(k)




