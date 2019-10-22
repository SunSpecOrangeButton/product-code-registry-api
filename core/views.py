from .serializers import *
from .models import *
from rest_framework import generics, permissions
from .permissions import *
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from .filters import *
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.exceptions import ParseError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import json
from .utils import excelToDictGenericProduct


@ensure_csrf_cookie
@api_view(['GET'])
def login_view(request):
    email_address = request.GET.get('email_address', '')
    password = request.GET.get('password', '')
    user = authenticate(email_address=email_address, password=password)

    if user is not None:
        last_login = user.last_login
        if user.is_active:
            login(request, user)

            return Response(
                {
                    'status': 'success',
                    'id': user.identifier,
                    'email_address': user.email_address,
                    'is_superuser': user.is_superuser,
                    'is_staff': user.is_staff,
                    'last_login': last_login,
                })
        else:
            return Response(
                {
                    'status': 'error: disabled account',
                    'id': '', 'email': '', 'user_permission': '',
                    'is_superuser': '', 'is_staff': '', 'last_login': ''
                })
    else:
        return Response(
            {
                'status': 'error: invalid credentials', 'id': '', 'email': '', 'user_permission': '',
                'is_superuser': '', 'is_staff': '', 'last_login': ''
            })


@api_view(['GET'])
def logout_view(request):
    logout(request)
    return Response({'status': 'success'})


class ManufacturerList(generics.ListCreateAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly)
    filter_class = ManufacturerFilter


class ManufacturerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly,)


class ModuleList(generics.ListCreateAPIView):
    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]

            # check if many is required
            if isinstance(data, list):
                kwargs["many"] = True

        return super(ModuleList, self).get_serializer(*args, **kwargs)

    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly)
    filter_class = ModuleFilter


class ModuleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly,)


class InverterList(generics.ListCreateAPIView):
    queryset = Inverter.objects.all()
    serializer_class = InverterSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly)
    filter_class = InverterFilter


class InverterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inverter.objects.all()
    serializer_class = InverterSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly,)


class BatteryList(generics.ListCreateAPIView):
    queryset = Battery.objects.all()
    serializer_class = BatterySerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly)
    filter_class = BatteryFilter


class BatteryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Battery.objects.all()
    serializer_class = BatterySerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly,)


class FileUploadView(APIView):
    # MultiPartParser AND FormParser
    # https://www.django-rest-framework.org/api-guide/parsers/#multipartparser
    # "You will typically want to use both FormParser and MultiPartParser
    # together in order to fully support HTML form data."
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        product_json = excelToDict(request.FILES["file"])
        print(product_json)
        if (product_json['module'] == True and product_json['inverter'] == True):
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class FileUploadViewGenericProduct(APIView):
    # MultiPartParser AND FormParser
    # https://www.django-rest-framework.org/api-guide/parsers/#multipartparser
    # "You will typically want to use both FormParser and MultiPartParser
    # together in order to fully support HTML form data."
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        product_json = excelToDictGenericProduct(request.FILES["file"])
        if (product_json):
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ProductList(generics.ListCreateAPIView):
    # def get_queryset(self):
    #     if self.request.query_params.get('search'):

    # This line of code allows you to post multiple dictionaries. I don't know why it works, will have to go back and
    # refactor this logic. Will need to make a ListSerializer or override the existing Serializer to support bulk.
    # Taken from stackoverflow question 43525860
    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]

            # check if many is required
            if isinstance(data, list):
                kwargs["many"] = True

        return super(ProductList, self).get_serializer(*args, **kwargs)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly,)
    filter_class = ProductFilter
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['ProductCode', 'ManufacturerName', 'ManufacturerProductID', 'ManufacturerCode']


