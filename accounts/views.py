from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import FarmerProfile


def register_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        mobile = request.POST.get('mobile')
        village = request.POST.get('village')
        district = request.POST.get('district')
        state = request.POST.get('state')

        if password != confirm_password:
            error = "Passwords do not match."
        elif User.objects.filter(username=username).exists():
            error = "Username already taken."
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            FarmerProfile.objects.create(
                user=user,
                mobile=mobile,
                village=village,
                district=district,
                state=state
            )
            login(request, user)
            return redirect('farm:dashboard')

    return render(request, 'accounts/register.html', {'error': error})


@login_required
@never_cache
def profile_view(request):
    profile, created = FarmerProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.mobile = request.POST.get('mobile', profile.mobile)
        profile.village = request.POST.get('village', profile.village)
        profile.district = request.POST.get('district', profile.district)
        profile.state = request.POST.get('state', profile.state)

        total_land_acres = request.POST.get('total_land_acres')
        if total_land_acres:
            profile.total_land_acres = Decimal(total_land_acres)

        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('accounts:profile')

    return render(request, 'accounts/profile.html', {'profile': profile})
