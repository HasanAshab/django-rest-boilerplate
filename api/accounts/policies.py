class UserPolicy():
    def delete(user, targerUser):
        return (user == targerUser or
            (user.is_staff and not user.is_staff and not user.is_superuser) or 
            (user.is_superuser and not user.is_superuser))