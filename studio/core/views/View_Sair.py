from django.shortcuts import redirect, render
from django.views import View


class SairView(View):
    def get(self,request):
        request.session.flush()

        return redirect("paginaInicial") 

