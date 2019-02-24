from django.views.generic import ListView

from .mixin import LoginRequiredMixin
from apps.custom import SandboxCreateView, SandboxUpdateView, BreadcrumbMixin
from .models import Menu,Structure
from django.shortcuts import render
from django.views.generic.base import View
import  json


class MenuCreateView(SandboxCreateView):
    model = Menu
    fields = '__all__'

    def get_context_data(self, **kwargs):
        kwargs['menu_all'] = Menu.objects.all()
        return super().get_context_data(**kwargs)


class MenuListView(LoginRequiredMixin, BreadcrumbMixin, ListView):
    model = Menu
    context_object_name = 'menu_all'


class MenuUpdateView(SandboxUpdateView):
    model = Menu
    fields = '__all__'
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        kwargs['menu_all'] = Menu.objects.all()
        return super().get_context_data(**kwargs)

class getMenuTree:
    def getStructure(self):
        fields = ['id', 'name', 'parent__id', ]
        structures = list(Structure.objects.all().values(*fields))
        return  structures

    def getChildren(self,id=None):
        sz=[]
        structures = self.getStructure()
        for obj in structures:
            if obj["parent__id"] == id:
                sz.append({"id":obj["id"],"name":obj["name"],"children":self.getChildren(obj["id"])})
        return sz

    def print(self):
        sz = self.getChildren(id=None)
        print(json.dumps(sz,ensure_ascii=False))
        return json.dumps(sz,ensure_ascii=False)


class MenuTree(View):
    def get(self,request):
        #nodes = Structure.objects.all()
        nodes = getMenuTree().print()
        return render(request, 'menutree.html', {'nodes': nodes})
