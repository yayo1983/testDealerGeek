from django import forms
from .models import Package, Tracking, Status
from datetime import datetime
from django.db import transaction
from django.db import IntegrityError
from .Factory import Factory


class PackageForm(forms.Form):

    def __init__(self):
        self.__factory__ = Factory()

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
            package = self.__factory__.create_object('Package')
            package.description = self.cleaned_data['description']
            package.size = self.cleaned_data['size']
            package.email_receiver = self.cleaned_data['email_receiver']
            package.status = 'I'
            package.save()

            tracking = self.__factory__.create_object('Tracking')
            tracking.address = self.cleaned_data['address_origin']
            tracking.date = datetime.now()
            tracking.package = package
            tracking.status = 'I'
            tracking.save()

            tracking = self.__factory__.create_object('Tracking')
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


class UpdateTrackingForm(forms.Form):
    def __init__(self):
        self.__factory__ = Factory()

    def choices(em):
        return [(e.name, e.value) for e in em]

    id = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=4, max_length=250, label='Identificador')
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                     min_length=4, max_length=250, label='Lugar del paquete')
    status = forms.ChoiceField(label='Estado', choices=choices(Status), widget=forms.Select(attrs={'class': 'form-control'}))

    @transaction.atomic()
    def save_update(self):
        try:
            package = Package.objects.get(pk=self.cleaned_data['id'])
            package.status = self.cleaned_data['status']
            package.save()
            if self.cleaned_data['status'] == 'I':
                return -1
            tracking = self.__factory__.create_object('Tracking')
            if self.cleaned_data['status'] == 'E':
                tracking = Tracking.objects.filter(package=package, status='E')
            else:
                tracking.address = self.cleaned_data['address']
                tracking.date = datetime.now()
                tracking.package = package
                tracking.status = self.cleaned_data['status']
            tracking.date = datetime.now()
            tracking.save()
            return package.id
        except IntegrityError:
            return False
        except Package.DoesNotExist:
            return False
