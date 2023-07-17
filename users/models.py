from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to="users_images", blank=True, null=True)
    is_verified_email = models.BooleanField(default=False)
    email = models.EmailField(unique=True, blank=False)


class Category(models.Model):
    name = models.CharField(max_length=56, unique=True)

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    file_add = models.FileField(null=True, blank=True, upload_to="add_files")

    def __str__(self) -> str:
        return f"Объявление: {self.title} | Автор объявления: {self.author}"


class Comment(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.text[:30]


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f"EmailVerefication object for {self.user.email}"

    def send_verefication_email(self):
        link = reverse(
            "users:email_verefication",
            kwargs={"email": self.user.email, "code": self.code},
        )
        verefication_link = f"{settings.DOMAIN_NAME}{link}"
        subject = f"Подтверждение учетной записи для {self.user.username}"
        message = (
            "Для подтверждения учетной записил для {} перейдите по ссылке {}".format(
                self.user.email, verefication_link
            )
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False
