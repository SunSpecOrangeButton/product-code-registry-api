import rest_framework_filters as filters
from .models import *
from django_filters import rest_framework as df_filters
from rest_framework import filters as rf_filters


class ManufacturerFilter(filters.FilterSet):
    class Meta:
        model = Manufacturer
        fields = {
            'ManufacturerCode': '__all__',
            'ManufacturerName': '__all__',
            'LegalEntityIdentifier': '__all__',
        }


class ModuleFilter(filters.FilterSet):
    class Meta:
        model = Module
        fields = {
            'ProductCode': '__all__',
            'Description': '__all__',
            'ManufacturerName': '__all__',
            'ManufacturerProductID': '__all__',
            'ManufacturerCode': '__all__',
            'ProductType': '__all__',
            'ModuleTechnology': '__all__',
            'ModuleNameplateCapacity': '__all__',
            'FrameColor': '__all__',
            'BacksheetColor': '__all__',
        }


class InverterFilter(filters.FilterSet):
    class Meta:
        model = Inverter
        fields = {
            'ProductCode': '__all__',
            'Description': '__all__',
            'ManufacturerName': '__all__',
            'ManufacturerProductID': '__all__',
            'ManufacturerCode': '__all__',
            'ProductType': '__all__',
            'Power': '__all__',
            'Phases': '__all__',
            'Transformerless': '__all__',
        }


class BatteryFilter(filters.FilterSet):
    class Meta:
        model = Battery
        fields = {
            'ProductCode': '__all__',
            'Description': '__all__',
            'ManufacturerName': '__all__',
            'ManufacturerProductID': '__all__',
            'ManufacturerCode': '__all__',
            'ProductType': '__all__',
        }


class CharInFilter(df_filters.BaseInFilter, df_filters.CharFilter):
    pass


class ProductFilter(filters.FilterSet, rf_filters.SearchFilter):
    # OR filtering
    # ProductCode__in = CharInFilter(field_name='ProductType', lookup_expr='in')
    # ManufacturerName__in = CharInFilter(field_name='ProductRegion', lookup_expr='in')
    # ManufacturerProductID__in = CharInFilter(field_name='ProductCertificationType', lookup_expr='in')
    # ManufacturerCode__in = CharInFilter(field_name='ProductType', lookup_expr='in')
    ProductType__in = CharInFilter(field_name='ProductType', lookup_expr='in')

    class Meta:
        model = Product
        fields = {
            'ProductCode': '__all__',
            'ManufacturerName': '__all__',
            'ManufacturerProductID': '__all__',
            'ManufacturerCode': '__all__',
            'ProductType': '__all__',
        }


