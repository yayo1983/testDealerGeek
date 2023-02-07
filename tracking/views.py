
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from .abstract_factory_form import FactoryForm


def index(request):
    return render(request, 'index.html')


def create_package(request):
    factory = FactoryForm()
    if request.method == "POST":
        form = factory.create_package_form(request.POST)
        if form.is_valid():
            result = form.save_create()
            if result:
                return render(request, 'package_registered.html', {'ID': result})
        else:
            render(request, 'package_form.html', {'form': form})
    form = factory.create_package_form()
    return render(request, 'package_form.html', {'form': form})


def tracking_package(request):
    factory = FactoryForm()
    if request.method == "POST":
        form = factory.create_tracking_form(request.POST)
        if form.is_valid():
            result = form.search_packages()
            if result:
                context = {'package': result[0], 'tracking_package': result[1], 'Status': result[2], 'form': form}
                return render(request, 'tracking_package.html', context)
        return render(request, 'tracking_package.html', {'form': form})
    form = factory.create_tracking_form()
    return render(request, 'tracking_package.html', {'form': form})


def update_package(request):
    factory = FactoryForm()
    if request.method == "POST":
        form = factory.create_update_tracking_form(request.POST)
        if form.is_valid():
            package = form.save_update()
            if package:
                return render(request, 'package_updated.html', {'package': package})
        else:
            return render(request, 'package_update_form.html', {'form': form})
    form = factory.create_update_tracking_form()
    return render(request, 'package_update_form.html', {'package': {}, 'form': form})


@login_required
def report_package(request):
    factory = FactoryForm()
    if request.method == "POST":
        form = factory.create_report_tracking_form(request.POST)
        if form.is_valid():
            result = form.report_trackings()
            if result:
                context = {'trackings': result[0], 'Status': result[1], 'form': form, 'date': request.POST['date_report']}
                return render(request, 'package_report_form.html', context)
    form = factory.create_report_tracking_form()
    return render(request, 'package_report_form.html', {'form': form, 'trackings': []})


@login_required
def export_users_xls(request, dater):
    if request.method == "GET":
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="trackings.xls"'
        factory = FactoryForm()
        form = factory.create_report_tracking_form(request.POST)
        response = form.export_users_xls(response, dater)
        return response