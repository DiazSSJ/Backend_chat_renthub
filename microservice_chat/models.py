from django.db import models
from django.contrib.auth.models import AbstractUser,  Group, Permission
from django.db.models.signals import post_save

# Create your models here.

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, id_origin, name='', last_name='', **extra_fields):
        if not id_origin:
            raise ValueError('El campo id_origin debe ser proporcionado.')

        user = self.model(
            id_origin=id_origin,
            name=name,
            last_name= last_name,
        )

        user.set_unusable_password()  # Esto establece una contraseña no utilizable
        user.save(using=self._db)
        return user

    def create_superuser(self, id_origin, name='', last_name=''):
   
        return self.create_user(id_origin, name, last_name)


class User(AbstractUser):
    id_origin = models.IntegerField(unique=True,null=True)
    name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    username = models.CharField(max_length=30, unique=False)

    groups = models.ManyToManyField(Group, related_name="users")
    user_permissions = models.ManyToManyField(Permission, related_name="users")

    objects = CustomUserManager()

    def profile(self):
        profile = Profile.objects.get(user=self)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="user_images", default="default.jpg")
    #verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.full_name = f"{self.user.name} {self.user.last_name}"
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)


# Chat App Model
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="received_messages")

    message = models.CharField(max_length=1000)

    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date']
        verbose_name_plural = "Message"

    
    """
    @property
    def sender_profile(self):
        sender_profile = Profile.objects.get(user=self.sender)
        return sender_profile
    
    
    @property
    def reciever_profile(self):
        reciever_profile = Profile.objects.get(user=self.receiver)
        return reciever_profile
    """

