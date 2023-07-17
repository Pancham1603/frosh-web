from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, registration_id, password=None, **extra_fields):
        if not registration_id:
            raise ValueError("Registration ID is required!")
        
        extra_fields['email'] = self.normalize_email(extra_fields['email'])
        user = self.model(registration_id=registration_id, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, registration_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(registration_id, password, **extra_fields)