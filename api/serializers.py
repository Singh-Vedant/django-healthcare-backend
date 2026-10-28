import re
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Patient, Doctor, PatientDoctorMapping


 
class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)
    username = serializers.CharField(required=False, max_length=150)

    class Meta:
        model = User
        fields = ["id", "name", "username", "email", "password"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        name = validated_data.pop("name").strip()
        username = validated_data.pop("username", None)
        email = validated_data.get("email", "").strip().lower()

        if not name:
            raise serializers.ValidationError(
                {"name": "Name cannot be empty."}
            )

        if not username:
            username = email.split("@")[0]

        base_username = username
        counter = 1

        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        validated_data["email"] = email

        return User.objects.create_user(
            username=username,
            first_name=name,
            **validated_data,
        )


class PatientSerializer(serializers.ModelSerializer):

    def validate_phone(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise serializers.ValidationError(
                "Phone number must contain exactly 10 digits."
            )
        return value

    class Meta:
        model = Patient
        fields = "__all__"
        read_only_fields = ["created_by", "created_at"]


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = "__all__"
