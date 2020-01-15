from django.db import models
from pyuploadcare.dj.models import ImageField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model):
    bio = models.TextField(max_length = 500)
    profile_pic = ImageField(blank=True, manual_crop="")
    location = models.CharField(max_length = 100) 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save_profile(self):
        self.user

    def delete_profile(self):
        self.delete()


class Project(models.Model):
    title = models.CharField(max_length = 100)
    image = ImageField(blank=True, manual_crop="")
    url = models.CharField(max_length=250, null= True)
    description = models.TextField(max_length = 500)
    posted = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects', null=True)

    def __str__(self):
        return f'{self.user.name} Project'

    def get_absolute_url(self):
        return f"/single_post/{self.id}"

    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()

class Rating(models.Model):
    rating = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )

    design = models.IntegerField(choices=rating, default=0, blank=True)
    usability = models.IntegerField(choices=rating, blank=True)
    content = models.IntegerField(choices=rating, blank=True)
    score = models.FloatField(default=0, blank=True)
    design_average = models.FloatField(default=0, blank=True)
    usability_average = models.FloatField(default=0, blank=True)
    content_average = models.FloatField(default=0, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='rater')
    post = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings', null=True)

    class Meta:
        get_latest_by='score'
    
    @classmethod
    def get_leading_project(cls):
        post=cls.objects.latest()
        return post

    def save_rating(self):
        self.save()

    @classmethod
    def get_ratings(cls, id):
        ratings = Rating.objects.filter(post_id=id).all()
        return ratings

    def __str__(self):
        return f'{self.post} Rating'