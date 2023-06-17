from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView, TemplateView
)
from django.urls import reverse_lazy

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def simple_view(request):
    return HttpResponse('Страница для залогиненных пользователей!')


class HomePage(LoginRequiredMixin, TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста из родительского метода.
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь ключ total_count;
        # значение ключа — число объектов модели Birthday.
        context['total_count'] = Birthday.objects.count()
        # Возвращаем изменённый словарь контекста.
        return context


class BirthdayListView(LoginRequiredMixin, ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 10


class BirthdayCreateView(LoginRequiredMixin, CreateView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayUpdateView(LoginRequiredMixin, UpdateView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayDeleteView(LoginRequiredMixin, DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayDetailView(LoginRequiredMixin, DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        return context
