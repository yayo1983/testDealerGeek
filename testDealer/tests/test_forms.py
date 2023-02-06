from unittest import TestCase

from django.test import TestCase

from tracking.forms import PackageForm


class PackageFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form = PackageForm()
        self.assertTrue(form.fields['description'].label == 'Descripción' or form.fields['size'].label == 'Tamaño')

    def test_renew_form_date_in_past(self):
        email = 'yazanenator@gmail.com'
        form_data = {'email_receiver': email}
        form = PackageForm(data=form_data)
        self.assertFalse(form.is_valid())


class Test(TestCase):
    pass


class Test(TestCase):
    def test_package_form(self):
        self.fail()

    def test_tracking_form(self):
        self.fail()

    def test_update_tracking_form(self):
        self.fail()

    def test_report_package_form(self):
        self.fail()
