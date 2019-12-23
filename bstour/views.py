from django.shortcuts import render
from django.views.generic import FormView, DetailView
from results.tables import basic_table,seqYield_table, tables_yield, cols_dict, seq_qual_tab, library_tab
from miRQC.settings import MEDIA_ROOT, MEDIA_URL, SUB_SITE, MEDIA_URL, MAIN_SITE
from newJob.views import new_rand_folder
from newJob.forms import SpeciesForm
from newJob.models import Species
import os
import pandas
import plotly.graph_objs as go
from plotly.offline import plot
import numpy as np
from django.http import JsonResponse
from django.urls import reverse_lazy

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
        #get folder from path
        folder = "tour"
        context["jobID"] = folder
        context["result_url"] = reverse_lazy("check_status") + "/" + folder
        context["absolute_url"] = MAIN_SITE
        query_folder = os.path.join(MEDIA_ROOT,folder,"query")
        val_file = os.path.join(query_folder,"value_full.tsv")
        perc_file = os.path.join(query_folder,"percentil_full.tsv")
        context["vals_link"] = val_file.replace(MEDIA_ROOT,MEDIA_URL)
        context["perc_link"] = perc_file.replace(MEDIA_ROOT,MEDIA_URL)

        #read files into dfs
        val_df = pandas.read_csv(val_file, sep="\t")
        perc_df = pandas.read_csv(perc_file, sep="\t")
        columns = cols_dict(perc_df)
        # context["basic_hm"] = plot_heatmap(perc_df)

        #basic statistics
        basic_tab,basic_perc = basic_table(val_df, perc_df, columns)
        context["basic_table"] = basic_tab
        context["basic_perc"] = basic_perc

        #sequencing yield
        seqYield_tab, seqYield_perc = tables_yield(val_df, perc_df, columns)
        context["seqYield_table"] = seqYield_tab
        context["seqYield_perc"] = seqYield_perc

        #sequencing quality
        seqQual_tab, seqQual_perc = seq_qual_tab(val_df, perc_df, columns)
        context["seqQual_table"] = seqQual_tab
        context["seqQual_perc"] = seqQual_perc

        # library quality
        library_table, library_perc = library_tab(val_df, perc_df, columns)
        context["library_table"] = library_table
        context["library_perc"] = library_perc

        return render(self.request, 'tour/results.html', context)
