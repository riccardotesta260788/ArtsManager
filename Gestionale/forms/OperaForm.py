# import form class from django
from django import forms

# import GeeksModel from models.py
from Gestionale.models import Opera


# create a ModelForm
class OperaForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Opera
        fields = "__all__"
