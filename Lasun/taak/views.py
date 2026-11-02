from django.shortcuts import render
from .models import TaakVarity
from django.shortcuts import get_object_or_404

# Create your views here.

def all_taak(request):
    taaks = TaakVarity.objects.all()
    return render(request,'taak/all_taak.html',{'taaks':taaks})

def taak_detail(request,taak_id):
    taak = get_object_or_404(TaakVarity,pk=taak_id)
    return render(request,'taak/taak_detail.html',{'taak':taak})
