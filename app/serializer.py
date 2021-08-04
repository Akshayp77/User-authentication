from rest_framework import serializers


class EmpS(serializers.Serializer):
    name=serializers.CharField(max_length=50)
    e_id=serializers.IntegerField()
    salary=serializers.IntegerField()