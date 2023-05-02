from django.dispatch import receiver
from django.db.models import signals
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from acc_auth.models import MyUser, Profile
from django.db.models.signals import pre_save, post_save

@receiver(post_save,sender=MyUser)
def dependency_Collaborators_creator(sender,instance,*args,**kwargs):
    
    if (hasattr(instance, 'profile')) == False:
        print('profile does not exist')
        Profile.objects.create(user=instance)
    