from django.contrib.auth.models import Group, BaseUserManager
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    """
    Custom user manager where email is the required identifier for all users,
    including regular users, managers, and superusers.
    """

    def create_user(self, username, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError("Regular users must have an email address")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with email, password, and admin permissions.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Ensure that email is provided
        if not email:
            raise ValidationError("Superusers must have an email address")

        return self._create_user(username, email, password, **extra_fields)

    def create_manager(self, username, email, password=None, **extra_fields):
        """
        Create and save a Manager with email, password, and manager permissions.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)

        # Ensure email is provided for the manager
        if not email:
            raise ValidationError("Managers must have an email address")

        user = self._create_user(username, email, password, **extra_fields)

        # Assign the user to the "Managers" group
        manager_group, _ = Group.objects.get_or_create(name="Managers")
        user.groups.add(manager_group)

        return user

    def _create_user(self, username, email, password=None, **extra_fields):
        """
        Internal method to create a user (either manager or regular user) with email.
        """
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
