from rest_framework import serializers


class HelloSerializers(serializers.Serializer):
    """Serializa un campo para probar nuestro APIview"""
    name = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)




