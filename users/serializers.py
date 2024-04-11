from rest_framework import serializers
from users.models import EmpID, User

class EmpIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpID
        fields = ('emp_id',)

class UserSerializer(serializers.ModelSerializer):
    emp_id = serializers.SerializerMethodField()

    def get_emp_id(self, obj):
        return obj.emp_id.emp_id if obj.emp_id else None

    class Meta:
        model = User
        fields = ('id', 'emp_id', 'firstName', 'lastName', 'email', 'role', 'mobileNumber')
