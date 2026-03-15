from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Custom manager for User model with email as the unique identifier."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('staff', 'Staff'),
    ]

    username = None  # Remove username field
    email = models.EmailField('email address', unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='staff')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_admin(self):
        return self.role == 'admin'


class Cabinet(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='cabinets_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def file_count(self):
        return self.files.filter(is_deleted=False).count()

    @property
    def phase_count(self):
        return self.phases.count()


class Phase(models.Model):
    cabinet = models.ForeignKey(
        Cabinet, on_delete=models.CASCADE, related_name='phases'
    )
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='phases_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']
        unique_together = ['cabinet', 'name']

    def __str__(self):
        return f"{self.cabinet.name} - {self.name}"


class File(models.Model):
    STATUS_CHOICES = [
        ('normal', 'Normal'),
        ('petition', 'Petition'),
        ('petition_in_progress', 'Petition in Progress'),
        ('petition_solved', 'Petition Solved'),
        ('custom', 'Other (Custom)'),
    ]

    cabinet = models.ForeignKey(
        Cabinet, on_delete=models.CASCADE, related_name='files'
    )
    phase = models.ForeignKey(
        Phase, on_delete=models.SET_NULL, null=True, blank=True, related_name='files'
    )
    file_name = models.CharField(max_length=500)
    file_number = models.CharField(max_length=100, unique=True)
    case_brief = models.CharField(max_length=500, blank=True, default='')
    date_invited = models.DateField(null=True, blank=True)

    document_image = models.ImageField(
        upload_to='document_images/%Y/%m/', blank=True, null=True
    )
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default='normal'
    )
    custom_status = models.CharField(max_length=100, blank=True, default='')

    # Audit fields
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='files_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='files_updated'
    )
    updated_at = models.DateTimeField(auto_now=True)

    # Soft delete
    is_deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='files_deleted'
    )
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.file_name} ({self.file_number})"

    @property
    def display_status(self):
        if self.status == 'custom' and self.custom_status:
            return self.custom_status
        return self.get_status_display()
