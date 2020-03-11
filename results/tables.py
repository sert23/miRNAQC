from collections import OrderedDict
import results.mqc_table as table
from multiqc import config
import pandas
import os
from miRQC.settings import MEDIA_ROOT, MEDIA_URL, SUB_SITE, MEDIA_URL
import math

import math

#quartiles colors
# colors:{'Q1':'rgb(164, 207, 99)','Q2':'rgb(232, 213, 89)','Q3':'rgb(251, 163,83)','Q4':'rgb(221,90,78)'},

# values_tab = "/Users/ernesto/Desktop/colabo/quality/mock_values.tsv"
values_tab = os.path.join(MEDIA_ROOT,"test","mock_values.tsv")
# perc_tab = "/Users/ernesto/Desktop/colabo/quality/mock_perc.tsv"
perc_tab = os.path.join(MEDIA_ROOT,"test","mock_perc.tsv")


# d2 = {k: f(v) for k, v in d1.items()}


def get_quart_cols(input_val, sense = "desc" ):
    if sense == "desc":
        if input_val > 75:
            col = 'rgb(164, 207, 99)'
        elif input_val > 50:
            col = 'rgb(232, 213, 89)'
        elif input_val > 25:
            col = 'rgb(251, 163,83)'
        else:
            col = 'rgb(221,90,78)'
        return col
    elif sense == "asc":
        if input_val > 75:
            col = 'rgb(221,90,78)'
        elif input_val > 50:
            col = 'rgb(251, 163,83)'
        elif input_val > 25:
            col = 'rgb(232, 213, 89)'
        else:
            col = 'rgb(164, 207, 99)'
        return col
    elif sense == "neut":
        return 'rgb(192,192,192)'

def make_ordinal(n):
    '''
    Convert an integer into its ordinal representation::

        make_ordinal(0)   => '0th'
        make_ordinal(3)   => '3rd'
        make_ordinal(122) => '122nd'
        make_ordinal(213) => '213th'
    '''

    x = float(n)
    if math.isnan(x):
        return " _"

    n = int(n)

    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return suffix



def get_ordinals(input_dict):

    return {k: make_ordinal(v) for k, v in input_dict.items()}

def gen_col_dict(input_dict, sense):

    if input_dict:
        return {k: get_quart_cols(v,sense) for k, v in input_dict.items()}
    else:
        return None



def df2dict(df):
    table = df
    new_dict = {}
    # print(table.columns)
    samples = table['sample'].values

    for sample in samples:
        subset = table.loc[table['sample'] == sample]
        subset = subset.drop(["sample"],1)
        new_dict[sample] = subset.to_dict("records")[0]

    return new_dict


def table2dict(filepath):

    table = pandas.read_csv(filepath, sep="\t")
    new_dict = {}
    samples = table['sample'].values

    for sample in samples:
        subset = table.loc[table['sample'] == sample]
        subset = subset.drop(["sample"],1)
        new_dict[sample] = subset.to_dict("records")[0]

    return new_dict

#
# def cols_dict(input_file):
#     table = pandas.read_csv(input_file, sep="\t", index_col=0)
#     new_dict = {}
#     columns = table.columns
#     for column in columns:
#         subset = table[column]
#         new_dict[column] = subset.to_dict()
#         # print(column)
#     return new_dict

def cols_dict(df):
    table = df.copy()
    table.set_index("sample", inplace=True)
    new_dict = {}
    columns = table.columns
    # print(columns)
    for column in columns:
        subset = table[column]
        new_dict[column] = subset.to_dict()
        # print(column)
    return new_dict

# def pars_dict(df):
#     table = df.copy()
#     table.set_index("Input File", inplace=True)
#     new_dict = {}
#     columns = table.columns
#     print(columns)
#     for column in columns:
#         subset = table[column]
#         new_dict[column] = subset.to_dict()
#         # print(column)
#     return new_dict

def pars2dict(df):
    table = df
    new_dict = {}
    # print(table.columns)
    samples = table["Input File"].values

    for sample in samples:
        subset = table.loc[table["Input File"] == sample]
        subset = subset.drop(["Input File"],1)
        new_dict[sample] = subset.to_dict("records")[0]

    return new_dict


config_p = {
    'namespace': 'My Module',
    'min': 0,
    'scale': 'GnBu'
    #     make switch button
    # 'data_labels': [
    #     {'name': 'DS 1', 'ylab': 'Dataset 1', 'xlab': 'x Axis 1'},
    #     {'name': 'DS 2', 'ylab': 'Dataset 2', 'xlab': 'x Axis 2'}
    # ]
}

def par_table(input_file):

    input_df = pandas.read_csv(input_file, sep="\t")
    vals_dict = pars2dict(input_df)
    headers = OrderedDict()
    to_keep = ["Input File", "taxon ID","Species","short species name","protocol","adapter","5' Random Adapter Bases",
               " 3' Random Adapter Bases"]
    keep = set(to_keep).intersection(list(input_df.columns))
    if True:
        if "Input File" in keep:
            headers["Input File"] = {
                'title': "Input File",
                # 'description': 'Total number of reads sequenced',
                # 'is_int': True
            }
        if "taxon ID" in keep:
            headers["taxon ID"] = {
                'title': "taxon ID",
                # 'description': 'Total number of reads sequenced',
                'is_int': True
            }
        if "Species" in keep:
            headers["Species"] = {
                'title': "Species",
                # 'description': 'Total number of reads sequenced',
                # 'is_int': True
            }
        if "short species name" in keep:
            headers["short species name"] = {
                'title': "short <br>species name",
                # 'description': 'Total number of reads sequenced',
                # 'is_int': True
            }

        if "protocol" in keep:
            headers["protocol"] = {
                'title': "protocol",
                # 'description': 'Total number of reads sequenced',
                # 'is_int': True
            }
        if "adapter" in keep:
            headers["adapter"] = {
                'title': "adapter",
                # 'description': 'Total number of reads sequenced',
                # 'is_int': True
            }
        if "5' Random Adapter Bases" in keep:
            headers["5' Random Adapter Bases"] = {
                'title': "5' Random <br> Adapter Bases",
                # 'description': 'Total number of reads sequenced',
                'is_int': True
            }
        if " 3' Random Adapter Bases" in keep:
            headers[" 3' Random Adapter Bases"] = {
                'title': "3' Random <br> Adapter Bases",
                # 'description': 'Total number of reads sequenced',
                'is_int': True
            }
    # val_tab = table.plot(vals_dict)
    val_tab = table.plot(vals_dict, headers)
    return val_tab

def basic_table(val_df,perc_df, columns):

    vals_dict = df2dict(val_df)
    columns_dict = columns

    perc_dict = df2dict(perc_df)
    headers = OrderedDict()


    #
    # miRNA SD

    # readsRaw     # readsPerc     # adapterDimerPerc     # detectedMatureSA     # maturePercofReads
    #  meanofp50     # mainPeakMiRNAlength     # stdDevMiRNAlength
    to_keep = ["readsRaw", "readsPerc", "adapterDimerPerc", "shortReadsPerc", "detectedMatureSA", "maturePercofReads",
               "mainPeakMiRNAlength", "meanofp50"]
    keep = set(to_keep).intersection(list(val_df.columns))
    if True:
        if "readsRaw" in keep:
            headers["readsRaw"] = {
                'title': 'Raw reads',
                'description': 'Total number of reads sequenced',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict["readsRaw"], "desc"),
                'bar_dict': columns_dict["readsRaw"],
                'is_int': True
                # 'max': 100,
                # 'min': 0,

            }
        if "readsPerc" in keep:
            headers["readsPerc"] = {
                'title': '% Reads',
                'description': 'Percentage of reads used for the analysis after filtering',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict["readsPerc"], "desc"),
                'bar_dict': columns_dict["readsPerc"],
                'suffix': '%',

                # 'max': 100,

                # 'min': 0,

            }
        if "adapterDimerPerc" in keep:
            headers["adapterDimerPerc"] = {
            'title': '% Dimers',
            'description': 'The percentage of reads that correspond to adapter-dimer, i.e. those that are shorter or equal to 2nt after adapter trimming ',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict["adapterDimerPerc"], "asc"),
            'bar_dict': columns_dict["adapterDimerPerc"],
            'suffix': '%',
        }

        if "shortReadsPerc" in keep:

            headers["shortReadsPerc"] = {
                'title': '% short reads',
                'description': 'Reads between 15 and 17 nt. This range was choosen because tRNA fragments are frequently of 18 nt length.',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict["shortReadsPerc"], "asc"),
                'bar_dict': columns_dict["shortReadsPerc"],
                'suffix': '%',
            }

        if "detectedMatureSA" in keep:
            headers["detectedMatureSA"] = {
                'title': 'miRNAs',
                'description': 'Total number of mature miRNAs detected',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict["detectedMatureSA"], "desc"),
                'bar_dict': columns_dict["detectedMatureSA"],
                'is_int': True
                # 'max': 100,
                # 'min': 0,

            }
        if "maturePercofReads" in keep:
            headers["maturePercofReads"] = {
                'title': '% microRNA reads',
                'description': 'Percentage of effective reads assigned to mature microRNAs',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict["maturePercofReads"], "desc"),
                'bar_dict': columns_dict["maturePercofReads"],
                'suffix': '%',
                # 'max': 100,
                # 'min': 0,
            }
        if "mainPeakMiRNAlength" in keep:
            headers["mainPeakMiRNAlength"] = {
                'title': 'miRNA "peak"',
                # 'title': 'miRNA lengths',
                'description': 'Percentage of miRNA reads of lengths 21, 22 and 23',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict["mainPeakMiRNAlength"], "desc"),
                'bar_dict': columns_dict["mainPeakMiRNAlength"],
                'suffix': '%',
                # 'max': 100,
                # 'min': 0,
            }
        if "meanofp50" in keep:
            headers["meanofp50"] = {
                'title': 'Phred score',
                'description': 'Average Phred Score of the per position score median',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict["meanofp50"], "desc"),
                'bar_dict': columns_dict["meanofp50"],
                # 'suffix': '%',
                # 'max': 100,
                # 'min': 0,
            }



    # print("eo")
    # print(keep)
    # clean_headers = {k: headers[k] for k in headers.keys() if k in keep}
    # print(list(clean_headers.keys()))
    val_tab = table.plot(vals_dict, headers)

    for k in list(headers.keys()):
        c_dict = headers.get(k)
        description = c_dict["description"]
        c_dict["description"] = description + " (percentile)"
        c_dict['suffix'] = "show_perc"
        c_dict['is_int'] = False
        c_dict["suffix_dict"] = get_ordinals(columns_dict[k])


    perc_tab = table.plot(perc_dict, headers)

    return val_tab,perc_tab


def tables_yield(val_df, perc_df, columns):
    vals_dict = df2dict(val_df)
    columns_dict = columns

    perc_dict = df2dict(perc_df)
    headers = OrderedDict()
    # readsRaw     # reads     # readsAdapterFound     # readsAdapterFoundPerc
    # readsUnique     # avgRCperUnique     # detectedMatureSA


    # avgRCperUnique
    # detectedMatureSA
    # maturePercofReads

    to_keep = ["readsRaw", "reads", "readsAdapterFound", "readsAdapterFoundPerc", "readsUnique", "avgRCperUnique",
               "detectedMatureSA", "maturePercofReads"]
    keep = set(to_keep).intersection(list(val_df.columns))

    if True:
        if "readsRaw" in keep:
            headers["readsRaw"] = {
            'title': 'Raw reads',
            'description': 'Total number of reads sequenced',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict.get("readsRaw"), "desc"),
            'bar_dict': columns_dict.get("readsRaw"),
            'is_int': True
            # 'max': 100,
            # 'min': 0,

        }
        if "reads" in keep:
            headers["reads"] = {
            'title': 'Num. of reads',
            'description': 'Number of reads used for the analysis after filtering',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict.get("reads"), "desc"),
            'bar_dict': columns_dict.get("reads"),
            'is_int': True

        }
        if "readsUnique" in keep:
            headers["readsUnique"] = {
            'title': 'Unique reads',
            # 'title': 'microRNA mapping reads length SD',
            'description': 'Number of unique sequences after collapsing',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict.get("readsUnique"), "neut"),
            'bar_dict': columns_dict.get("readsUnique"),
            'is_int': True


        }
        if "detectedMatureSA" in keep:
            headers["detectedMatureSA"] = {
            'title': 'Detected microRNAs',
            'description': 'Total number of mature miRNAs detected',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict.get("detectedMatureSA"), "desc"),
            'bar_dict': columns_dict.get("detectedMatureSA"),
            'is_int': True
        }
        if "maturePercofReads" in keep:
            headers["maturePercofReads"] = {
            'title': '% microRNA reads',
            'description': 'Percentage of reads assigned to mature microRNAs',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict.get("maturePercofReads"), "desc"),
            'bar_dict': columns_dict.get("maturePercofReads"),
            'suffix': '%',
            # 'max': 100,
            # 'min': 0,
        }
        if "readsAdapterFound" in keep:
            headers["readsAdapterFound"] = {
            'title': 'Trimmed reads',
            'description': 'Number of reads for which the adapter was found and trimmed',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict.get("readsAdapterFound"), "desc"),
            'bar_dict': columns_dict.get("readsAdapterFound"),
            'is_int': True
            # 'suffix': '%',
            # 'max': 100,
            # 'min': 0,
        }
        if "readsAdapterFoundPerc" in keep:
            headers["readsAdapterFoundPerc"] = {
            'title': '% Adapter trimmed reads',
            'description': 'Percentage of reads for which the adapter was found and trimmed',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict.get("readsAdapterFoundPerc"), "desc"),
            'bar_dict': columns_dict.get("readsAdapterFoundPerc"),
            'suffix': '%',

        }

        # headers["avgRCperUnique"] = {
        #     'title': 'Reads per unique',
        #     'description': 'Number of reads in analysis divided by number of unique reads',
        #     'scale': "quart",
        #     'col_dict': gen_col_dict(columns_dict.get("avgRCperUnique"), "desc"),
        #     'bar_dict': columns_dict.get("avgRCperUnique"),
        # }


        # headers["maturePercofReads"] = {
        #     'title': '% microRNA reads',
        #     'description': 'Percentage of effective reads assigned to mature microRNAs',
        #     'scale': "quart",
        #     'col_dict': gen_col_dict(columns_dict.get("maturePercofReads"), "desc"),
        #     'bar_dict': columns_dict.get("maturePercofReads"),
        #     'suffix': '%',
        #
        # }


    # print("eo")
    # print(keep)
    #clean_headers = {k: headers[k] for k in headers.keys() if k in keep}
    # print(list(clean_headers.keys()))
    val_tab = table.plot(vals_dict, headers)

    for k in list(headers.keys()):
        c_dict = headers.get(k)
        description = c_dict["description"]
        c_dict["description"] = description + " (percentile)"
        if k in keep:
            c_dict['suffix'] = "show_perc"
            c_dict['is_int'] = False
            c_dict["suffix_dict"] = get_ordinals(columns_dict[k])


    #clean_headers = {k: headers[k] for k in headers.keys() if k in keep}

    perc_tab = table.plot(perc_dict, headers)

    return val_tab, perc_tab

def tables_complex(val_df, perc_df, columns):
    vals_dict = df2dict(val_df)
    columns_dict = columns

    perc_dict = df2dict(perc_df)
    headers = OrderedDict()

    to_keep = ["avgRCperUnique", "miRNAexprTop1", "miRNAexprTop5", "miRNAexprTop20", "miRNAexprp50", "miRNAexprp75", "miRNAexprp95", "miRNAper1k" ]
    keep = set(to_keep).intersection(list(val_df.columns))

    if True:
        if "avgRCperUnique" in keep:
            headers["avgRCperUnique"] = {
                'title': 'Reads per unique',
                'description': 'Number of reads in analysis divided by number of unique reads',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict.get("avgRCperUnique"), "desc"),
                'bar_dict': columns_dict.get("avgRCperUnique"),
            }
        if "miRNAexprTop1" in keep:
            headers["miRNAexprTop1"] = {
                'title': '% top miRNA',
                'description': 'Percentage of reads assigned to the most expressed miRNA',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict.get("miRNAexprTop1"), "desc"),
                'bar_dict': columns_dict.get("miRNAexprTop1"),
                'suffix': '%',
            }
        if "miRNAexprTop5" in keep:
            headers["miRNAexprTop5"] = {
                'title': '% top5 miRNA',
                'description': 'Percentage of reads assigned to the 5 most expressed miRNA',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict.get("miRNAexprTop5"), "desc"),
                'bar_dict': columns_dict.get("miRNAexprTop5"),
                'suffix': '%',
            }
        if "miRNAexprTop20" in keep:
            headers["miRNAexprTop20"] = {
                'title': '% top20 miRNA',
                'description': 'Percentage of reads assigned to the 20 most expressed miRNA',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict.get("miRNAexprTop20"), "desc"),
                'bar_dict': columns_dict.get("miRNAexprTop20"),
                'suffix': '%',
            }
        if "miRNAexprp50" in keep:
            headers["miRNAexprp50"] = {
                'title': '#miRNA p50',
                'description': 'Number of miRNAs needed to reach 50% miRNA reads',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict.get("miRNAexprp50"), "desc"),
                'bar_dict': columns_dict.get("miRNAexprp50"),
                "is_int": True
            }
        if "miRNAexprp75" in keep:
            headers["miRNAexprp75"] = {
                'title': '#miRNA p75',
                'description': 'Number of miRNAs needed to reach 75% miRNA reads',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict.get("miRNAexprp75"), "desc"),
                'bar_dict': columns_dict.get("miRNAexprp75"),
                "is_int": True
            }
        if "miRNAexprp95" in keep:
            headers["miRNAexprp95"] = {
                'title': '#miRNA p95',
                'description': 'Number of miRNAs needed to reach 95% miRNA reads',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict.get("miRNAexprp95"), "desc"),
                'bar_dict': columns_dict.get("miRNAexprp95"),
                "is_int": True
            }
        if "miRNAper1k" in keep:
            headers["miRNAper1k"] = {
                'title': 'miRNAs per 1000 reads',
                'description': 'Number of miRNAs detected per 1kb mapped to miRNAs',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict.get("miRNAper1k"), "desc"),
                'bar_dict': columns_dict.get("miRNAper1k"),
            }


    val_tab = table.plot(vals_dict, headers)

    for k in list(headers.keys()):
        c_dict = headers.get(k)
        description = c_dict["description"]
        c_dict["description"] = description + " (percentile)"
        if k in keep:
            c_dict['suffix'] = "show_perc"
            c_dict['is_int'] = False
            c_dict["suffix_dict"] = get_ordinals(columns_dict[k])

    perc_tab = table.plot(perc_dict, headers)


    return val_tab, perc_tab

def seq_qual_tab(val_df,perc_df, columns):
    vals_dict = df2dict(val_df)
    columns_dict = columns

    perc_dict = df2dict(perc_df)
    headers = OrderedDict()

    #headers
    #meanofmeans
    # meanofp10
    # meanofp25
    # meanofp50
    # meanofp75
    # meanofp90
    if True:
        headers["meanofmeans"] = {
            'title': 'Average mean <br>Phred Score',
            'description': 'The mean Phred Scores are obtained by FastQC per position, then the average of these values are calculated using positions 1 to 40',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict.get("meanofmeans"), "desc"),
            'bar_dict': columns_dict.get("meanofmeans"),
            # 'max': 100,
            # 'min': 0,
        }
        headers["meanofp10"] = {
            'title': 'Average percentile 10 <br>Phred Score ',
            'description': 'The mean Phred Scores are obtained by FastQC per position, then the average of these values are calculated using positions 1 to 40',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict.get("meanofp10"), "desc"),
            'bar_dict': columns_dict.get("meanofp10"),
            # 'max': 100,
            # 'min': 0,
        }
        headers["meanofp25"] = {
            'title': 'Average percentile 25 <br>Phred Score ',
            'description': 'The mean Phred Scores are obtained by FastQC per position, then the average of these values are calculated using positions 1 to 40',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict.get("meanofp25"), "desc"),
            'bar_dict': columns_dict.get("meanofp25"),
            # 'max': 100,
            # 'min': 0,
        }
        headers["meanofp50"] = {
            'title': 'Average median <br>Phred Score ',
            'description': 'The mean Phred Scores are obtained by FastQC per position, then the average of these values are calculated using positions 1 to 40',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict.get("meanofp50"), "desc"),
            'bar_dict': columns_dict.get("meanofp50"),
            # 'max': 100,
            # 'min': 0,
        }
        headers["meanofp75"] = {
            'title': 'Average percentile 75 <br>Phred Score ',
            'description': 'The mean Phred Scores are obtained by FastQC per position, then the average of these values are calculated using positions 1 to 40',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict.get("meanofp75"), "desc"),
            'bar_dict': columns_dict.get("meanofp75"),
            # 'max': 100,
            # 'min': 0,
        }
        headers["meanofp90"] = {
            'title': 'Average percentile 90 <br>Phred Score ',
            'description': 'The mean Phred Scores are obtained by FastQC per position, then the average of these values are calculated using positions 1 to 40',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict.get("meanofp90"), "desc"),
            'bar_dict': columns_dict.get("meanofp90"),
            # 'max': 100,
            # 'min': 0,
        }



    to_keep = ["meanofmeans", "meanofp10"," meanofp25","meanofp50","meanofp75","meanofp90"]
    keep = set(to_keep).intersection(list(val_df.columns))
    clean_headers = {k: headers[k] for k in headers.keys() if k in keep}
    val_tab = table.plot(vals_dict, clean_headers)

    for k in list(headers.keys()):
        c_dict = headers.get(k)
        description = c_dict["description"]
        c_dict["description"] = description + " (percentile)"
        if k in keep:
            c_dict['suffix'] = "show_perc"
            c_dict['is_int'] = False
            c_dict["suffix_dict"] = get_ordinals(columns_dict[k])


    clean_headers = {k: headers[k] for k in headers.keys() if k in keep}

    perc_tab = table.plot(perc_dict, clean_headers)


    return val_tab, perc_tab



def library_tab(val_df,perc_df, columns):
    vals_dict = df2dict(val_df)
    columns_dict = columns
    perc_dict = df2dict(perc_df)
    headers = OrderedDict()
    to_keep = ["adapterDimerPerc", "ultraShortReadsPerc", "shortReadsPerc", "rRNAPerc" ]
    keep = set(to_keep).intersection(list(val_df.columns))
    # adapterDimerPerc
    # ultraShortReadsPerc
    # shortReadsPerc
    # rRNAPerc

    if True:
        if "adapterDimerPerc" in keep:
            headers["adapterDimerPerc"] = {
                'title': '% Dimers',
                'description': 'The percentage of reads that correspond to adapter-dimer, i.e. those that are shorter or equal to 2nt after adapter trimming ',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict["adapterDimerPerc"], "asc"),
                'bar_dict': columns_dict["adapterDimerPerc"],
                'suffix': '%',
            }
        if "ultraShortReadsPerc" in keep:
            headers["ultraShortReadsPerc"] = {
                'title': '% ultrashort',
                'description': 'Reads between 3 and 14 nt. A high number of these usually indicates issues in library preparation or low RNA quality',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict["ultraShortReadsPerc"], "asc"),
                'bar_dict': columns_dict["ultraShortReadsPerc"],
                'suffix': '%',
            }
        if "shortReadsPerc" in keep:
            headers["shortReadsPerc"] = {
                'title': '% short reads',
                'description': 'Reads between 15 and 17 nt. This range was choosen because tRNA fragments are frequently of 18 nt length.',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict["shortReadsPerc"], "asc"),
                'bar_dict': columns_dict["shortReadsPerc"],
                'suffix': '%',
            }
        if "rRNAPerc" in keep:
            headers["rRNAPerc"] = {
                        'title': '% rRNA',
                        'description': 'The percentage of ribosomal RNA derived reads',
                        'scale': "quart",
                        'col_dict': gen_col_dict(columns_dict["rRNAPerc"], "asc"),
                        'bar_dict': columns_dict["rRNAPerc"],
                        'suffix': '%',
                    }


    val_tab = table.plot(vals_dict, headers)
    for k in list(headers.keys()):
        c_dict = headers.get(k)
        description = c_dict["description"]
        c_dict["description"] = description + " (percentile)"
        c_dict['is_int'] = False
        if k in keep:
            c_dict['suffix'] = "show_perc"
            c_dict["suffix_dict"] = get_ordinals(columns_dict[k])

    perc_tab = table.plot(perc_dict, headers)




    return val_tab, perc_tab


def contamination_tab(val_df,perc_df, columns):
    vals_dict = df2dict(val_df)
    columns_dict = columns
    perc_dict = df2dict(perc_df)
    headers = OrderedDict()

    to_keep = ["refSpecies","unmapped","bacteria","virus"]
    keep = set(to_keep).intersection(list(val_df.columns))



    if True:
        if "refSpecies" in keep:
            headers["refSpecies"] = {
                'title': '% ref.genome',
                'description': 'Percentage of reads mapped to the reference genome',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict["refSpecies"], "desc"),
                'bar_dict': columns_dict["refSpecies"],
                'suffix': '%',
            }

        if "unmapped" in keep:
            headers["unmapped"] = {
                'title': '% unmapped',
                'description': 'Percentage of reads not mapped to the genome',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict["unmapped"], "asc"),
                'bar_dict': columns_dict["unmapped"],
                'suffix': '%',
            }

        if "bacteria" in keep:
            headers["bacteria"] = {
                'title': '% bacteria',
                'description': 'Percentage of reads mapped to a collection of different bacteria',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict["bacteria"], "asc"),
                'bar_dict': columns_dict["bacteria"],
                'suffix': '%',
            }

        if "virus" in keep:
            headers["virus"] = {
                'title': '% virus',
                'description': 'Percentage of reads mapped to a collection of different virus',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict["virus"], "asc"),
                'bar_dict': columns_dict["virus"],
                'suffix': '%',
            }

    val_tab = table.plot(vals_dict, headers)
    for k in list(headers.keys()):
        c_dict = headers.get(k)
        description = c_dict["description"]
        c_dict["description"] = description + " (percentile)"
        c_dict['is_int'] = False
        if k in keep:
            c_dict['suffix'] = "show_perc"
            c_dict["suffix_dict"] = get_ordinals(columns_dict[k])

    perc_tab = table.plot(perc_dict, headers)

    return val_tab, perc_tab


def length_tab(val_df,perc_df, columns):
    vals_dict = df2dict(val_df)
    columns_dict = columns
    perc_dict = df2dict(perc_df)
    headers = OrderedDict()

    to_keep = ["mainPeakMiRNAlength","stdDevMiRNAlength","modeMiRNAlength","meanMiRNAlength","skewnessMiRNAlength","absskewnessMiRNAlength"]
    keep = set(to_keep).intersection(list(val_df.columns))





    if True:
        if "mainPeakMiRNAlength" in keep:
            headers["mainPeakMiRNAlength"] = {
                'title': 'miRNA "peak"',
                # 'title': 'miRNA lengths',
                'description': 'Percentage of miRNA reads of lengths 21, 22 and 23',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict["mainPeakMiRNAlength"], "desc"),
                'bar_dict': columns_dict["mainPeakMiRNAlength"],
                'suffix': '%',
                # 'max': 100,
                # 'min': 0,
            }
        if "meanMiRNAlength" in keep:
            headers["meanMiRNAlength"] = {
                'title': 'miRNA mean length',
                'description': 'Mean of miRNA mapping reads read length',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict["meanMiRNAlength"], "desc"),
                'bar_dict': columns_dict["meanMiRNAlength"],
                # 'suffix': '%',
            }

        if "stdDevMiRNAlength" in keep:
            headers["stdDevMiRNAlength"] = {
                'title': 'miRNA SD',
                # 'title': 'microRNA mapping reads length SD',
                'description': 'Read length standard deviation of miRNA mapping reads',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict["stdDevMiRNAlength"], "asc"),
                'bar_dict': columns_dict["stdDevMiRNAlength"],
                # 'suffix': '%',
                # 'max': 100,
                # 'min': 0,
            }

        if "modeMiRNAlength" in keep:
            headers["modeMiRNAlength"] = {
                'title': 'miRNA length mode',
                'description': 'miRNA length mode',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict["modeMiRNAlength"], "desc"),
                'bar_dict': columns_dict["modeMiRNAlength"],
                'is_int': True
                # 'suffix': '%',
            }



        if "skewnessMiRNAlength" in keep:
            headers["skewnessMiRNAlength"] = {
                'title': 'skewness',
                'description': 'skewness read length distribution',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict["skewnessMiRNAlength"], "desc"),
                'bar_dict': columns_dict["skewnessMiRNAlength"],
                # 'suffix': '%',
            }
        if "absskewnessMiRNAlength" in keep:
            headers["absskewnessMiRNAlength"] = {
                'title': '|skewness|',
                'description': 'absolute read length distribution skewness',
                'scale': "quart",
                'col_dict': gen_col_dict(columns_dict["absskewnessMiRNAlength"], "desc"),
                'bar_dict': columns_dict["absskewnessMiRNAlength"],
                # 'suffix': '%',
            }
    val_tab = table.plot(vals_dict, headers)
    for k in list(headers.keys()):
        c_dict = headers.get(k)
        description = c_dict["description"]
        c_dict["description"] = description + " (percentile)"
        c_dict['is_int'] = False
        if k in keep:
            c_dict['suffix'] = "show_perc"
            c_dict["suffix_dict"] = get_ordinals(columns_dict[k])

    perc_tab = table.plot(perc_dict, headers)

    return val_tab, perc_tab


#old
# def seqYield_table(val_df,perc_df):
#
#     vals_dict = df2dict(val_df)
#     columns_dict = cols_dict(perc_df)
#
#     perc_dict = df2dict(perc_df)
#     headers = OrderedDict()
#
#     #headers
#
#     #readsRaw  # reads # readsAdapterFound # readsAdapterFoundPerc # readsAdapterNotFound
#     #  readsAdapterNotFoundPerc # readsUnique # avgRCperUnique # detectedMatureSA
#
#     if True:
#         headers["readsRaw"] = {
#             'title': 'Input reads',
#             'description': 'Total number of reads sequenced2',
#             'scale': "quart",
#             'col_dict': gen_col_dict(columns_dict["readsRaw"], "desc"),
#             'bar_dict': columns_dict["readsRaw"],
#             # 'max': 100,
#             # 'min': 0,
#
#         }
#
#         headers["reads"] = {
#             'title': '% reads in analysis',
#             'description': 'Total number of reads used for the analysis after filtering',
#             'scale': "quart",
#             'col_dict': gen_col_dict(columns_dict["reads"], "desc"),
#             'bar_dict': columns_dict["reads"],
#             'suffix': '%',
#
#         }
#
#
#         headers["readsAdapterFound"] = {
#             'title': 'Adapter trimmed reads',
#             'description': '',
#             'scale': "quart",
#             'col_dict': gen_col_dict(columns_dict["readsAdapterFound"], "desc"),
#             'bar_dict': columns_dict["readsAdapterFound"],
#             # 'suffix': '%',
#             # 'max': 100,
#             # 'min': 0,
#         }
#
#         headers["readsAdapterFoundPerc"] = {
#             'title': '% Adapter trimmed reads',
#             'description': 'Percentage of reads for which the adapter was found',
#             'scale': "quart",
#             'col_dict': gen_col_dict(columns_dict["readsAdapterFoundPerc"], "desc"),
#             'bar_dict': columns_dict["readsAdapterFoundPerc"],
#             'suffix': '%',
#             # 'max': 100,
#             # 'min': 0,
#         }
#
#
#         headers["readsUnique"] = {
#             'title': 'Unique sequences',
#             # 'title': 'microRNA mapping reads length SD',
#             'description': 'Number of unique sequences',
#             'scale': "quart",
#             'col_dict': gen_col_dict(columns_dict["readsUnique"], "asc"),
#             'bar_dict': columns_dict["readsUnique"],
#             # 'suffix': '%',
#             # 'max': 100,
#             # 'min': 0,
#         }
#
#
#     val_tab = table.plot(vals_dict, headers)
#
#
#     for k in list(headers.keys()):
#         c_dict = headers.get(k)
#         description = c_dict["description"]
#         c_dict["description"] = description + " (percentile)"
#         c_dict['suffix'] = "show_perc"
#         c_dict['is_int'] = False
#         c_dict["suffix_dict"] = get_ordinals(columns_dict[k])
#
#
#     perc_tab = table.plot(perc_dict, headers)
#
#     return val_tab,perc_tab
