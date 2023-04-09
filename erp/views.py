from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Inbound, Outbound
from .forms import InboundForm, OutboundForm


def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def inbound(request):
    if request.method == 'POST':
        form = InboundForm(request.POST)
        if form.is_valid():
            inbound = form.save(commit=False)
            inbound.save()
            messages.success(request, '출고 완료')
            return redirect('erp:index')
    else:
        form = InboundForm()
    return render(request, 'inbound.html', {'form': form})


def outbound(request):
    if request.method == 'POST':
        form = OutboundForm(request.POST)
        if form.is_valid():
            outbound = form.save(commit=False)
            try:
                outbound.save()
                messages.success(request, '출고 완료')
            except ValueError as e:
                messages.error(request, str(e))
            return redirect('erp:index')
    else:
        form = OutboundForm()
    return render(request, 'outbound.html', {'form': form})
