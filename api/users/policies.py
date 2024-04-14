class UserPolicy():
    def delete(self, user, targer_user):
        return (user == targer_user or
            (user.is_staff and not targer_user.is_staff and not targer_user.is_superuser) or 
            (user.is_superuser and not targer_user.is_superuser))
            
    def change_role(self, user, targer_user):
        return user.is_superuser and not targer_user.is_superuser