from django.shortcuts import render
from Gestionale.forms import OperaForm

template_folder = "form"


def insert_opera(request):
    context = {}

    # create object of form
    form = OperaForm(request.POST or None, request.FILES or None)

    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        form.save()

    context['form'] = form
    return render(request, '/'.join([template_folder, "opere.html"]), context)
