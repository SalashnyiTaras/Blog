from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(blank=True, upload_to='post_pics')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # TODO: ManyToMany relationship will be useful because Post can have many likes from many users???
    #        What is related_name
    likes = models.ManyToManyField(User, related_name='blog_post')

    # TODO: basically we do not need to do migrations after we added class method
    #       but we do need to do migrations after we addded class attribute, simle isn't it?

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    # TODO: to find out the difference between redirect() and reverse()
    def get_absolute_url(self):
        # TODO: inspect what reverse does
        return reverse('post-detail', kwargs={'pk': self.pk})
