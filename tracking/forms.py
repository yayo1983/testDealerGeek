from django import forms
from .models import Package, Tracking, Status
from django.db import transaction
from django.db import IntegrityError
from .abstract_factory_model import FactoryModel
from .serializers import TrackingSerializers
from .utils import send_user_mail, put_status_e_to_end, export_users_xls, choices
from datetime import datetime


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
            package = factory.create_package_model
            package.description = self.cleaned_data['description'].strip()
            package.size = self.cleaned_data['size']
            package.email_receiver = self.cleaned_data['email_receiver'].strip()
            package.status = 'I'
            package.save()

            tracking = factory.create_tracking_model()
            tracking.address = self.cleaned_data['address_origin'].strip()
            tracking.date = datetime.now()
            tracking.package = package
            tracking.status = 'I'
            tracking.save()

            tracking = factory.create_tracking_model()
            tracking.address = self.cleaned_data['address_destination'].strip()
            tracking.package = package
            tracking.status = 'E'
            tracking.save()
            return package.id
        except IntegrityError:
            return False


class TrackingForm(forms.Form):
    id = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=4, max_length=250, label='Identificador')

    def clean(self):
        super(TrackingForm, self).clean()
        try:
            Package.objects.get(pk=self.cleaned_data['id'])
        except Package.DoesNotExist:
            raise forms.ValidationError({'id': ["No es un válido indentificador",]} )
        return self.cleaned_data

    def search_packages(self):
        try:
            package = Package.objects.get(pk=self.cleaned_data['id'])
            trackings = Tracking.objects.filter(package=package)
            serializer_tracking = TrackingSerializers(trackings, many=True)
            data = put_status_e_to_end(serializer_tracking.data)
            return [package, data, Status]
        except Package.DoesNotExist:
            return False


class UpdateTrackingForm(forms.Form):

    id = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=4, max_length=250, label='Identificador',
                         error_messages={'required': 'El identificador es requerido'})
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                     min_length=4, max_length=250, label='Lugar del paquete')
    status = forms.ChoiceField(label='Estado', choices=choices(Status), widget=forms.Select(attrs={'class': 'form-control'}))

    def clean(self):
        super(UpdateTrackingForm, self).clean()
        try:
            status = self.cleaned_data['status']
            package = Package.objects.get(pk=self.cleaned_data['id'])
            if status == 'I':
                raise forms.ValidationError("El paquete ya no debe volver a tener el estado Iniciado" )
            if package.status == 'E' and status != 'A':
                raise forms.ValidationError("Solo se puede cambiar para el estado Aceptado cuando el paquete tiene el estado de Entregado" )
        except Package.DoesNotExist:
            raise forms.ValidationError("No es un válido indentificador")
        return self.cleaned_data

    @transaction.atomic()
    def save_update(self):
        try:
            package = Package.objects.get(pk=self.cleaned_data['id'])
            package.status = self.cleaned_data['status']
            package.save()
            factory = FactoryModel()
            tracking = factory.create_tracking_model()
            if self.cleaned_data['status'] is 'E':
                tracking = Tracking.objects.filter(package=package).filter(status='E').first()
                send_user_mail(package.email_receiver, package.id)
            else:
                tracking.address = self.cleaned_data['address']
                tracking.date = datetime.now()
                tracking.package = package
                tracking.status = self.cleaned_data['status']
            tracking.date = datetime.now()
            tracking.save()
        except IntegrityError:
            raise forms.ValidationError("Error, contacte al admnistrador")
        return package


class ReportPackageForm(forms.Form):
    date_report = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='Fecha para reportar')

    def clean(self):
        super(ReportPackageForm, self).clean()
        date_report = self.cleaned_data['date_report']

        if date_report == "":
            self._errors['date_report'] = self.error_class(['La fecha para reportar no puede ser vacío'])

        return self.cleaned_data

    def report_trackings(self):
        try:
            trackings = Tracking.objects.filter(date__date=self.cleaned_data['date_report'])
            serializer_tracking = TrackingSerializers(trackings, many=True)
            return [serializer_tracking.data, Status]
        except:
            return False

    def export_users_xls(self, response, date):
        columns = ['ID de rastreo ', 'Estado del rastreo', 'Fecha de rastreo', 'Ubicación']
        rows = Tracking.objects.filter(date__date=date).values_list('id', 'status', 'date', 'address')
        return export_users_xls(response, columns, rows, nameSheet='Package-Tracking')