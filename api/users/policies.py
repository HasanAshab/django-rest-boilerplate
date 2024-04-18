class UserPolicy:
    def delete(self, user, target_user):
        return (
            user == target_user
            or (
                user.is_staff
                and not target_user.is_staff
                and not target_user.is_superuser
            )
            or (user.is_superuser and not target_user.is_superuser)
        )

    def change_role_of_staff(self, user, target_user):
        return (
            (user.is_staff and user == target_user)
            or (user.is_superuser and user == target_user)
            or (user.is_superuser and not target_user.is_superuser)
        )

    def change_role_of_superuser(self, user, target_user):
        return user.is_superuser and (
            user == target_user or not target_user.is_superuser
        )
