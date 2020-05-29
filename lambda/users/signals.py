from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver

NORMAL_USER_GROUP = Group.objects.get(pk=1)


@receiver(post_save, sender=User)
def post_user_save(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(NORMAL_USER_GROUP)
        instance.save()
