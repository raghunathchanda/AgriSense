from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.views.decorators.cache import never_cache

from farm.models import Crop, CropSale, CropExpense, Harvest


@login_required
@never_cache
def dashboard_view(request):
    crops = Crop.objects.filter(farmer=request.user)
    active_crops_count = crops.filter(status='Growing').count()
    total_acres = crops.aggregate(Sum('acres'))['acres__sum'] or 0

    total_investment = CropExpense.objects.filter(crop__farmer=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    sales = CropSale.objects.filter(crop__farmer=request.user)
    total_sales = sum([sale.sales_revenue for sale in sales])
    total_profit = total_sales - total_investment

    context = {
        'active_crops_count': active_crops_count,
        'total_acres': total_acres,
        'total_investment': total_investment,
        'total_sales': total_sales,
        'total_profit': total_profit,
        'recent_crops': crops[:5]
    }
    return render(request, 'farm/dashboard.html', context)

@login_required
@never_cache
def crop_list_view(request):
    crops = Crop.objects.filter(farmer=request.user)
    return render(request, 'farm/crop_list.html', {'crops': crops})

@login_required
@never_cache
def crop_create_view(request):
    if request.method == 'POST':
        Crop.objects.create(
            farmer=request.user,
            name=request.POST.get('name'),
            variety=request.POST.get('variety', ''),
            acres=request.POST.get('acres'),
            season=request.POST.get('season'),
            start_date=request.POST.get('start_date'),
            expected_harvest_date=request.POST.get('expected_harvest_date') or None,
            actual_harvest_date=request.POST.get('actual_harvest_date') or None,
            status=request.POST.get('status', 'Planned'),
            notes=request.POST.get('notes', '')
        )
        return redirect('farm:crop_list')
    return render(request, 'farm/crop_form.html', {'title': 'Add Crop'})

@login_required
@never_cache
def crop_detail_view(request, pk):
    crop = get_object_or_404(Crop, pk=pk, farmer=request.user)
    expenses = crop.expenses.all()
    harvests = crop.harvests.all()
    sales = crop.sales.all()

    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_revenue = sum([sale.sales_revenue for sale in sales])
    net_profit = total_revenue - total_expense

    context = {
        'crop': crop,
        'expenses': expenses,
        'harvests': harvests,
        'sales': sales,
        'total_expense': total_expense,
        'total_revenue': total_revenue,
        'net_profit': net_profit,
    }
    return render(request, 'farm/crop_detail.html', context)

@login_required
@never_cache
def crop_update_view(request, pk):
    crop = get_object_or_404(Crop, pk=pk, farmer=request.user)
    if request.method == 'POST':
        crop.name = request.POST.get('name')
        crop.variety = request.POST.get('variety', '')
        crop.acres = request.POST.get('acres')
        crop.season = request.POST.get('season')
        crop.start_date = request.POST.get('start_date')
        crop.expected_harvest_date = request.POST.get('expected_harvest_date') or None
        crop.actual_harvest_date = request.POST.get('actual_harvest_date') or None
        crop.status = request.POST.get('status')
        crop.notes = request.POST.get('notes', '')
        crop.save()
        return redirect('farm:crop_detail', pk=crop.pk)
    return render(request, 'farm/crop_form.html', {'crop': crop, 'title': 'Edit Crop'})

@login_required
@never_cache
def crop_delete_view(request, pk):
    crop = get_object_or_404(Crop, pk=pk, farmer=request.user)
    if request.method == 'POST':
        crop.delete()
        return redirect('farm:crop_list')
    return render(request, 'farm/crop_confirm_delete.html', {'crop': crop})

@login_required
@never_cache
def expense_create_view(request, crop_pk):
    crop = get_object_or_404(Crop, pk=crop_pk, farmer=request.user)
    if request.method == 'POST':
        CropExpense.objects.create(
            crop=crop,
            expense_date=request.POST.get('expense_date'),
            category=request.POST.get('category'),
            amount=request.POST.get('amount'),
            description=request.POST.get('description', ''),
            quantity=request.POST.get('quantity', '')
        )
        return redirect('farm:crop_detail', pk=crop.pk)
    return render(request, 'farm/expense_form.html', {'crop': crop})


@login_required
@never_cache
def harvest_create_view(request, crop_pk):
    crop = get_object_or_404(Crop, pk=crop_pk, farmer=request.user)

    if request.method == 'POST':
        Harvest.objects.create(
            crop=crop,
            harvest_date=request.POST.get('harvest_date'),
            quantity=request.POST.get('quantity'),
            unit=request.POST.get('unit', 'kg'),
            notes=request.POST.get('notes', ''),
        )
        return redirect('farm:crop_detail', pk=crop.pk)

    return render(request, 'farm/harvest_form.html', {'crop': crop})


@login_required
@never_cache
def sale_create_view(request, crop_pk):
    crop = get_object_or_404(Crop, pk=crop_pk, farmer=request.user)
    harvests = crop.harvests.all()

    if request.method == 'POST':
        harvest_id = request.POST.get('harvest')
        harvest = None
        if harvest_id:
            harvest = get_object_or_404(Harvest, pk=harvest_id, crop=crop)

        quantity_sold = request.POST.get('quantity_sold')
        unit_price = request.POST.get('unit_price')
        selling_cost = request.POST.get('selling_cost', 0)

        CropSale.objects.create(
            crop=crop,
            harvest=harvest,
            sale_date=request.POST.get('sale_date'),
            quantity_sold=Decimal(str(quantity_sold)) if quantity_sold else 0,
            unit_price=Decimal(str(unit_price)) if unit_price else 0,
            buyer=request.POST.get('buyer', ''),
            selling_cost=Decimal(str(selling_cost)) if selling_cost else 0,
        )
        return redirect('farm:crop_detail', pk=crop.pk)

    return render(request, 'farm/sale_form.html', {'crop': crop, 'harvests': harvests})
