from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class UserProfile(models.Model):
    MALE = 1
    FEMALE = 2
    OTHER = 3
    GENDERS = (
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHER, "Other"),
    )

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    birth_date = models.DateField(verbose_name="Birth date", blank=True, null=True)
    gender = models.PositiveSmallIntegerField(
        verbose_name="Gender",
        choices=GENDERS,
        blank=True,
        null=True,
    )

    ENTRY_LEVEL = 1
    MANAGER = 2
    OTHER = 3

    EXPERIENCE_LEVELS = (
        (ENTRY_LEVEL, "Entry level"),
        (MANAGER, "Manager"),
        (OTHER, "Other"),
    )

    experience_level = models.PositiveSmallIntegerField(
        verbose_name="Job title",
        choices=EXPERIENCE_LEVELS,
        blank=True,
        null=True,
    )
    expected_salary = models.DecimalField(
        verbose_name="Expected salary",
        decimal_places=2,
        max_digits=10,
        blank=True,
        null=True,
    )
    completed_welcome = models.BooleanField(default=False)

    class Meta:
        app_label = "registration"

    def __str__(self):
        return f"{self.user.username} profile"


class Interest(models.Model):
    name = models.CharField(verbose_name="Name", max_length=255)
    slug = models.SlugField(editable=False)
    users = models.ManyToManyField(User, related_name="interests")

    class Meta:
        app_label = "registration"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
