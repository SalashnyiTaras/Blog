from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User


class PostListView(ListView):
    model = Post
    # TODO: how to check which attributes are built-in, for instance how can I know that it is enough to set
    #       paginate_by in order to do pagination.
    # TODO: What a hell is page.obj in home.html page( when creating paginating buttons )
    # be default ListView renders template <app>/<model>_<viewtype>.html - blog/post_list.html.
    # instead of renaming our template we can set a variable template_name
    template_name = 'blog/home.html'
    # by default List view is going to loop through variables named "objects"
    # so we need to change variable name to 'posts'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        # TODO: how can I get data from User which is logged in and who makes some requests, for instance here we
        #       recieve a username from that user
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        # we set that author of current form instance should be logged in user
        form.instance.author = self.request.user
        # basically we run form.valid() on our parent class after we set a author
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

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


def about(request):
    return render(request, 'blog/about.html')


def donate(request):
    return render(request, 'blog/donate.html')
