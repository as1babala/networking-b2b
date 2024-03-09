from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
import six
from core.models import CustomUser
user = CustomUser



class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp)  + six.text_type(user.is_active)
        )

account_activation_token = AccountActivationTokenGenerator()


def generate_confirmation_token(user):
    token_generator = PasswordResetTokenGenerator()
    return token_generator.make_token(user)
