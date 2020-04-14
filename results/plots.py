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
import numpy


with open(VAR_DICT_PATH) as json_file:
    var_dict = json.load(json_file)

def tick_cleaner(ticks, dmin=0.05):
    maxi = ticks[-1]
    mini = ticks[0]
    mini_delta = (maxi-mini)*dmin

    print(mini_delta)
    print(ticks)
    t_copy = []
    for j,t in enumerate(ticks):
        if j <1:
            t_copy.append(t)
            continue
        ds = [abs(t-x) for x in t_copy]
        print(ds)
        if all(i >= mini_delta for i in ds):
            t_copy.append(t)
    return t_copy

def make_group_dict(input_file):
    group_df = pandas.read_csv(input_file, sep="\t")
    groups = group_df.group.unique()
    group_dict = OrderedDict()
    for g in groups:
        group_dict[g] = group_df[(group_df.group == g)]["sample"].values

    return group_dict


def plot_boxplots(input_df=None,input_file=None, scale=None, tag=None, disp="perc",groups_dict=None):
    alpha = 0.3
    colors = ['rgba(164, 207, 99,{})'.format(alpha), 'rgba(232, 213, 89,{})'.format(alpha),
              'rgba(251, 163,83,{})'.format(alpha), 'rgba(221,90,78,{})'.format(alpha)]
    groups = list(groups_dict.keys())
    x = list(range(len(groups) + 2))
    if scale == "log10":
        #scale = "log"
        scale = "linear"
    else:
        scale = "linear"

    tag_dict = var_dict.get(tag)
    if tag_dict:
        colorscale = tag_dict.get("color_scale")
        if tag_dict.get("is_percentage"):
            tick_su = "%"
        else:
            tick_su=""
    else:
        colorscale = None

    # colorscale = "asc"

    if colorscale == "asc":
        pass
    elif colorscale == "desc":
        colors.reverse()
    else:
        # colors = 4*["#1f77b4"]
        colors = 4 * ['rgba(31, 119, 180,0.01)']

    # disp = "perc"
    # disp = "raw"

    if disp == "perc":

        layout = go.Layout(
                showlegend=False,
                title=var_dict.get(tag).get("full_name"),
            xaxis=dict(
                tickvals= x,
                ticktext= [" "] + groups + [" "]
            ),
                yaxis=dict(
                       # autotick = False,
                       #  title=var_dict.get(tag).get("full_name"),
                       tick0= 0,
                       dtick= 25,
                       type=scale,
                       range= [0, 100],
                       tickformat='.3s',
                        ),
                yaxis2=dict(
                    # autotick=False,
                    title= "Percentiles",
                    tick0=0,
                    dtick=25,
                    type=scale,
                    range=[0, 100],
                    overlaying='y',
                    tickformat='.3s',
                    ),
        )

        fig = go.Figure(layout=layout)
        #adding background colors
        if True:
            fig.add_trace(go.Scatter(
                x=x, y=[25] * len(x),
                hoverinfo="none",
                mode='lines',
                line=dict(width=0.5, color=colors[0]),
                stackgroup='one', # define stack group
                fillcolor=colors[0]
            ))
            fig.add_trace(go.Scatter(
                x=x, y=[25] * len(x),
                hoverinfo="none",
                mode='lines',
                line=dict(width=0.5, color=colors[1]),
                stackgroup='one',
                fillcolor=colors[1]
                # opacity=0.3
            ))
            fig.add_trace(go.Scatter(
                x=x, y=[25] * len(x),
                hoverinfo="none",
                mode='lines',
                line=dict(width=0.5, color=colors[2]),
                stackgroup='one',
                fillcolor=colors[2]
                # opacity=0.3
            ))
            fig.add_trace(go.Scatter(
                x=x, y=[25] * len(x),
                hoverinfo="none",
                mode='lines',
                line=dict(width=0.5, color=colors[3]),
                stackgroup='one',
                fillcolor=colors[3]
                # opacity=0.3
            ))
        for i,g in enumerate(groups):

            samples_df = input_df[input_df["sample"].isin(groups_dict[g])]
            y_vals = samples_df[tag].values
            fig.add_trace(go.Box(
                x=[i+1]*len(y_vals),
                y=y_vals,
                yaxis="y2",
                name = g,
                # hoverinfo="none",
                # mode='lines',
                line=dict(width=2, color='rgb(31, 119, 180)'),
                # stackgroup='one',
                fillcolor='rgba(102,178,255,0.5)',
                # opacity=1
            ))

        div = plot(fig, show_link=False, auto_open=False, include_plotlyjs=False, output_type="div")
        return div

    elif disp == "raw":

        perc_df = pandas.read_csv(input_file, sep="\t",index_col=0)
        perc_df.value = perc_df.value.round(decimals=2)
        tick0 = perc_df.iloc[0]["value"]
        tick25 = perc_df.iloc[25]["value"]
        tick50 = perc_df.iloc[50]["value"]
        tick75 = perc_df.iloc[75]["value"]
        tick100 = perc_df.iloc[100]["value"]
        ticks = [tick0,tick25,tick50,tick75,tick100]

        if scale == "linear":
            ticks = tick_cleaner(ticks,0.03)
        #print(input_df["values"])
        layout = go.Layout(
                showlegend=False,
                title=var_dict.get(tag).get("full_name"),
            xaxis=dict(
                tickvals= x,
                ticktext= [" "] + groups + [" "]
            ),
                yaxis=dict(
                   # autotick = False,
                   #  autorange=False,
                   #  title=var_dict.get(tag).get("full_name"),
                   # tick0= ,
                    title=var_dict.get(tag).get("full_name"),
                    tickvals=ticks,
                    # ticktext=["p0","p25","p50","p75","p100"],
                    tickformat= '.3s',
                    type=scale,
                    ticksuffix=tick_su,
                    range=[tick0, tick100],
                   # range= [0, 100],
                    ),
                yaxis2=dict(
                    # autorange=False,
                    # autotick=False,
                    # title=var_dict.get(tag).get("full_name"),
                    # tick0=0,
                    anchor="x",
                    tickvals=ticks,
                    ticktext=[""]*len(ticks),
                    # tickformat=".2",
                    range=[tick0, tick100],
                    tickformat='.3s',
                    overlaying='y',
                    type=scale,
                    ticksuffix=tick_su,
                    ),
        )

        fig = go.Figure(layout=layout)
        #adding background colors
        if True:
            fig.add_trace(go.Scatter(
                x=x, y=[tick25]*len(x),
                hoverinfo="none",
                mode='lines',
                line=dict(width=0.5, color=colors[0]),
                stackgroup='one', # define stack group
                fillcolor=colors[0]
            ))
            fig.add_trace(go.Scatter(
                x=x, y=[tick50-tick25] * len(x),
                hoverinfo="none",
                mode='lines',
                line=dict(width=0.5, color=colors[1]),
                stackgroup='one',
                fillcolor=colors[1]
                # opacity=0.3
            ))
            fig.add_trace(go.Scatter(
                x=x, y=[tick75-tick50] * len(x),
                hoverinfo="none",
                mode='lines',
                line=dict(width=0.5, color=colors[2]),
                stackgroup='one',
                fillcolor=colors[2]
                # opacity=0.3
            ))
            fig.add_trace(go.Scatter(
                x=x, y=[tick100-tick75] * len(x),
                hoverinfo="none",
                mode='lines',
                line=dict(width=0.5, color=colors[3]),
                stackgroup='one',
                fillcolor=colors[3]
                # opacity=0.3
            ))
        for i,g in enumerate(groups):

            samples_df = input_df[input_df["sample"].isin(groups_dict[g])]
            y_vals = samples_df["values"].values
            print(y_vals)
            fig.add_trace(go.Box(
                x=[i+1]*len(y_vals),
                y=y_vals,
                yaxis="y2",
                name = g,
                # hoverinfo="none",
                # mode='lines',
                line=dict(width=2, color='rgb(31, 119, 180)'),
                # stackgroup='one',
                fillcolor='rgba(102,178,255,0.5)',
                # opacity=1
            ))

        div = plot(fig, show_link=False, auto_open=False, include_plotlyjs=False, output_type="div")
        return div


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


def plot_boxplots2(input_df=None,input_file=None, scale=None, tag=None):
    tick = ""
    tag_dict = var_dict.get(tag)
    if tag_dict:
        colorscale = tag_dict.get("color_scale")
        if tag_dict.get("is_percentage"):
            tick = "%"
    else:
        colorscale = None
    if colorscale == "asc":
        scale_list = ['rgb(164, 207, 99)'] * 26 + ['rgb(232, 213, 89)'] * 25 + ['rgb(251, 163,83)'] * 25 + [
            'rgb(221,90,78)'] * 25
    elif colorscale == "desc":
        scale_list = ['rgb(221,90,78)'] * 26 + ['rgb(251, 163,83)'] * 25 + ['rgb(232, 213, 89)'] * 25 + [
            'rgb(164, 207, 99)'] * 25
    else:
        scale_list = 101 * ["#1f77b4"]

    perc_df = pandas.read_csv(input_file, sep="\t")
    perc_df["bar_color"] = scale_list
    data = [go.Box(name="percentile",
                   x=[var_dict.get(tag).get("full_name")],
                   y=perc_df.value.values,
                   # marker=dict(color="blue"),
                   hovertemplate="%{x}p: %{y}",
                   showlegend=False
                   )]
    layout = go.Layout(
        # autosize=False,
        # width=500,
        # scene = dict(
        #     annotations = [annoation],
        title=var_dict.get(tag).get("full_name"),
        # annotations=annotation,

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
            title=var_dict.get(tag).get("full_name"),
            # type=scale,
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
    div = plot(fig, show_link=False, auto_open=False, include_plotlyjs=False, output_type="div",
               config={'editable': True})
    return div

def ajax_boxplots(request):

    folder = request.GET.get('id', None)
    comparison = request.GET.get('comp_set', None)
    query_folder = os.path.join(MEDIA_ROOT, folder, "query", "comparisons", comparison)
    variable = request.GET.get('variable', None)
    scale = request.GET.get('scale', None)
    disp = request.GET.get('disp_vals', None)

    group_file = os.path.join(MEDIA_ROOT, folder, "query", "comparisons", "sampleSheet.tsv")
    group_dict = make_group_dict(group_file)
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

    data["plot"] = plot_boxplots(perc_df, filepath, scale, variable, disp, group_dict)
    # data["plot"] = plot_boxplots()
    return JsonResponse(data)