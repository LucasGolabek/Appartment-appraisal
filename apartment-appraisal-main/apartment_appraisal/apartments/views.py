from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from django.conf import settings

from apartments.models import UserApartment
from apartments.serializers import (
    WriteUserApartmentSerializer,
    GetUserApartmentsSerializer,
    RegisterUserSerializer,
)

from apartments.utils import update_apartments, get_apartments_suggestions_and_estimation


if getattr(settings, 'DB_UPDATE', None):
    update_apartments(delete_outdated=False)


class RegisterUserView(ModelViewSet):
    queryset = User.objects
    serializer_class = RegisterUserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)

        return super(RegisterUserView, self).get_permissions()


class UserApartmentView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = WriteUserApartmentSerializer(data=data, context={"request": request})

        if(serializer.is_valid()):
            serializer.save()
        else:
            print(serializer.errors)
            return JsonResponse(serializer.errors, status=400)

        return JsonResponse({"data": get_apartments_suggestions_and_estimation(serializer.data)}, status=201)


class UserApartmentsGetView(ModelViewSet):
    serializer_class = GetUserApartmentsSerializer

    def get_queryset(self):
        return UserApartment.objects.filter(user=self.request.user)
