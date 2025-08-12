# api/serializers.py
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    role = serializers.ChoiceField(choices=['customer', 'doctor', 'pharmacy'])
    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(allow_blank=True, required=False)
    address = serializers.CharField(allow_blank=True, required=False)
    token = serializers.CharField(read_only=True)

class PharmacySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    address = serializers.CharField(allow_blank=True, required=False)
    phone = serializers.CharField(allow_blank=True, required=False)
    lat = serializers.FloatField(required=False)
    lng = serializers.FloatField(required=False)

class MedicineSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    brand = serializers.CharField(allow_blank=True, required=False)
    description = serializers.CharField(allow_blank=True, required=False)
    price = serializers.FloatField(required=False)
    stock = serializers.IntegerField(default=0)
    pharmacy_id = serializers.IntegerField()

class PrescriptionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    doctor_id = serializers.IntegerField(allow_null=True, required=False)
    pharmacy_id = serializers.IntegerField(allow_null=True, required=False)
    medicines = serializers.ListField(child=serializers.DictField(), required=False)
    uploaded_image_url = serializers.CharField(allow_blank=True, required=False)
    ocr_text = serializers.CharField(allow_blank=True, required=False)

class ReminderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    medicine_name = serializers.CharField()
    time = serializers.DateTimeField()
    repeat = serializers.CharField(allow_blank=True, required=False)
