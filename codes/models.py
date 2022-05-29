from django.db import models
from django.conf import settings
import secrets


def _gen_code(N_DIGITS):
    """
    Generator function for generating verification codes.
    :param N_DIGITS: number of digits in the verification code
    :return: generated verification code
    """
    while True:
        yield str(secrets.randbelow(10 ** N_DIGITS)).rjust(N_DIGITS, '0')


class Code(models.Model):
    """
    Class representing the verification code bound to the user.
    """
    NUMBER_OF_DIGITS = 6  # number of digits in the verification codes
    gen_code = _gen_code(NUMBER_OF_DIGITS)
    number = models.CharField(max_length=NUMBER_OF_DIGITS, blank=True)  # verification code
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)  # user bound to the verification code

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        # generate new_verification code
        self.number = next(Code.gen_code)

        super().save(*args, **kwargs)
