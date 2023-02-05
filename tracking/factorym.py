from .models import Package, Tracking


class FactoryModel:

    def create_model(self, name):
        if "Package" == name:
            return Package()

        elif "Tracking" == name:
            return Tracking()
        else:
            raise Exception("Sorry, class not implemented")
