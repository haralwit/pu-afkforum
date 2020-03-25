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
from .models import Post
from updown.views import AddRatingFromModel


def home(request):
    context = {"posts": Post.objects.all()}
    return render(request, "forum/home.html", context=context)


class PostListView(ListView):
    model = Post
    template_name = "forum/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]  # negative sign inverses order from newest to oldest
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = "forum/user_posts.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]  # negative sign inverses order from newest to oldest
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")


class PostDetailView(DetailView):
    model = Post


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if (
            self.request.user == post.author
            or self.request.user.profile.role == "admin"
        ):
            return True
        return False


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):

        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if (
            self.request.user == post.author
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
        return redirect('post-detail', pk=object_id)



