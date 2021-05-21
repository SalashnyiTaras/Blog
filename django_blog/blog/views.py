from django.shortcuts import render, get_object_or_404, reverse
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse


class PostListView(ListView):
    model = Post
    # TODO: What a hell is page.obj in home.html page( when creating paginating buttons )
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        # it shows total amount of likes
        context = super(PostListView, self).get_context_data(**kwargs)
        likes_var = get_object_or_404(Post, id=kwargs['id'])
        total_likes = likes_var.total_likes()
        context["total_likes"] = total_likes
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4


class PostDetailView(DetailView):
    # TODO: what is slag? get_slug_field()?
    model = Post

    def get_context_data(self, **kwargs):
        # it shows total amount of likes
        context = super(PostDetailView, self).get_context_data(**kwargs)
        likes_var = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = likes_var.total_likes()
        context["total_likes"] = total_likes
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        # we set that author of current form instance should be logged in user
        form.instance.author = self.request.user
        # basically we run form.valid() on our parent class after we set a author
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):   # ?????
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def donate(request):
    return render(request, 'blog/donate.html')


def like_detail_view(request, pk):
    # it is a button, to add a like
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


def like_list_view(request, pk):
    # it is a button, to add a like
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('blog-home'))

