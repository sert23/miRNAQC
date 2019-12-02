from django.shortcuts import render
from django.views.generic import FormView, DetailView
from .tables import test_table
# Create your views here.

class testMulti(FormView):

    def get(self, request):
        context = {}
        t1,t2 = test_table()
        context["test_table"] = t1
        context["test_table2"] = t2

        # print("hey")
        # return render(self.request, 'test_table.html', context)
        return render(self.request, 'table.html', context)