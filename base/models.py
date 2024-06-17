from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from enum import Enum

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        try:
            user.save()
            print('user has been saved')
            print(user)
        except Exception as e:
            print(e)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"CustomUser(id={self.id}, email='{self.email}', is_staff={self.is_staff})"


# class Color(models.Model):
#     name = models.CharField(max_length=50, primary_key=True)
#     pastel = models.BooleanField(default=False)
    
#     def get_model_fields(model):
#         return model._meta.fields

# class Event(models.Model):
#     color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
#     userId = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

#     name = models.CharField(max_length=50, default='(No title)')
#     start = models.IntegerField(validators=[MaxValueValidator(95), MinValueValidator(0)])
#     end = models.IntegerField(validators=[MaxValueValidator(96), MinValueValidator(1)])
#     date = models.DateField()

class Message(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    replyTo = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    imageUrl = models.CharField(max_length=200, null=True, blank=True)

class Reaction(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reactedOn = models.ForeignKey(Message, on_delete=models.CASCADE)

    class EmojiChoices(models.TextChoices):
        SMILEY = "😊", "Smiley"
        HEART = "❤️", "Heart"
        THUMBS_UP = "👍", "Thumbs Up"
        THUMBS_DOWN = "👎", "Thumbs Down"
        LAUGH = "😂", "Laugh"

    emoji = models.CharField(
        max_length=2,
        choices=EmojiChoices.choices,
        default=EmojiChoices.SMILEY,
    )