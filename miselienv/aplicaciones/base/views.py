import json

from django.shortcuts import render

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

# from rest_framework.views import APIView
# from rest_framework.response import Response
#
#
# from rest_framework import status
# from aplicaciones.base.serializers import HelloSerializers


class IndexView(LoginRequiredMixin, View):
    templateName = 'index.html'
    context = {'tableContainer':   'self.tableContainer'}

    def get(self, request, *args, **kwargs):
        return render(request, self.templateName, self.context)


# class HelloApi(APIView):
#     """Retornar lista de caracteristicas de APIview"""
#     serializers_class = HelloSerializers
#
#     def get(self, request, format=None):
#         an_apiview = (
#             'Usamos metodos HTTTP para funciones (get, post, patch, put, delete)',
#             'Es similar a una vista tradicional de Django',
#             'Nos da mayor control sobre la logica de nuestra aplicacion',
#             'Esta mapeado manualmente a los URLs',
#         )
#         return Response({'message': 'Hello', 'an_apiview': an_apiview})
#
#     def post(self, request):
#         """Crea  un mensaje con nuestro nombre"""
#
#         for x in request.data:
#             print(x, " - ", "aqui debio salir algo")
#         print(request.data)
#
#         serializer = self.serializers_class(data=request.data)
#
#         if serializer.is_valid():
#             content = serializer.validated_data.get('name')  # name es el usado en serializer.py class HelloSerializers
#
#             message = f'Hello {content}'
#             return Response({'message': message})
#         else:
#             return Response(
#                 serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#     def put(self, request, pk=None):
#         return Response({'method': 'PUT'})
#
#     def path(self, request, pk=None):
#         return Response({'method': 'PATCH'})
#
#     def delete(self, request, pk=None):
#         return Response({'method': 'DELETE'})


