from django.shortcuts import render, redirect
from .forms import PackageForm, TrackingForm, UpdateTrackingForm
from .models import Package, Tracking, Status
from .serializers import TrackingSerializers


def index(request):
    return render(request, 'index.html')


def create_package(request):
    if request.method == "POST":
        form = PackageForm(request.POST)
        if form.is_valid():
            result = form.save_create()
            if result:
                return render(request, 'package_registered.html', {'ID': result})
            return redirect('update-package')
    else:
        form = PackageForm()
    return render(request, 'package_form.html', {'form': form})


def tracking_package(request):
    try:
        form = TrackingForm(request.POST)
        if request.method == "POST":
            package = Package.objects.get(pk=request.POST["id"])
            if form.is_valid():
                trackings = Tracking.objects.filter(package=package)
                serializer_tracking = TrackingSerializers(trackings, many=True)
                data = form.put_status_e_to_end(serializer_tracking.data)
                for index, obj in enumerate(data):
                    if obj['status'] == 'E':
                        data.append(obj)
                        data.pop(index)
                return render(request, 'tracking_package.html',
                          {'package': package, 'tracking_package': data, 'Status': Status, 'form': form})
        return render(request, 'tracking_package.html', {'form': form})
    except Package.DoesNotExist:
        return render(request, 'tracking_package.html', {'package': {}, 'tracking_package': [], 'form': form })


def update_package(request):
    if request.method == "POST":
        form = UpdateTrackingForm(request.POST)
        if form.is_valid():
            result = form.save_update()
            if result:
                if result == -1:
                    return redirect('update-package', {'form': form})
                return render(request, 'package_updated.html', {'ID': result})
            return redirect('update-package', {'form': form})
    form = UpdateTrackingForm()
    return render(request, 'package_update_form.html', {'package': {}, 'tracking_package': [], 'form': form})