from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound


class NotFoundAPIView(APIView):
    def get(self, request, *args, **kwargs):
        raise NotFound

    def post(self, request, *args, **kwargs):
        raise NotFound

    def put(self, request, *args, **kwargs):
        raise NotFound

    def delete(self, request, *args, **kwargs):
        raise NotFound
