from django.shortcuts import render
from django.views.generic import FormView, DetailView
from .tables import basic_table,seqYield_table
from miRQC.settings import MEDIA_ROOT, MEDIA_URL, SUB_SITE, MEDIA_URL
import os
import pandas
import plotly.graph_objs as go
from plotly.offline import plot
import numpy as np
from django.http import JsonResponse
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


def plot_heatmap(input_df=None):
    bvals = [0 , 25, 50, 75, 100]

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
    perc_df = input_df
    basic_df = perc_df[to_keep]
    # z = np.random.randint(bvals[0], bvals[-1] + 1, size=(20, 20))
    # z = [[10,30,50,60,70,80,90,100,100]]
    test_values = [0.10,0.30,0.31,0.34,0.35,0.40,0.60,0.70,0.80,1.00]
    other_values = test_values.copy()
    other_values.reverse()
    z = [test_values,other_values]
    print(dcolorsc)
    print(ticktext)
    print(tickvals)
    quartiles = ["Q1","Q2","Q3","Q4"]
    quartiles.reverse()
    heatmap = go.Heatmap(x=basic_df.columns,
                         y=perc_df["sample"].values,
                         z=basic_df.values,
                         colorscale=dcolorsc,
                         colorbar=dict(thickness=25,
                                       # tickvals=tickvals,
                                       tickvals=[20, 42, 65, 87.5],
                                       ticktext=quartiles))
    layout = go.Layout(
        # autosize=False,
        # width=500,

        # height=500,
        margin=go.layout.Margin(
            l=200,
            r=50,
            b=100,
            t=100,
            pad=4
        )
        )
    fig = go.Figure(data=[heatmap], layout=layout)
    # fig.update_layout(autosize=False)
    div = plot(fig, show_link=False, auto_open=False, include_plotlyjs=False, output_type="div")
    return div

def ajax_heatmap(jobID):

    folder = jobID
    query_folder = os.path.join(MEDIA_ROOT, folder, "query")
    perc_file = os.path.join(query_folder, "percentil_full.tsv")

    # read files into dfs
    perc_df = pandas.read_csv(perc_file, sep="\t")
    data = {}
    data["plot"] = plot_heatmap(perc_df)
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

        context = {}
        path = request.path
        #get folder from path
        folder = path.split("/")[-1]
        context["jobID"] = folder
        query_folder = os.path.join(MEDIA_ROOT,folder,"query")
        val_file = os.path.join(query_folder,"value_full.tsv")
        perc_file = os.path.join(query_folder,"percentil_full.tsv")

        #read files into dfs
        val_df = pandas.read_csv(val_file, sep="\t")
        perc_df = pandas.read_csv(perc_file, sep="\t")
        context["basic_hm"] = plot_heatmap(perc_df)

        #basic statistics
        basic_tab,basic_perc = basic_table(val_df, perc_df)
        context["basic_table"] = basic_tab
        context["basic_perc"] = basic_perc



        #sequencing yield
        seqYield_tab, seqYield_perc = seqYield_table(val_df, perc_df)
        context["seqYield_table"] = seqYield_tab
        context["seqYield_perc"] = seqYield_perc

        # t1,t2 = test_table()
        # context["test_table"] = t1
        # context["test_table2"] = t2

        # print("hey")
        # return render(self.request, 'test_table.html', context)
        return render(self.request, 'results.html', context)
