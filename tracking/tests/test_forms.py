# from unittest import TestCase
from django.http import HttpRequest
from django.test import TestCase
from tracking.factoryf import FactoryForm
from tracking.models import Package
from tracking.forms import PackageForm, TrackingForm


class PackageFormTest(TestCase):
    def test_created_package_traking(self):
        request = HttpRequest()
        request.POST = {
            'description': 'description_test',
            'size': 'size_tesst',
            'email_receiver': 'emali@test.test',
            'address_origin': "tulum test",
            'address_destination': "cdmx test",
        }
        data = {
            'description': 'description_test',
            'size': 'size_tesst',
            'email_receiver': 'emali@test.test',
            'address_origin': "tulum test",
            'address_destination': "cdmx test",
        }

        factory = FactoryForm()
        # form = factory.create_form('PackageForm', data)
        form = PackageForm(data=request.POST)
        form.save_create()
        self.assertEqual(Package.objects.filter(email_receiver='emali@test.test').count(), 1)

    def test_check_value_label(self):
        form = PackageForm()
        self.assertTrue(form.fields['description'].label == 'Descripción' and form.fields['size'].label == 'Tamaño' and
                        form.fields['address_origin'].label == 'Dirección origen' and form.fields['address_destination'].label == 'Dirección de destino' and
                        form.fields['email_receiver'].label == 'Correo')

    def test_check_valid_package_form(self):
        email = 'yazanenator@gmail.com'
        description = 'some'
        size = 9
        address_origin = 'some address'
        address_destination = 'other address'
        form_data = {'description': description, 'size': size, 'address_origin': address_origin, 'address_destination': address_destination, 'email_receiver': email}
        form = PackageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_check_false_value(self):
        email = 'yazanenator.com'
        description = ''
        size = 9
        address_origin = ''
        address_destination = ''
        form_data = {'description': description, 'size': size, 'address_origin': address_origin, 'address_destination': address_destination, 'email_receiver': email}
        form = PackageForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_render_form(self):
        form = PackageForm()
        self.assertIn("description", form.fields)
        self.assertIn("size", form.fields)
        self.assertIn("address_origin", form.fields)
        self.assertIn("address_destination", form.fields)
        self.assertIn("email_receiver", form.fields)




class TrackingFormTest(TestCase):
    def test_render_form(self):
        factory = FactoryForm()
        form = factory.create_form('TrackingForm')
        self.assertInHTML('<input type="text" name="id" class="form-control" maxlength="250" minlength="4" required="" id="id_id">', str(form))

    @classmethod
    def setUpTestData(cls):
        pass

    def test_form_value_tracking_packages(self):
        request = HttpRequest()
        request.POST = {"id": "596f04388bd84f1d9ba4d0a32f9bd06d"}
        factory = FactoryForm()
        form = factory.create_form('TrackingForm', request.POST)
        self.assertTrue(form.is_valid())
