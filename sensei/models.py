from django.db import models
from users.models import User

student = User()

class PageVisit(models.Model):
    user = models.ForeignKey(student, on_delete=models.CASCADE)
    page_name = models.CharField(max_length=100)
    time_spent_seconds = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class UserPageVisit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    page_visits = models.ManyToManyField(PageVisit)