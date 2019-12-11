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
    else:
        if input_val > 75:
            col = 'rgb(221,90,78)'
        elif input_val > 50:
            col = 'rgb(251, 163,83)'
        elif input_val > 25:
            col = 'rgb(232, 213, 89)'
        else:
            col = 'rgb(164, 207, 99)'
        return col

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
        return " "

    n = int(n)

    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return suffix



def get_ordinals(input_dict):

    return {k: make_ordinal(v) for k, v in input_dict.items()}

def gen_col_dict(input_dict, sense):

    return {k: get_quart_cols(v,sense) for k, v in input_dict.items()}



def df2dict(df):
    table = df
    new_dict = {}
    print(table.columns)
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
    print(columns)
    for column in columns:
        subset = table[column]
        new_dict[column] = subset.to_dict()
        # print(column)
    return new_dict

# print(cols_dict(perc_tab))


# print(table2dict(values_tab))
#
# exit()

data = {
    'sample 1': {
        'aligned': 235420000000000,
        'not_aligned': 343,
        'aligned_percent': 98.563952271
    },
    'sample 2': {
        'aligned': 12750000000000,
        'not_aligned': 7328,
        'aligned_percent': 14.820411484
    }
}


# data = table2dict(values_tab)


headers = OrderedDict()



headers['aligned_percent'] = {
    'scale': "quart",
    'col_dict': {'sample 1':  "rgb(164, 207, 99)", 'sample 2' : 'rgb(232, 213, 89)'},
    'title': '% Aligned',
    'description': 'Percentage of reads that aligned',
    'suffix': '%',
    'max': 200,
    'format': '{:,.0f}' # No decimal places please
}
headers['aligned'] = {
    'title': '{} Aligned'.format(config.read_count_prefix),
    'description': 'Aligned Reads ({})'.format(config.read_count_desc),
    'shared_key': 'read_count',
    # 'modify': lambda x: x * config.read_count_multiplier
}



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



def tables_yield(val_file, perc_file):

    vals_dict = table2dict(val_file)
    columns_dict = cols_dict(perc_file)
    perc_dict = table2dict(perc_file)
    headers = OrderedDict()
    # rawReads_orig	reads	adapterDimer	detectedMatureSA
    headers["rawReads_orig"] = {
        'title': 'Input reads',
        'description': 'Total number of reads sequenced',
        'scale': "quart",
        'col_dict': gen_col_dict(columns_dict["rawReads_orig"], "desc"),
        'bar_dict': columns_dict["rawReads_orig"],
        # 'max': 100,
        # 'min': 0,

    }
    headers["analysisP"] = {
        'title': '% Reads in Analysis',
        'description': 'Percentage of reads included in the analysis',
        'scale': "quart",
        'col_dict': gen_col_dict(columns_dict["analysisP"], "desc"),
        'bar_dict': columns_dict["analysisP"],
        'suffix': '%',
        'max': 100,
        'min': 0,

    }
    headers["microP"] = {
        'title': '% miRNAs reads',
        'description': 'Percentage of reads mapping to miRNA libraries',
        'scale': "quart",
        'col_dict': gen_col_dict(columns_dict["microP"], "desc"),
        'bar_dict': columns_dict["microP"],
        'suffix': '%',
        'max': 100,
        'min': 0,

    }
    headers["detectedN"] = {
        'title': 'miRNAs detected',
        'description': 'Number of miRNAs detected',
        'scale': "quart",
        'col_dict': gen_col_dict(columns_dict["detectedN"], "desc"),
        'bar_dict': columns_dict["detectedN"],


    }
    headers["uniqueP"] = {
        'title': '% Unique reads',
        'description': 'Percentage of unique reads',
        'scale': "quart",
        'col_dict': gen_col_dict(columns_dict["uniqueP"], "desc"),
        'bar_dict': columns_dict["uniqueP"],
        'suffix': '%',
        'max': 100,
        'min': 0,

    }

    val_tab = table.plot(vals_dict, headers)

    headers["rawReads_orig"] = {
        'title': 'Input reads',
        'description': 'Total number of reads sequenced (percentile)',
        'scale': "quart",
        'col_dict': gen_col_dict(columns_dict["rawReads_orig"], "desc"),
        'bar_dict': columns_dict["rawReads_orig"],
        # 'max': 100,
        # 'min': 0,

    }
    headers["analysisP"] = {
        'title': '% Reads in Analysis',
        'description': 'Percentage of reads included in the analysis (percentile)',
        'scale': "quart",
        'col_dict': gen_col_dict(columns_dict["analysisP"], "desc"),
        'bar_dict': columns_dict["analysisP"],
        # 'suffix': '%',
        'max': 100,
        'min': 0,

    }
    headers["microP"] = {
        'title': '% miRNAs reads',
        'description': 'Percentage of reads mapping to miRNA libraries (percentile)',
        'scale': "quart",
        'col_dict': gen_col_dict(columns_dict["microP"], "desc"),
        'bar_dict': columns_dict["microP"],
        # 'suffix': '%',
        'max': 100,
        'min': 0,

    }
    headers["detectedN"] = {
        'title': 'miRNAs detected',
        'description': 'Number of miRNAs detected (percentile)',
        'scale': "quart",
        'col_dict': gen_col_dict(columns_dict["detectedN"], "desc"),
        'bar_dict': columns_dict["detectedN"],

    }
    headers["uniqueP"] = {
        'title': '% Unique reads',
        'description': 'Percentage of unique reads (percentile)',
        'scale': "quart",
        'col_dict': gen_col_dict(columns_dict["uniqueP"], "desc"),
        'bar_dict': columns_dict["uniqueP"],
        # 'suffix': '%',
        'suffix': "show_perc",
        "suffix_dict": get_ordinals(columns_dict["uniqueP"]),
        'max': 100,
        'min': 0,

    }

    perc_tab = table.plot(perc_dict, headers)



    return val_tab, perc_tab
    # return val_tab, perc_tab

#
# def test_table():
#
#     return tables_yield(values_tab,perc_tab)

def basic_table(val_df,perc_df):

    vals_dict = df2dict(val_df)
    columns_dict = cols_dict(perc_df)

    perc_dict = df2dict(perc_df)
    headers = OrderedDict()

    #headers

    # readsRaw     # readsPerc     # adapterDimerPerc     # detectedMatureSA     # maturePercofReads
    #  meanofp50     # mainPeakMiRNAlength     # stdDevMiRNAlength
    if True:
        headers["readsRaw"] = {
            'title': 'Input reads',
            'description': 'Total number of reads sequenced',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict["readsRaw"], "desc"),
            'bar_dict': columns_dict["readsRaw"],
            # 'max': 100,
            # 'min': 0,

        }

        headers["readsPerc"] = {
            'title': '% reads in analysis',
            'description': 'Percentage of reads used for the analysis after filtering',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict["readsPerc"], "desc"),
            'bar_dict': columns_dict["readsPerc"],
            'suffix': '%',
            # 'max': 100,

            # 'min': 0,

        }
        headers["adapterDimerPerc"] = {
            'title': '% Adapter - dimer reads',
            'description': 'The percentage of reads that correspond to adapter-dimer, i.e. those that are shorter or equel to 2nt after adapter trimming ',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict["adapterDimerPerc"], "asc"),
            'bar_dict': columns_dict["adapterDimerPerc"],
            'suffix': '%',
        }
        headers["detectedMatureSA"] = {
            'title': 'Detected microRNAs',
            'description': 'Total number of mature miRNAs detected',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict["detectedMatureSA"], "desc"),
            'bar_dict': columns_dict["detectedMatureSA"],
            # 'max': 100,
            # 'min': 0,

        }
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

        headers["mainPeakMiRNAlength"] = {
            'title': '% miRNAs "peak"',
            # 'title': '% main miRNA lengths',
            'description': 'Percentage of miRNA reads of lengths 21, 22 and 23',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict["mainPeakMiRNAlength"], "desc"),
            'bar_dict': columns_dict["mainPeakMiRNAlength"],
            'suffix': '%',
            # 'max': 100,
            # 'min': 0,
        }
        headers["stdDevMiRNAlength"] = {
            'title': 'microRNA SD',
            # 'title': 'microRNA mapping reads length SD',
            'description': 'Read length standard deviation of miRNA mapping reads',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict["stdDevMiRNAlength"], "asc"),
            'bar_dict': columns_dict["stdDevMiRNAlength"],
            # 'suffix': '%',
            # 'max': 100,
            # 'min': 0,
        }



    val_tab = table.plot(vals_dict, headers)


    for k in list(headers.keys()):
        c_dict = headers.get(k)
        description = c_dict["description"]
        c_dict["description"] = description + " (percentile)"
        c_dict['suffix'] = "show_perc"
        c_dict["suffix_dict"] = get_ordinals(columns_dict[k])

    # if True:
    #
    #
    #     headers["readsRaw"] = {
    #         'title': 'Input reads',
    #         'description': 'Total number of reads sequenced',
    #         'scale': "quart",
    #         'col_dict': gen_col_dict(columns_dict["readsRaw"], "desc"),
    #         'bar_dict': columns_dict["readsRaw"],
    #         'suffix': "show_perc",
    #         "suffix_dict": get_ordinals(columns_dict["readsRaw"]),
    #         # 'max': 100,
    #         # 'min': 0,
    #
    #     }
    #
    #     headers["reads"] = {
    #         'title': '% reads in analysis',
    #         'description': 'Total number of reads used for the analysis after filtering',
    #         'scale': "quart",
    #         'col_dict': gen_col_dict(columns_dict["reads"], "desc"),
    #         'bar_dict': columns_dict["reads"],
    #         'suffix': "show_perc",
    #         "suffix_dict": get_ordinals(columns_dict["reads"]),
    #         # 'max': 100,
    #         # 'min': 0,
    #
    #     }

    perc_tab = table.plot(perc_dict, headers)

    return val_tab,perc_tab

def seqYield_table(val_df,perc_df):

    vals_dict = df2dict(val_df)
    columns_dict = cols_dict(perc_df)

    perc_dict = df2dict(perc_df)
    headers = OrderedDict()

    #headers

    #readsRaw  # reads # readsAdapterFound # readsAdapterFoundPerc # readsAdapterNotFound
    #  readsAdapterNotFoundPerc # readsUnique # avgRCperUnique # detectedMatureSA

    if True:
        headers["readsRaw"] = {
            'title': 'Input reads',
            'description': 'Total number of reads sequenced',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict["readsRaw"], "desc"),
            'bar_dict': columns_dict["readsRaw"],
            # 'max': 100,
            # 'min': 0,

        }

        headers["reads"] = {
            'title': '% reads in analysis',
            'description': 'Total number of reads used for the analysis after filtering',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict["reads"], "desc"),
            'bar_dict': columns_dict["reads"],
            'suffix': '%',

        }


        # headers["readsAdapterFound"] = {
        #     'title': 'Adapter trimmed reads',
        #     'description': '',
        #     'scale': "quart",
        #     'col_dict': gen_col_dict(columns_dict["readsAdapterFound"], "desc"),
        #     'bar_dict': columns_dict["readsAdapterFound"],
        #     # 'suffix': '%',
        #     # 'max': 100,
        #     # 'min': 0,
        # }

        # headers["readsAdapterFoundPerc"] = {
        #     'title': '% Adapter trimmed reads',
        #     'description': 'Percentage of reads for which the adapter was found',
        #     'scale': "quart",
        #     'col_dict': gen_col_dict(columns_dict["readsAdapterFoundPerc"], "desc"),
        #     'bar_dict': columns_dict["readsAdapterFoundPerc"],
        #     'suffix': '%',
        #     # 'max': 100,
        #     # 'min': 0,
        # }

        # headers["readsAdapterNotFound"] = {
        #     'title': 'Adapter not found',
        #     # 'title': '% main miRNA lengths',
        #     'description': 'The number of reads for which the adapter was not found',
        #     'scale': "quart",
        #     'col_dict': gen_col_dict(columns_dict["readsAdapterNotFound"], "desc"),
        #     'bar_dict': columns_dict["readsAdapterNotFound"],
        #     # 'suffix': '%',
        #     # 'max': 100,
        #     # 'min': 0,
        # }
        # headers["readsAdapterNotFoundPerc"] = {
        #     'title': '% Adapter not found',
        #     'description': 'Percentage of reads for which the adapter was not found',
        #     'scale': "quart",
        #     'col_dict': gen_col_dict(columns_dict["readsAdapterNotFoundPerc"], "desc"),
        #     'bar_dict': columns_dict["readsAdapterNotFoundPerc"],
        #     'suffix': '%',
        #     # 'max': 100,
        #     # 'min': 0,
        # }
        # headers["readsUnique"] = {
        #     'title': 'Unique sequences',
        #     # 'title': 'microRNA mapping reads length SD',
        #     'description': 'Number of unique sequences',
        #     'scale': "quart",
        #     'col_dict': gen_col_dict(columns_dict["readsUnique"], "asc"),
        #     'bar_dict': columns_dict["readsUnique"],
        #     # 'suffix': '%',
        #     # 'max': 100,
        #     # 'min': 0,
        # }
        headers["avgRCperUnique"] = {
            'title': 'Reads per unique read',
            'description': 'Number of reads in analysis divided by number of unique reads',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict["detectedMatureSA"], "desc"),
            'bar_dict': columns_dict["detectedMatureSA"],
            # 'max': 100,
            # 'min': 0,

        }
        headers["detectedMatureSA"] = {
            'title': 'Detected microRNAs',
            'description': 'Total number of mature miRNAs detected',
            'scale': "quart",
            'col_dict': gen_col_dict(columns_dict["detectedMatureSA"], "desc"),
            'bar_dict': columns_dict["detectedMatureSA"],
            # 'max': 100,
            # 'min': 0,

        }



    val_tab = table.plot(vals_dict, headers)


    for k in list(headers.keys()):
        c_dict = headers.get(k)
        description = c_dict["description"]
        c_dict["description"] = description + " (percentile)"
        c_dict['suffix'] = "show_perc"
        c_dict["suffix_dict"] = get_ordinals(columns_dict[k])

    # if True:
    #
    #
    #     headers["readsRaw"] = {
    #         'title': 'Input reads',
    #         'description': 'Total number of reads sequenced',
    #         'scale': "quart",
    #         'col_dict': gen_col_dict(columns_dict["readsRaw"], "desc"),
    #         'bar_dict': columns_dict["readsRaw"],
    #         'suffix': "show_perc",
    #         "suffix_dict": get_ordinals(columns_dict["readsRaw"]),
    #         # 'max': 100,
    #         # 'min': 0,
    #
    #     }
    #
    #     headers["reads"] = {
    #         'title': '% reads in analysis',
    #         'description': 'Total number of reads used for the analysis after filtering',
    #         'scale': "quart",
    #         'col_dict': gen_col_dict(columns_dict["reads"], "desc"),
    #         'bar_dict': columns_dict["reads"],
    #         'suffix': "show_perc",
    #         "suffix_dict": get_ordinals(columns_dict["reads"]),
    #         # 'max': 100,
    #         # 'min': 0,
    #
    #     }

    perc_tab = table.plot(perc_dict, headers)

    return val_tab,perc_tab
