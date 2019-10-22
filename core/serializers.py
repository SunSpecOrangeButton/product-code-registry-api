from rest_framework import serializers
from .models import *


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'
        

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'
        

class InverterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inverter
        fields = '__all__'
        

class BatterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Battery
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
