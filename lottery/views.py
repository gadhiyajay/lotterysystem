from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import User
from .forms import LotteryForm
from .models import Lottery, LotteryEntry
from django.core.exceptions import PermissionDenied


def lottery_list(request):
    lotteries = Lottery.objects.all().order_by =['expiry_date']
    # paginator start::
    p = Paginator(Lottery.objects.all(), 4)
    page = request.GET.get('page')
    final_list = p.get_page(page)
    # final_list is the list with the pagination
    return render(request, 'lottery/lottery_list.html', {'lotteries': lotteries, 'final_list': final_list})


@login_required
def create_lottery(request):
    # Check if the user is a vendor
    if request.user.user_type != 'vendor':
        message = 'You must be a vendor to create a lottery.'
        messages.error(request, message)
        raise PermissionDenied

    if request.method == 'POST':
        form = LotteryForm(request.POST, request.FILES)
        if form.is_valid():
            lottery = form.save(commit=False)
            lottery.creator = request.user
            lottery.save()
            messages.success(request, 'Lottery created successfully!')
            return redirect('lottery_list')
    else:
        form = LotteryForm()

    return render(request, 'lottery/create_lottery.html', {'form': form})


def lottery_detail(request, pk):
    lottery = get_object_or_404(Lottery, pk=pk)
    return render(request, 'lottery/lottery_detail.html', {'lottery': lottery})


@login_required
def lottery_entry(request, pk):
    lottery = get_object_or_404(Lottery, pk=pk)
    if request.user.user_type == 'buyer':
        if request.method == 'POST':
            if timezone.now() < lottery.expiry_date:
                LotteryEntry.objects.create(user=request.user, lottery=lottery)
                messages.success(request, 'Congratulations, You have entered in the lottery successful!!')
            else:
                messages.warning(request, 'The Lottery Entry date has passed, not possible to enter!')
            return redirect('lottery_detail', pk=pk)
        return render(request, 'lottery/lottery_enter.html', {'lottery': lottery})
    else:
        messages.warning(request, "You can only buy using the buyer's account!")
        return redirect('lottery_detail', pk=pk)


@login_required
def user_lottery_entries(request):
    if request.user.user_type != 'vendor':
        message = 'You must be a vendor to view the entries of a lottery.'
        messages.error(request, message)
        raise PermissionDenied(message)
    entries = (
        LotteryEntry.objects.values('user__username', 'lottery__title', 'lottery__amount_to_enter')
        .annotate(entry_count=Count('id'))
    )

    return render(request, 'lottery/lottery_entries.html', {'entries': entries})


@login_required()
def my_lotteries(request):
    lottery_entries = LotteryEntry.objects.filter(user=request.user)
    return render(request, 'lottery/my_lotteries.html', {'lottery_entries': lottery_entries})


@login_required
def delete_lottery(request, pk):
    lottery = get_object_or_404(Lottery, pk=pk)
    if request.user == lottery.creator:
        lottery.delete()
        messages.success(request, 'The lottery was deleted successfully!')
    else:
        messages.warning(request, "You don't have permission to delete this lottery!")

    return redirect('lottery_list')


@login_required
def edit_lottery(request, pk):
    lottery = get_object_or_404(Lottery, pk=pk)
    if request.method == 'POST':
        if request.user == lottery.creator:
            form = LotteryForm(request.POST, instance=lottery)
            if form.is_valid():
                form.save()
                return redirect('lottery_list')
        else:
            messages.warning(request, 'Only the creator of the lottery can alter the lottery.!!')
            return redirect('lottery_list')
    else:
        form = LotteryForm(instance=lottery)

    return render(request, 'lottery/edit_lottery.html', {'form' : form})



