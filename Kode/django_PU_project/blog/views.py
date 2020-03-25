from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.http import HttpResponse
from .models import Thread
from updown.views import AddRatingFromModel


def home(request):
    context = {"threads": Thread.objects.all()}
    return render(request, "forum/home.html", context=context)


class ThreadListView(ListView):
    model = Thread
    template_name = "forum/home.html"
    context_object_name = "threads"
    ordering = ["-date_posted"]  # negative sign inverses order from newest to oldest
    paginate_by = 5


class UserThreadListView(ListView):
    model = Thread
    template_name = "forum/user_threads.html"
    context_object_name = "threads"
    ordering = ["-date_posted"]  # negative sign inverses order from newest to oldest
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Thread.objects.filter(author=user).order_by("-date_posted")


class ThreadDetailView(DetailView):
    model = Thread


class ThreadDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Thread
    success_url = "/"

    def test_func(self):
        thread = self.get_object()
        if (
            self.request.user == thread.author
            or self.request.user.profile.role == "admin"
        ):
            return True
        return False


class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ThreadUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Thread
    fields = ["title", "content"]

    def form_valid(self, form):

        return super().form_valid(form)

    def test_func(self):
        thread = self.get_object()
        if (
            self.request.user == thread.author
            or self.request.user.profile.role == "admin"
        ):
            return True
        return False


def about(request):
    return render(request, "forum/about.html", context={"title": "About"})

class GiveVote(AddRatingFromModel):
    def __call__(self, request, model, app_label, object_id, field_name, score, **kwargs):
        response = super(GiveVote, self).__call__(request, model, app_label, object_id, field_name, score, **kwargs)
        message = (response.content).decode("UTF-8")
        if(response.status_code!=403):
            messages.success(request,message)
        else:
            messages.warning(request,message)
        return redirect('thread-detail', pk=object_id)



