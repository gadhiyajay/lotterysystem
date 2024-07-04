from django.shortcuts import render, redirect, get_object_or_404
from .models import Lottery, LotteryEntry
from .forms import LotteryForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Count


def lottery_list(request):
    lotteries = Lottery.objects.all()
    # paginator chalu::
    p = Paginator(Lottery.objects.all(), 4)
    page = request.GET.get('page')
    final_list = p.get_page(page)

    return render(request, 'lottery/lottery_list.html', {'lotteries': lotteries, 'final_list' : final_list })


@login_required
def create_lottery(request):
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
    if request.method == 'POST':
        if timezone.now() < lottery.expiry_date:
            LotteryEntry.objects.create(user=request.user, lottery=lottery)
            messages.success(request, 'Congratulations, You have entered in the lottery successful!!')
        else:
            messages.warning(request, 'The Lottery Entry date has passed, not possible to enter!')
        return redirect('lottery_detail', pk=pk)
    return render(request, 'lottery/lottery_enter.html', {'lottery': lottery})


@login_required
def user_lottery_entries(request):
    entries = (
        LotteryEntry.objects.values('user__username', 'lottery__title')
        .annotate(entry_count=Count('id'))
    )

    print(entries)

    return render(request, 'lottery/lottery_entries.html', {'entries': entries})

