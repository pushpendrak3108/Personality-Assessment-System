from django.db import models
from django.db.models.signals import post_save
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(default=20)
    gender = models.CharField(max_length=100, default='Male')
    o_score = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    c_score = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    e_score = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    a_score = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    n_score = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    predicted_personality_type = models.CharField(max_length=100, default='none')
    test_score = models.PositiveIntegerField(default=0)
    taken_apt_test = models.BooleanField(default=False)
    taken_personality_test = models.BooleanField(default=False)
    mbti_statement = models.CharField(max_length=1000000, default='None')
    mbti_type = models.CharField(max_length=100, default='xxxx')
    taken_mbti_test = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
