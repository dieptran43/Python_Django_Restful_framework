from django.urls import path,re_path
from restApiCreation.views import GetCircuits,GetCircuit
from . import views
urlpatterns=[
        re_path("^$", views.csvFileUplaod, name="csvFileUplaod"),
        re_path("circuits/(?P<name>[0-9a-zA-Z_\s]*/$)", GetCircuits.as_view(), name="circuits"),
        re_path("circuit/(?P<circuit>[0-9]{2}\.[A-Z]\d[A-Z]{2}\.[0-9]{4}\.[A-Z]{4}/$)", GetCircuit.as_view(), name="circuit"),
       
]
