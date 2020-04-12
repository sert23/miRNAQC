from django.shortcuts import render
from django.views.generic import FormView, DetailView
from .tables import basic_table, tables_yield, cols_dict, seq_qual_tab, library_tab, tables_complex, contamination_tab, length_tab, par_table
from miRQC.settings import MEDIA_ROOT, MEDIA_URL, SUB_SITE, MEDIA_URL, MAIN_SITE, VAR_DICT_PATH
import os
import pandas
import plotly.graph_objs as go
from plotly.offline import plot
import numpy as np
from django.http import JsonResponse
from django.urls import reverse_lazy
import math
from random import randrange
import json
from collections import OrderedDict
from newJob.views import parse_web_log


with open(VAR_DICT_PATH) as json_file:
    var_dict = json.load(json_file)

def parse_errors(log_path):

    tagged = ""
    if os.path.exists(log_path):
        with open(log_path,"r") as log_file:
            for line in log_file.readlines():
                if "ERROR" in line:
                    tagged = tagged + line + "<br>"
                if "WEB:" in line:
                    rem, keep = line.rstrip().split("WEB:")
                    tagged = tagged + keep + "<br>"

        return tagged
    else:
        return None



# Create your views here.

def discrete_colorscale(bvals, colors):
    """
    bvals - list of values bounding intervals/ranges of interest
    colors - list of rgb or hex colorcodes for values in [bvals[k], bvals[k+1]],0<=k < len(bvals)-1
    returns the plotly  discrete colorscale
    """
    if len(bvals) != len(colors) + 1:
        raise ValueError('len(boundary values) should be equal to  len(colors)+1')
    bvals = sorted(bvals)
    nvals = [(v - bvals[0]) / (bvals[-1] - bvals[0]) for v in bvals]  # normalized values

    dcolorscale = []  # discrete colorscale
    for k in range(len(colors)):
        dcolorscale.extend([[nvals[k], colors[k]], [nvals[k + 1], colors[k]]])
    return dcolorscale

def plot_percentiles(input_df=None,input_file=None, scale=None, tag=None):

    tick = ""
    tag_dict = var_dict.get(tag)
    if tag_dict:
        colorscale = tag_dict.get("color_scale")
        if tag_dict.get("is_percentage"):
            tick = "%"
    else:
        colorscale = None
    if colorscale == "asc":
        scale_list = ['rgb(164, 207, 99)']*26 + ['rgb(232, 213, 89)']*25 + ['rgb(251, 163,83)']*25 + ['rgb(221,90,78)']*25
    elif colorscale == "desc":
        scale_list = ['rgb(221,90,78)'] * 26 + ['rgb(251, 163,83)'] * 25 + ['rgb(232, 213, 89)'] * 25 + ['rgb(164, 207, 99)'] * 25
    else:
        scale_list = 101 * ["#1f77b4"]

    perc_df = pandas.read_csv(input_file, sep="\t")
    perc_df["bar_color"] = scale_list
    data = [go.Bar(name="percentile",
        x=perc_df.percentile.values,
                         y=perc_df.value.values,
                  marker=dict(color=perc_df.bar_color.values),
                  hovertemplate="%{x}p: %{y}",
                   showlegend=False
                  )]
                         # colorscale=dcolorsc,

    # print(perc_df.shape)


    if scale == "log10":
        scale = "log"
    else:
        scale = "linear"
    annotation = []
    # print(input_df.columns)
    if input_df.shape[0] < 6:

        for row in input_df.iterrows():
            x = math.ceil(row[1].values[1])
            r = randrange(50)

            sample = row[1].values[0]
            old_y = row[1].values[2]
            y = old_y
            if scale == "log":
                try:
                    y = math.log10(y)
                    # print("hehe")
                except:
                    y = 0
            # print("new")
            # # print(row[0].values)
            # print()

            annotation.append(
                dict(
                    x=x,
                    y=y,
                    # xref="x",
                    # yref="y",
                    text=sample,
                    hovertext="Sample: {} <br>Value: {}{}<br>Percentile: {}".format(sample,round(old_y,2),tick,x),
                    showarrow=True,
                    arrowhead=3,
                    ax=20+r,
                    ay=-30-r,
                    # bordercolor="#FFFFFF",
                    font = dict(
                        color="#FFFFFF",
                    ),

                    bordercolor="#000000",
                    borderwidth=1,
                    borderpad=4,
                    bgcolor="#1f77b4",
                    # bgcolor="#ff7f0e",
                    # editable=True
                )

            )
            # print(row[1].values[0])
    else:

        # print(input_df.iloc[:,1].values)
        input_df.iloc[:, 1] = input_df.iloc[:,1].round()
        input_df.iloc[:, 2] = input_df.iloc[:,2].round(2)
        input_df["hover"] = input_df.iloc[:, 0].astype(str) +":  "+ input_df.iloc[:, 2].astype(str)
        unique_percentiles = set(input_df.iloc[:, 1].values)

        step = perc_df.iloc[:, 0].max()/float(50)
        for p in unique_percentiles:
            sub_df = input_df.loc[(input_df.iloc[:, 1] ==p)]
            x = p
            # print(perc_df.columns)
            old_y = perc_df.loc[(perc_df.iloc[:, 0] ==p)].value.values[0]
            y = old_y
            # if scale == "log":
            #     try:
            #         #y = math.log10(y)
            #         print("hehe")
            #     except:
            #         y = 0
            # print(input_df.columns)
            print(y)
            # text = "<br>".join(sub_df.iloc[:, 0].values )
            # text = "Percentile " + str(int(p)) + ":<br> "  + str(sub_df.shape[0]) + " samples"
            new_line = tick +"<br>"
            # new_line = "%" +"<br>"
            hover = new_line.join(sub_df["hover"].values)+tick
            trace = go.Scatter(
                name="Percentile " + str(int(p)),
                x=[x],
                y=[y],
                marker=dict(
                color="#1f77b4"),
                # text= [hover]),
                hovertemplate=hover,
                showlegend=False
            )
            data.append(trace)
            # r = randrange(100)
            # annotation.append(
            #     dict(
            #         x=x,
            #         y=y,
            #         # xref="x",
            #         # yref="y",
            #         text=text,
            #         hovertext=hover,
            #         showarrow=True,
            #         arrowhead=3,
            #         ax=20 + r,
            #         ay=-30 - r,
            #         # bordercolor="#FFFFFF",
            #         font=dict(
            #             color="#FFFFFF",
            #         ),
            #
            #         bordercolor="#000000",
            #         borderwidth=1,
            #         borderpad=4,
            #         bgcolor="#1f77b4",
            #         # bgcolor="#ff7f0e",
            #         # editable=True
            #     )
            #
            # )



    layout = go.Layout(
        # autosize=False,
        # width=500,
        # scene = dict(
        #     annotations = [annoation],
        title =  var_dict.get(tag).get("full_name"),
        annotations=annotation,

        margin=go.layout.Margin(
            l=200,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
        xaxis=dict(
            title="Percentiles"
        ),
        yaxis=dict(
            title = var_dict.get(tag).get("full_name") ,
            type=scale,
            # dtick = 1,
            showexponent='all',
            exponentformat='power',
            ticksuffix=tick,
            # tickformat=".2f",
            ),

    )
    fig = go.Figure(data=data, layout=layout)


    # fig.update_layout(autosize=False)
    # div = plot(fig, show_link=False, auto_open=False, include_plotlyjs=False, output_type="div")
    div = plot(fig, show_link=False, auto_open=False, include_plotlyjs=False, output_type="div", config={'editable': True})
    return div

def reverse_scale(input_values):
    rvals = [(-1) * (x-100) for x in input_values]
    return rvals

def fix_scale(input_df):
    pandas.options.mode.chained_assignment = None
    for column_name in input_df.columns.values:
        tag_dict = var_dict.get(column_name)
        if tag_dict:
            if tag_dict.get("color_scale") == "asc" :
                input_df.loc[:,column_name] = reverse_scale(input_df[column_name].values)
    pandas.options.mode.chained_assignment = 'warn'
    return input_df

def plot_heatmap(input_df=None):
    bvals = [0 , 25, 50, 75, 100]
    # bvals = [0 , 25, 50, 75, 100]

    to_keep = ["readsRaw", "readsPerc","adapterDimerPerc","detectedMatureSA","maturePercofReads","meanofp50",
               "mainPeakMiRNAlength","stdDevMiRNAlength"]

    # colors = ['#09ffff', '#19d3f3', '#e763fa', '#ab63fa']
    colors = ['rgb(164, 207, 99)', 'rgb(232, 213, 89)', 'rgb(251, 163,83)', 'rgb(221,90,78)']
    colors.reverse()
    bvals = np.array(bvals)
    tickvals = [np.mean(bvals[k:k + 2]) for k in
                range(len(bvals) - 1)]  # position with respect to bvals where ticktext is displayed
    # ticktext = [f'<{bvals[1]}'] + [f'{bvals[k]}-{bvals[k+1]}' for k in range(1, len(bvals) - 2)] + [f'>{bvals[-2]}']
    ticktext = ["Q1","Q2","Q3","Q4"]
    ticktext.reverse()
    dcolorsc = discrete_colorscale(bvals, colors)
    print(dcolorsc)
    perc_df = input_df
    basic_df = perc_df[to_keep]
    # z = np.random.randint(bvals[0], bvals[-1] + 1, size=(20, 20))
    # z = [[10,30,50,60,70,80,90,100,100]]
    test_values = [0.10,0.30,0.31,0.34,0.35,0.40,0.60,0.70,0.80,1.00]
    other_values = test_values.copy()
    other_values.reverse()
    z = [test_values,other_values]
    # print(dcolorsc)
    # print(ticktext)
    # print(tickvals)
    quartiles = ["Q1","Q2","Q3","Q4"]
    quartiles.reverse()
    x = [var_dict.get(n).get("full_name") for n in basic_df.columns.values]
    basic_df = fix_scale(basic_df)
    print(perc_df["sample"].values)
    heatmap = go.Heatmap(x=x,
                         y=perc_df["sample"].values,
                         z=basic_df.values,
                         colorscale=dcolorsc,
                         zmin=0,
                         zmax=100,
                         # hovertemplate="HEHE{x}",   # Hover can be applied if text is provided, hovertemplate not working
                         # text = ["hehe"],
                         # hoverinfo="text",
                         # hovertemplate="%{x}p: %{y}",
                         colorbar=dict(thickness=25,
                                       # tickvals=tickvals,
                                       tickvals=[14, 38, 62.5, 87.5],
                                       # tickvals=[18, 39, 62.5, 82.5],
                                       ticktext=quartiles))
    layout = go.Layout(
        # autosize=False,
        # width=500,
        title="Samples percentiles for main quality statistics",
        # height=500,
        margin=go.layout.Margin(
                l=200,
                r=150,
                b=150,
                t=100,
                pad=4))
        # margin=go.layout.Margin(
        #     l=200,
        #     r=50,
        #     b=100,
        #     t=100,
        #     pad=4
        # )

    fig = go.Figure(data=[heatmap], layout=layout)
    # fig.update_layout(autosize=False)
    div = plot(fig, show_link=False, auto_open=False, include_plotlyjs=False, output_type="div")
    return div

def parse_perc_files(comparison_folder):

    folder = os.path.join(comparison_folder ,"percentiles")
    files = [ f.replace("_percentiles.tsv","") for f in os.listdir(folder) if
             os.path.isfile(os.path.join(folder, f))]
    names = [[x,var_dict.get(x).get("short_name")] for x in files if var_dict.get(x)]

    snames = sorted(names, key=lambda x: str.lower(x[1]))

    # snames = sorted(names, key=)
    #fs = sorted(files, key=str.lower)
    #names = [var_dict.get(x).get("short_name") for x in fs if var_dict.get(x)]

    return snames

def ajax_heatmap(request):

    folder = request.GET.get('id', None)
    comparison = request.GET.get('comp_set', None)
    query_folder = os.path.join(MEDIA_ROOT, folder, "query", "comparisons" ,comparison)
    perc_file = os.path.join(query_folder, "percentil.tsv")

    # read files into dfs
    perc_df = pandas.read_csv(perc_file, sep="\t")
    data = {}
    data["plot"] = plot_heatmap(perc_df)
    return JsonResponse(data)

def ajax_percentiles(request):

    folder = request.GET.get('id', None)
    comparison = request.GET.get('comp_set', None)
    query_folder = os.path.join(MEDIA_ROOT, folder, "query", "comparisons", comparison)
    variable = request.GET.get('variable', None)
    scale = request.GET.get('scale', None)

    perc_file = os.path.join(query_folder, "percentil.tsv")
    val_file = os.path.join(query_folder, "value.tsv")
    perc_df = pandas.read_csv(perc_file, sep="\t")[["sample",variable]]
    val_df = pandas.read_csv(val_file, sep="\t")[["sample",variable]]
    val_df.columns = ["sample","values"]
    perc_df = perc_df.join(val_df.set_index('sample'), on='sample')
    # perc_df = perc_df.set_index('sample').join(val_df.set_index('sample'))
    # print(perc_df.columns)
    # print(perc_df)
    # exit()
    filepath = os.path.join(query_folder,"percentiles",variable + "_percentiles.tsv")
    # read files into dfs

    data = {}

    data["plot"] = plot_percentiles(perc_df, filepath, scale, variable)
    return JsonResponse(data)


class testMulti(FormView):

    def get(self, request):
        context = {}
        # t1,t2 = test_table()
        # context["test_table"] = t1
        # context["test_table2"] = t2

        # print("hey")
        # return render(self.request, 'test_table.html', context)
        perc_file = "/Users/ernesto/PycharmProjects/miRQC/upload/test/query/percentil_full.tsv"

        # read files into dfs
        perc_df = pandas.read_csv(perc_file, sep="\t")
        context["test_div"] = plot_heatmap(perc_df)
        return render(self.request, 'plotly_test.html', context)

class loadResults(FormView):

    def get(self, request):
        try:

            context = {}
            path = request.path
            #get folder from pathresults for job
            folder = path.split("/")[-1]
            context["jobID"] = folder
            context["result_url"] = reverse_lazy("check_status") + "/" + folder
            context["absolute_url"] = MAIN_SITE
            comp_folder = os.path.join(MEDIA_ROOT,folder,"query", "comparisons")
            with open(os.path.join(comp_folder,"config.json")) as d_file:
                comp_dict = json.load(d_file, object_pairs_hook=OrderedDict)
            comparison = path.split("/")[-2]
            if comparison not in comp_dict.keys():
                comparison = "vsAll"

            query_folder = os.path.join(MEDIA_ROOT,folder,"query", "comparisons", comparison)

            # comparisons = [[f,comp_dict.get(f)] for f in os.listdir(comp_folder) if
            #          os.path.isdir(os.path.join(comp_folder, f))]
            comparisons = [[f, comp_dict.get(f)] for f in comp_dict.keys() if os.path.isdir(os.path.join(comp_folder, f))]
            # print(comparisons)
            # query_folder = os.path.join(MEDIA_ROOT,folder,"query",)
            val_file = os.path.join(query_folder,"value.tsv")
            perc_file = os.path.join(query_folder,"percentil.tsv")
            context["vals_link"] = val_file.replace(MEDIA_ROOT,MEDIA_URL)
            context["perc_link"] = perc_file.replace(MEDIA_ROOT,MEDIA_URL)

            #parameters
            context["par_tab"] = par_table(os.path.join(MEDIA_ROOT,folder,"query", "comparisons","summary_results.tsv"))

            #errrors/warnings
            context["warns"] = parse_errors(os.path.join(MEDIA_ROOT,folder,"query", "comparisons","summaryqc.log"))
            print("hee")
            print(context["warns"])
            # print(parse_web_log(os.path.join(MEDIA_ROOT,folder,"query", "comparisons","summaryqc.log")))

            #read files into dfs
            val_df = pandas.read_csv(val_file, sep="\t")
            perc_df = pandas.read_csv(perc_file, sep="\t")
            columns = cols_dict(perc_df)
            # context["basic_hm"] = plot_heatmap(perc_df)
            #basic statistics
            basic_tab,basic_perc = basic_table(val_df, perc_df, columns)
            context["basic_table"] = basic_tab
            context["basic_perc"] = basic_perc
            context["comp_list"] = comparisons

            #sequencing yield
            seqYield_tab, seqYield_perc = tables_yield(val_df, perc_df, columns)
            context["seqYield_table"] = seqYield_tab
            context["seqYield_perc"] = seqYield_perc

            # library complexity
            complex_tab, complex_perc = tables_complex(val_df, perc_df, columns)
            context["complex_table"] = complex_tab
            context["complex_perc"] = complex_perc

            #sequencing quality
            seqQual_tab, seqQual_perc = seq_qual_tab(val_df, perc_df, columns)
            context["seqQual_table"] = seqQual_tab
            context["seqQual_perc"] = seqQual_perc

            # library quality
            library_table, library_perc = library_tab(val_df, perc_df, columns)
            context["library_table"] = library_table
            context["library_perc"] = library_perc

            # contamination

            cont_table, cont_perc = contamination_tab(val_df, perc_df, columns)
            context["contam_table"] = cont_table
            context["contam_perc"] = cont_perc

            # length distribution

            len_table, len_perc = length_tab(val_df, perc_df, columns)
            context["length_table"] = len_table
            context["length_perc"] = len_perc

            context["sub_site"] = SUB_SITE
            context["comparison"] = comparison

            # percentiles
            # print(os.path.join(query_folder,"percentiles"))
            if os.path.exists(os.path.join(query_folder,"percentiles")):
                context["perc_list"] = parse_perc_files(query_folder)
            # t1,t2 = test_table()
            # context["test_table"] = t1
            # context["test_table2"] = t2

            # print("hey")
            # return render(self.request, 'test_table.html', context)
            return render(self.request, 'results.html', context)
        except:
            context = {}
            path = request.path
            # get folder from path
            finished = False
            folder = path.split("/")[-1]
            context["jobID"] = folder
            context["result_url"] = reverse_lazy("check_status") + "/" + folder
            context["absolute_url"] = MAIN_SITE
            logfile = os.path.join(MEDIA_ROOT, folder, "query", "comparisons", "summaryqc.log")
            if os.path.exists(logfile):
                launched = True
            else:
                launched = False

            if launched:
                message, finished = parse_web_log(logfile)
                context["message"] = message
                return render(self.request, 'status.html', context)
            else:
                context["message"] = "Your Job is in queue"
                return render(self.request, 'status.html', context)
