from collections import OrderedDict
import results.mqc_table as table
from multiqc import config
import pandas
import os
from miRQC.settings import MEDIA_ROOT, MEDIA_URL, SUB_SITE, MEDIA_URL


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

def gen_col_dict(input_dict, sense):

    return {k: get_quart_cols(v,sense) for k, v in input_dict.items()}


def table2dict(filepath):
    table = pandas.read_csv(filepath, sep="\t")
    new_dict = {}
    samples = table['Sample'].values

    for sample in samples:
        subset = table.loc[table['Sample'] == sample]
        subset = subset.drop(["Sample"],1)
        new_dict[sample] = subset.to_dict("records")[0]

    return new_dict

def cols_dict(input_file):
    table = pandas.read_csv(input_file, sep="\t", index_col=0)
    new_dict = {}
    columns = table.columns
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


data = table2dict(values_tab)


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
    # rawN	analysisP	microP	detectedN	uniqueP
    headers["rawN"] = {
        'title': 'Input reads',
        'description': 'Total number of reads sequenced',
        'scale': "quart",
        'col_dict': gen_col_dict(columns_dict["rawN"], "desc"),
        'bar_dict': columns_dict["rawN"],
        # 'max': 100,
        # 'min': 0,

    }
    headers["analysisP"] = {
        'title': '% Reads in Analysis',
        'description': 'Percentage of reads included in the analysis',
        'scale': "quart",
        'col_dict': gen_col_dict(columns_dict["analysisP"], "desc"),
        'bar_dict': columns_dict["analysisP"],
        # 'suffix': '%',
        'max': 100,
        'min': 0,

    }
    headers["microP"] = {
        'title': '% miRNAs reads',
        'description': 'Percentage of reads mapping to miRNA libraries',
        'scale': "quart",
        'col_dict': gen_col_dict(columns_dict["microP"], "desc"),
        'bar_dict': columns_dict["microP"],
        # 'suffix': '%',
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
        # 'suffix': '%',
        'max': 100,
        'min': 0,

    }

    val_tab = table.plot(vals_dict, headers)

    headers["rawN"] = {
        'title': 'Input reads',
        'description': 'Total number of reads sequenced',
        'scale': "quart",
        'col_dict': gen_col_dict(columns_dict["rawN"], "desc"),
        'bar_dict': columns_dict["rawN"],
        # 'max': 100,
        # 'min': 0,

    }
    headers["analysisP"] = {
        'title': '% Reads in Analysis',
        'description': 'Percentage of reads included in the analysis',
        'scale': "quart",
        'col_dict': gen_col_dict(columns_dict["analysisP"], "desc"),
        'bar_dict': columns_dict["analysisP"],
        # 'suffix': '%',
        'max': 100,
        'min': 0,

    }
    headers["microP"] = {
        'title': '% miRNAs reads',
        'description': 'Percentage of reads mapping to miRNA libraries',
        'scale': "quart",
        'col_dict': gen_col_dict(columns_dict["microP"], "desc"),
        'bar_dict': columns_dict["microP"],
        # 'suffix': '%',
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
        # 'suffix': '%',
        'max': 100,
        'min': 0,

    }

    perc_tab = table.plot(perc_dict, headers)



    return val_tab, perc_tab
    # return val_tab, perc_tab


def test_table():

    return tables_yield(values_tab,perc_tab)

#
# def test_table():
#
#     return table.plot(data, headers, config_p)