from django.db import models
from django.conf import settings
import random


def _gen_code(N_DIGITS):
    while True:
        yield "".join(str(random.randint(0, 9)) for i in range(N_DIGITS))


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
