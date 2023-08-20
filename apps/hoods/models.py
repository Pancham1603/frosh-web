from django.db import models
# from..users.models import User

# Create your models here.

class Hood(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)
    member_count = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    is_booking = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# class HoodPreference(models.Model):
#     hood_1 = models.ForeignKey(Hood, related_name='hood_1', on_delete=models.DO_NOTHING)
#     hood_2 = models.ForeignKey(Hood, related_name='hood_2', on_delete=models.DO_NOTHING)
#     hood_3 = models.ForeignKey(Hood, related_name='hood_3', on_delete=models.DO_NOTHING)
#     hood_4 = models.ForeignKey(Hood, related_name='hood_4', on_delete=models.DO_NOTHING)
#     user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
#     datetime = models.DateTimeField(auto_now_add=True)