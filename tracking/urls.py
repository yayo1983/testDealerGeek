from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('package/create', views.create_package, name='create-package'),
    path('tracking', views.tracking_package, name='tracking-package'),
    path('package/update', views.update_package, name='update-package'),
    path('package/report', views.report_package, name='report-package'),
    path('export_excel/<str:dater>', views.export_users_xls, name='export_excel'),
]
