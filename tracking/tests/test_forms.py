from unittest import TestCase

from django.test import TestCase

from tracking.forms import PackageForm, TrackingForm


class PackageFormTest(TestCase):
    def test_check_value_label(self):
        form = PackageForm()
        self.assertTrue(form.fields['description'].label == 'Descripción' and form.fields['size'].label == 'Tamaño' and
                        form.fields['address_origin'].label == 'Dirección origen' and form.fields['address_destination'].label == 'Dirección de destino' and
                        form.fields['email_receiver'].label == 'Correo')

    def test_check_true_value(self):
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
        form = TrackingForm()
        self.assertInHTML('<input type="text" name="id" class="form-control" maxlength="250" minlength="4" required="" id="id_id">', str(form))