from django import forms
from .models import Package, Tracking, Status
from datetime import datetime
from django.db import transaction
from django.db import IntegrityError
from .factorym import FactoryModel
from .serializers import TrackingSerializers
from .sendemail import send_user_mail
from django.shortcuts import get_object_or_404


class PackageForm(forms.Form):

    description = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=4, max_length=250, label='Descripción')
    size = forms.FloatField(required=True, max_value=100000, min_value=0,
                     widget=forms.NumberInput(attrs={'id': 'form_homework', 'class': 'form-control' }), label='Tamaño')
    address_origin = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=1, max_length=250, label='Dirección origen')
    address_destination = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                     min_length=4, max_length=250, label='Dirección de destino')
    email_receiver = forms.EmailField(required=True, min_length=4, max_length=250, label='Correo', widget=forms.TextInput(attrs={'class': 'form-control'}))

    @transaction.atomic()
    def save_create(self):
        try:
            factory = FactoryModel()
            package = factory.create_model('Package')
            package.description = self.cleaned_data['description']
            package.size = self.cleaned_data['size']
            package.email_receiver = self.cleaned_data['email_receiver']
            package.status = 'I'
            package.save()

            tracking = factory.create_model('Tracking')
            tracking.address = self.cleaned_data['address_origin']
            tracking.date = datetime.now()
            tracking.package = package
            tracking.status = 'I'
            tracking.save()

            tracking = factory.create_model('Tracking')
            tracking.address = self.cleaned_data['address_destination']
            tracking.package = package
            tracking.status = 'E'
            tracking.save()
            return package.id
        except IntegrityError:
            return False


class TrackingForm(forms.Form):
    id = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=4, max_length=250, label='Identificador')

    def put_status_e_to_end(self, data):
        for index, obj in enumerate(data):
            if obj['status'] == 'E':
                data.append(obj)
                data.pop(index)
        return data

    def update(self, id):
        try:
            package = get_object_or_404(Package, pk=id)
            trackings = Tracking.objects.filter(package=package)
            serializer_tracking = TrackingSerializers(trackings, many=True)
            data = self.put_status_e_to_end(serializer_tracking.data)
            return [data, package, Status]
        except:
            return -1


class UpdateTrackingForm(forms.Form):

    def choices(em):
        return [(e.name, e.value) for e in em]

    id = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=4, max_length=250, label='Identificador')
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                     min_length=4, max_length=250, label='Lugar del paquete')
    status = forms.ChoiceField(label='Estado', choices=choices(Status), widget=forms.Select(attrs={'class': 'form-control'}))

    @transaction.atomic()
    def save_update(self):
        try:
            package = get_object_or_404(Package, pk=self.cleaned_data['id'])
            package.status = self.cleaned_data['status']
            package.save()
            if self.cleaned_data['status'] == 'I':
                return -1
            factory = FactoryModel()
            tracking = factory.create_model('Tracking')
            if self.cleaned_data['status'] == 'E':
                tracking = Tracking.objects.filter(package=package, status='E')
                send_user_mail(package.email_receiver, package.id)
            else:
                tracking.address = self.cleaned_data['address']
                tracking.date = datetime.now()
                tracking.package = package
                tracking.status = self.cleaned_data['status']
            tracking.date = datetime.now()
            tracking.save()
            return package
        except IntegrityError:
            return False
        except Package.DoesNotExist:
            return False


class ReportPackageForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='Fecha para reportar')

    def report_traquings(self):
        try:
            trackings = Tracking.objects.filter(date=self.cleaned_data['date'])
            serializer_tracking = TrackingSerializers(trackings, many=True)
            return serializer_tracking.data
        except:
            return False