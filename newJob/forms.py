from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Field


class FileForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     if kwargs.get("request_path"):
    #         self.request_path = kwargs.pop("request_path", None)
    #     super(PhotoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UploadFile
        fields = ('file', )



class CategoriesField(forms.ModelMultipleChoiceField):
    def __init__(self, queryset, **kwargs):
        try:
            queryset = queryset()
            super(CategoriesField, self).__init__(queryset, **kwargs)
            self.queryset = queryset.select_related()
            self.to_field_name=None

            group = None
            list = []
            self.choices = []

            for category in queryset:
                if not group:
                    group = category.sp_class

                if group != category.sp_class:
                    self.choices.append((group, list))
                    group = category.sp_class
                    list = [(category.id, str(category))]
                else:
                    #list.append((category.id, str(category)))
                    list.append((str(category.id)+":"+category.scientific, str(category)))
                    #list.append((str(category.id)+""+category.scientific, str(category)))
            try:
                self.choices.append((group, list))
            except:
                pass

        except:
            pass

    def clean(self, value):
        if value:
            if isinstance(value[0], list):
                value = value[0]
        value = [v for v in value if v != '']
        return super(CategoriesField, self).clean(value)

def m():

    q1 = Species.objects.all().filter(sp_class__in=['plant','animal', 'fungi' ])

    return q1.order_by('sp_class', 'specie')

class SpeciesForm(forms.Form):
    species = CategoriesField(queryset=m, required=False, label="Species")
    input_hidden = forms.CharField(label='', required=False, widget=forms.HiddenInput, max_length=2500)
    species_hidden = forms.CharField(label='', required=False, widget=forms.HiddenInput, max_length=2500)

    def __init__(self, *args, **kwargs):
        self.folder = kwargs.pop('dest_folder', None)
        super(SpeciesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            # Field('species'),
            Field('species_hidden', name='species_hidden'),
            Field('input_hidden', name='input_hidden'))
