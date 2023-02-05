from .forms import PackageForm, TrackingForm, UpdateTrackingForm


class FactoryForm:

    def create_form(self, name, parameter=''):
        if "PackageForm" == name:
            if parameter == '':
                return PackageForm()
            return PackageForm(parameter)

        elif "TrackingForm" == name:
            if parameter == '':
                return TrackingForm()
            return TrackingForm(parameter)

        elif "UpdateTrackingForm" == name:
            if parameter == '':
                return UpdateTrackingForm()
            return UpdateTrackingForm(parameter)

        else:
            raise Exception("Sorry, class not implemented")
