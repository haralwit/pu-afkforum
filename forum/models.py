from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from updown.fields import RatingField


class Thread(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = RatingField(can_change_vote=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('thread-detail', kwargs={'pk': self.pk})