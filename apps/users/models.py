from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

class User(AbstractUser):
    class UserType(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        BUSINESS_OWNER = 'BUSINESS_OWNER', _('Business Owner')

    class BusinessType(models.TextChoices):
        INDIVIDUAL = 'IND', _('Individual')
        COMPANY = 'COM', _('Company')
        PARTNERSHIP = 'PAR', _('Partnership')
        NONPROFIT = 'NPO', _('Non Profit')

    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.BUSINESS_OWNER
    )
    # Business owner specific fields
    business_name = models.CharField(max_length=255, blank=True, null=True)
    business_type = models.CharField(
        max_length=3,
        choices=BusinessType.choices,
        blank=True,
        null=True
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    address = models.TextField(blank=True)
    tax_number = models.CharField(max_length=50, blank=True)
    is_verified = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        if self.user_type == self.UserType.BUSINESS_OWNER:
            return f"{self.business_name} ({self.email})"
        return f"Admin: {self.email}"

    def save(self, *args, **kwargs):
        if self.user_type == self.UserType.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)