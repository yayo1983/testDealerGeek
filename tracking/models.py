from django.db import models
from enum import Enum
import uuid


def for_django(cls):
    cls.do_not_call_in_templates = True
    return cls


@for_django
class Status(Enum):
    A = "Aceptado"
    I = "Iniciado"
    T = "En tránsito"
    E = "Entregado"

    def __str__(self):
        return self.name


class Package(models.Model):
    description = models.CharField(max_length=250, null=False, blank=True, verbose_name="Descripción")
    size = models.FloatField(null=False, blank=True, verbose_name="Tamaño")
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="Identificador", primary_key=True)
    status = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in Status], verbose_name="Estatus", null=True, default='I')
    email_receiver = models.EmailField(max_length=254, verbose_name="Correo", null=False, default='' )

    class Meta:
        db_table = "package"

    def __str__(self):
        return self.id.uuid1()


class Tracking(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha", null=False)
    address = models.CharField(max_length=250, null=False, blank=True, verbose_name="Dirección")
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="package", null=True, verbose_name="paquete")
    status = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in Status], verbose_name="Estatus",
                              null=True, default='I')

    class Meta:
        db_table = "tracking"

    def __str__(self):
        return self.address

    @property
    def status_package(self):
        return self.package.status

    @property
    def id_package(self):
        return str(self.package.id.uuid1())

    @classmethod
    def create(cls, date, address, package, status):
        tracking = cls(date, address, package, status)
        return tracking