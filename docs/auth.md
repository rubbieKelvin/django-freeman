# Authentication

> module: `freeman/auth`

This module helps setting up authentication in django apps. I'd be improving upon this documentation frome time to a time, and also add more features.

## Setting up

### 1. Add freeman to installed apps

```python
INSTALLED_APPS = [
    # ...
    "rest_framework",
    "freeman",
    "freeman.auth",
]
```

### 2. Creating the user model

```python
from django.db import models
from freeman.auth.models import BaseUserModel


class User(BaseUserModel):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=60, null=False)
    last_name = models.CharField(max_length=60, null=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

```

if you want to make changes to your User model manager, you can create a Manager class

```python
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email: str, password: str, **extra_fields: str | bool):
        if not email:
            raise ValueError("The email must be set")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, password: str, **extra_fields: str | bool):
        extra_fields["is_active"] = True
        extra_fields["is_superuser"] = True

        return self.create_user(email, password, **extra_fields)

```

The you can mow add your manager to the user model

```python
class User(BaseUserModel):
    # ...
    objects = UserManager()
```

Now let's set our auth_model in django settings to the custom user class we just created. if your user model is in an app named `"myapp"`, we'll set out auth model to `"myapp.User"`

```python
AUTH_USER_MODEL = "myapp.User"
```

### 3. Make migrations

```shell
python manage.py makemigrations authapp myapp
python manage.py migrate
```

### 4. add freeman auth to restframework authentication

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "freeman.authapp.authentication.FreemanAuthentication",
    ),
    #...
}
```
