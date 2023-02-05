from .models import Package, Tracking


class Factory:

    def create_object(self, name):
        if "Package" == name:
            return Package()

        elif "Tracking" == name:
            return Tracking()
        else:
            raise Exception("Sorry, class not implemented")
