
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Doctor
from .models import Patient, Doctor, PatientDoctorMapping


class HealthcareAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123!"
        )

        response = self.client.post(
            "/api/auth/login/",
            {
                "username": "testuser",
                "password": "TestPassword123!"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.data['access']}"
        )

    def test_patient_list_requires_authentication(self):
        self.client.credentials()

        response = self.client.get("/api/patients/")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_patient_list_with_authentication(self):
        response = self.client.get("/api/patients/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_create_patient_with_valid_data(self):
        response = self.client.post(
            "/api/patients/",
            {
                "name": "Test Patient",
                "age": 25,
                "gender": "Male",
                "phone": "9876543210",
                "address": "Delhi",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Test Patient")

    def test_create_patient_with_invalid_phone(self):
        response = self.client.post(
            "/api/patients/",
            {
                "name": "Invalid Phone Patient",
                "age": 25,
                "gender": "Male",
                "phone": "abc",
                "address": "Delhi",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone", response.data)


    def test_doctor_list(self):
        response = self.client.get("/api/doctors/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_doctor(self):
        response = self.client.post(
            "/api/doctors/",
            {
                "name": "Dr. Test Doctor",
                "specialization": "Cardiology",
                "email": "doctor.test@example.com",
                "phone": "9123456780",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Dr. Test Doctor")

    def test_create_patient_doctor_mapping(self):
        patient_response = self.client.post(
            "/api/patients/",
            {
                "name": "Mapping Test Patient",
                "age": 30,
                "gender": "Male",
                "phone": "9876543210",
                "address": "Delhi",
            },
            format="json",
        )

        self.assertEqual(
            patient_response.status_code,
            status.HTTP_201_CREATED,
        )

        doctor = self.client.post(
            "/api/doctors/",
            {
                "name": "Dr. Mapping Test",
                "specialization": "Neurology",
                "email": "mapping.doctor@example.com",
                "phone": "9123456781",
            },
            format="json",
        )

        self.assertEqual(doctor.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            "/api/mappings/",
            {
                "patient": patient_response.data["id"],
                "doctor": doctor.data["id"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_patient_doctor_mapping(self):
        from api.models import Patient, Doctor, PatientDoctorMapping

        patient = Patient.objects.create(
            name="Duplicate Test Patient",
            age=35,
            gender="Male",
            phone="9876543211",
            address="Delhi",
            created_by=self.user,
        )

        doctor = Doctor.objects.create(
            name="Dr. Duplicate Test",
            specialization="Cardiology",
            email="duplicate.doctor@example.com",
            phone="9123456782",
        )

        PatientDoctorMapping.objects.create(
            patient=patient,
            doctor=doctor,
        )

        response = self.client.post(
            "/api/mappings/",
            {
                "patient": patient.id,
                "doctor": doctor.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


    def test_create_doctor_with_valid_data(self):
        response = self.client.post(
            "/api/doctors/",
            {
                "name": "Dr. Test Doctor",
                "specialization": "Cardiology",
                "email": "doctor1@example.com",
                "phone": "9123456780",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            response.data["email"],
            "doctor1@example.com",
        )

    def test_create_doctor_with_invalid_email(self):
        response = self.client.post(
            "/api/doctors/",
            {
                "name": "Invalid Email Doctor",
                "specialization": "Cardiology",
                "email": "not-an-email",
                "phone": "9123456780",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("email", response.data)

    def test_create_doctor_with_duplicate_email(self):
        Doctor.objects.create(
            name="Existing Doctor",
            specialization="Cardiology",
            email="duplicate@example.com",
            phone="9123456780",
        )

        response = self.client.post(
            "/api/doctors/",
            {
                "name": "Another Doctor",
                "specialization": "Neurology",
                "email": "duplicate@example.com",
                "phone": "9876543210",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("email", response.data)
        
    
    def create_test_patient(self, name="Mapping Test Patient"):
        return Patient.objects.create(
            name=name,
            age=30,
            gender="Male",
            phone="9876543210",
            address="Delhi",
            created_by=self.user,
        )

    def create_test_doctor(self, email="mapping.doctor@example.com"):
        return Doctor.objects.create(
            name="Dr. Mapping Test",
            specialization="Cardiology",
            email=email,
            phone="9123456780",
        )

    def test_create_patient_doctor_mapping(self):
        patient = self.create_test_patient()
        doctor = self.create_test_doctor()

        response = self.client.post(
            "/api/mappings/",
            {"patient": patient.id, "doctor": doctor.id},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            PatientDoctorMapping.objects.filter(
                patient=patient, doctor=doctor
            ).count(),
            1,
        )

    def test_duplicate_patient_doctor_mapping_rejected(self):
        patient = self.create_test_patient()
        doctor = self.create_test_doctor()

        PatientDoctorMapping.objects.create(
            patient=patient, doctor=doctor
        )

        response = self.client.post(
            "/api/mappings/",
            {"patient": patient.id, "doctor": doctor.id},
            format="json",
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_mapping_with_invalid_patient_rejected(self):
        doctor = self.create_test_doctor()

        response = self.client.post(
            "/api/mappings/",
            {"patient": 999999, "doctor": doctor.id},
            format="json",
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertIn("patient", response.data)

    def test_mapping_with_invalid_doctor_rejected(self):
        patient = self.create_test_patient()

        response = self.client.post(
            "/api/mappings/",
            {"patient": patient.id, "doctor": 999999},
            format="json",
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertIn("doctor", response.data)

    def test_delete_patient_doctor_mapping(self):
        patient = self.create_test_patient()
        doctor = self.create_test_doctor()

        mapping = PatientDoctorMapping.objects.create(
            patient=patient, doctor=doctor
        )

        response = self.client.delete(
            f"/api/mappings/delete/{mapping.id}/"
        )

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(
            PatientDoctorMapping.objects.filter(
                id=mapping.id
            ).exists()
        )

    def test_patient_cannot_access_another_users_mapping(self):
        from django.contrib.auth.models import User

        other_user = User.objects.create_user(
            username="other_mapping_user",
            password="OtherPassword123!",
        )

        patient = Patient.objects.create(
            name="Other User Patient",
            age=40,
            gender="Female",
            phone="9876543211",
            address="Noida",
            created_by=other_user,
        )
        doctor = self.create_test_doctor()

        mapping = PatientDoctorMapping.objects.create(
            patient=patient, doctor=doctor
        )

        response = self.client.get("/api/mappings/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = (
            response.data
            if isinstance(response.data, list)
            else response.data.get("results", [])
        )

        self.assertNotIn(
            mapping.id, [item["id"] for item in results]
        )
    
