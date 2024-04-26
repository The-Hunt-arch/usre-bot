from rest_framework import serializers
from core.models import JobApplication  # Replace 'yourapp' with the actual name of your app

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'
