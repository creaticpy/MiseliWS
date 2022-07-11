from aplicaciones.shared_apps.models import MenusSistemaModel, SubMenusSistemasModel
from django.shortcuts import render
import uuid
from django.views import View


class IndexView(View):
    templateName = 'template_base.html'

    def get(self, request):
        context = {
            "menu": MenusSistemaModel.objects.all().order_by("orden_visualizacion"),
            "sub_menu": SubMenusSistemasModel.objects.all().order_by("orden_visualizacion"),
            "uuid": uuid,
        }

        return render(request, self.templateName, context=context)



