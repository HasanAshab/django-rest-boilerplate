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