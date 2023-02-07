from abc import ABC, abstractmethod
from .models import Package, Tracking


class AbstractFactoryModel(ABC):

    @abstractmethod
    def create_package_model(self):
        pass

    @abstractmethod
    def create_tracking_model(self):
        pass


class FactoryModel(AbstractFactoryModel):

    def create_package_model(self):
        return Package()

    def create_tracking_model(self):
        return Tracking()