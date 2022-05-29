from users.models import CustomUser
from .models import Code
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(signal=post_save, sender=CustomUser)
def post_save_generate_code(sender, instance, created, *args, **kwargs):
    """
    This function is called whenever a new CustomUser instance is created.
    Creates a new Code instance and binds it to the newly created CustomUser.
    :param sender: the model class (CustomUser)
    :param instance: CustomUser instance the .save() method was called upon
    :param created: True if new record was created
    """
    if created:
        # create Code instance and bind the created CustomUser instance to it
        Code.objects.create(user=instance)
        # Model.objects.create() method implicitly saves the created instance to the database

