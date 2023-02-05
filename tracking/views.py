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
            return redirect('update-package')
    else:
        form = factory.create_form('PackageForm')
    return render(request, 'package_form.html', {'form': form})


def tracking_package(request):
    factory = FactoryForm()
    form = factory.create_form('TrackingForm', request.POST)
    if request.method == "POST":
        if form.is_valid():
            result = form.update(request.POST["id"])
            if result != -1 :
                return render(request, 'tracking_package.html',
                      {'package': result[1], 'tracking_package': result[0], 'Status': result[2], 'form': form})
    form = factory.create_form('TrackingForm')
    return render(request, 'tracking_package.html', {'package': {}, 'tracking_package': [], 'form': form })


def update_package(request):
    factory = FactoryForm()
    if request.method == "POST":
        form = factory.create_form('UpdateTrackingForm', request.POST)
        if form.is_valid():
            result = form.save_update()
            if result:
                if result == -1:
                    return redirect('update-package', {'form': form})
                return render(request, 'package_updated.html', {'package': result})
            return redirect('update-package', {'form': form})
    form = factory.create_form('UpdateTrackingForm')
    return render(request, 'package_update_form.html', {'package': {}, 'tracking_package': [], 'form': form})


@login_required
def report_package(request):
    factory = FactoryForm()
    if request.method == "POST":
        form = factory.create_form('ReportPackageForm', request.POST)
        if form.is_valid():
            result = form.save_update()
            if result:
                if result == -1:
                    return redirect('package_report_form', {'form': form})
                return render(request, 'package_report_form.html', {'package': result})
            return redirect('package_report_form', {'form': form})
    form = factory.create_form('UpdateTrackingForm')
    return render(request, 'package_report_form.html', {'package': {}, 'tracking_package': [], 'form': form})