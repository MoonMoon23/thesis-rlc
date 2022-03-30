from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

#Custom user model manager where faculty id is the unique identifier for authentication.

class FacultyManager(BaseUserManager):
    def create_user(self, faculty_id, password, **extra_fields):
        """
        Create and save a User with the given id and password.
        """
        if not faculty_id:
            raise ValueError(_('The Faculty ID must be set'))
        user = self.model(faculty_id=faculty_id, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, faculty_id, password, **extra_fields):
        """
        Create and save a SuperUser with the given id and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(faculty_id, password, **extra_fields)
