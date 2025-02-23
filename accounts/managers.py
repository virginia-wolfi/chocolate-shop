from django.contrib.auth.models import UserManager


class UserManager(UserManager):
    """
    User model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """

        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        return super().create_superuser(username, email, password, **extra_fields)
