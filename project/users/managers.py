from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, phone_number='', password=None, is_active=False):
        """
        Create and save user
        """
        user = self.model(

            email=email,
            full_name=full_name,
            phone_number=phone_number,
            is_active=is_active,
        )

        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, full_name, password,  phone_number):
        user = self.create_user(email, full_name, password, phone_number)

        user.is_admin = True
        user.is_active = True
        user.is_superuser = True

        user.save(using=self.db)

        return user