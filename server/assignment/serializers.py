from .models import Assignment
from rest_framework import serializers
from django.utils import timezone



# ! User Registration Serailizer 
class AssignmentSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields=['id','title','description','submission_date']

    def validate_submission_date(self,value):
        if not self.instance and value < timezone.now():
            raise serializers.ValidationError("Cannot create assignment in the past date")
        if self.instance and value < self.instance.created_at:
            raise serializers.ValidationError("Cannot update assignment for the past date")
        return value