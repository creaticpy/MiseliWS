import json
from aplicaciones.shared_apps.models import MenusSistemaModel, SubMenusSistemasModel
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
import uuid
from django.views import View
from django.views.generic import ListView


class IndexView(View):
    templateName = 'template_base.html'

    def get(self, request):
        context = {
            "menu": MenusSistemaModel.objects.all().order_by("orden_visualizacion"),
            "sub_menu": SubMenusSistemasModel.objects.all().order_by("orden_visualizacion"),
            "uuid": uuid,
        }

        return render(request, self.templateName, context=context)
        # return HttpResponse(json.dumps(context, cls=DjangoJSONEncoder), content_type='application/json')


