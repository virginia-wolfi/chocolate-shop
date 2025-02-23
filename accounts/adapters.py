from allauth.account.adapter import DefaultAccountAdapter


class NoUniqueUsernameAccountAdapter(DefaultAccountAdapter):
    def clean_username(self, username, shallow=False):
        return username
