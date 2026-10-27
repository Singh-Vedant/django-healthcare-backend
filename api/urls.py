
from django.urls import path
from .views import (
    RegisterView, LoginView,
    PatientListCreateView, PatientDetailView,
    DoctorListCreateView, DoctorDetailView,
    MappingListCreateView, PatientMappingView, MappingDeleteView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),

    path("patients/", PatientListCreateView.as_view(), name="patients"),
    path("patients/<int:pk>/", PatientDetailView.as_view(), name="patient-detail"),

    path("doctors/", DoctorListCreateView.as_view(), name="doctors"),
    path("doctors/<int:pk>/", DoctorDetailView.as_view(), name="doctor-detail"),

    path("mappings/", MappingListCreateView.as_view(), name="mappings"),
    path("mappings/<int:patient_id>/", PatientMappingView.as_view(), name="patient-mappings"),
    path("mappings/delete/<int:pk>/", MappingDeleteView.as_view(), name="mapping-delete"),
]
