from django.shortcuts import render, redirect
from .factoryf import FactoryForm
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')


def create_package(request):
    factory = FactoryForm()
    if request.method == "POST":
        form = factory.create_form('PackageForm', request.POST)
        if form.is_valid():
            result = form.save_create()
            if result:
                return render(request, 'package_registered.html', {'ID': result})
        else:
            render(request, 'package_form.html', {'form': form})
    form = factory.create_form('PackageForm')
    return render(request, 'package_form.html', {'form': form})


def tracking_package(request):
    factory = FactoryForm()
    if request.method == "POST":
        form = factory.create_form('TrackingForm', request.POST)
        if form.is_valid():
            result = form.search_packages()
            if result:
                return render(request, 'tracking_package.html',
                      {'package': result[0], 'tracking_package': result[1], 'Status': result[2], 'form': form})
    form = factory.create_form('TrackingForm')
    return render(request, 'tracking_package.html', {'package': {}, 'tracking_package': [], 'form': form })


def update_package(request):
    factory = FactoryForm()
    if request.method == "POST":
        form = factory.create_form('UpdateTrackingForm', request.POST)
        if form.is_valid():
            result = form.save_update()
            if result:
                if result != -1:
                    return render(request, 'package_updated.html', {'package': result})
    form = factory.create_form('UpdateTrackingForm')
    return render(request, 'package_update_form.html', {'package': {}, 'tracking_package': [], 'form': form})


@login_required
def report_package(request):
    factory = FactoryForm()
    if request.method == "POST":
        form = factory.create_form('ReportPackageForm', request.POST)
        if form.is_valid():
            trackings = form.report_traquings(request.POST["date"].strip())
            if trackings:
                return render(request, 'package_report_form.html', {'trackings': trackings, 'form': form})
    form = factory.create_form('ReportPackageForm')
    return render(request, 'package_report_form.html', {'form': form, 'trackings': []})