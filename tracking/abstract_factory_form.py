from abc import ABC, abstractmethod
from .forms import PackageForm, TrackingForm, UpdateTrackingForm, ReportPackageForm


class AbstractFactoryForm(ABC):

    @abstractmethod
    def create_package_form(self, parameter=''):
        pass

    @abstractmethod
    def create_tracking_form(self):
        pass

    @abstractmethod
    def create_update_tracking_form(self):
        pass

    @abstractmethod
    def create_report_tracking_form(self):
        pass


class FactoryForm(AbstractFactoryForm):

    def create_package_form(self, parameter=''):
        if parameter == '':
            return PackageForm()
        return PackageForm(parameter)

    def create_tracking_form(self, parameter=''):
        if parameter == '':
            return TrackingForm()
        return TrackingForm(parameter)

    def create_update_tracking_form(self, parameter=''):
        if parameter == '':
            return UpdateTrackingForm()
        return UpdateTrackingForm(parameter)

    def create_report_tracking_form(self, parameter=''):
        if parameter == '':
            return ReportPackageForm()
        return ReportPackageForm(parameter)