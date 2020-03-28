from django.shortcuts import render
from django.views.generic import FormView, DetailView
from results.tables import basic_table, tables_yield, cols_dict, seq_qual_tab, library_tab, tables_complex, contamination_tab, length_tab, par_table
from miRQC.settings import MEDIA_ROOT, MEDIA_URL, SUB_SITE, MEDIA_URL, MAIN_SITE
from newJob.views import new_rand_folder
from results.views import parse_perc_files
from newJob.forms import SpeciesForm
from newJob.models import Species
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


class tourStart(FormView):

    def get(self, request):
        # print(request.path[-1])
    # def get(self, request,**kwargs):
        context = {}
        jobID = "test"
        context["jobID"] = jobID
        context["request_path"] = os.path.join(SUB_SITE, "upload",jobID)
        context["submit_path"] = os.path.join("",jobID)
        context["form"] = SpeciesForm
        # species = list(Species.objects.all().filter(sp_class__in=['plant','animal', 'fungi' ]).values_list("scientific",flat=True))
        species = list(Species.objects.all().filter(sp_class__in=['plant','animal' ]).values_list("scientific",flat=True))
        assemblies = list(Species.objects.all().filter(sp_class__in=['plant','animal' ]).values_list("db_ver",flat=True))
        commons = list(Species.objects.all().filter(sp_class__in=['plant','animal']).values_list("specie",flat=True))
        shorts = list(Species.objects.all().filter(sp_class__in=['plant','animal']).values_list("shortName",flat=True))
        species_dict = dict(zip(species, assemblies))
        commons_list = list(zip(species,assemblies,shorts, commons))

        commons_list.sort()
        context["species_list"] = species
        context["species_dict"] = species_dict
        context["commons_list"] = commons_list

        # print(species_dict)
        # return render(self.request, 'multiupload.html', {'file_list': onlyfiles, "request_path":path, "form": MultiURLForm })
        return render(self.request, 'tour/index.html', context)


class tourResuls(FormView):

    def get(self, request):

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
        context["path_to_sample_results"] = SUB_SITE + "/result/T227DTB9FS2ZBU9"
        context["path_to_start"] = SUB_SITE
        return render(self.request, 'tour/results.html', context)
