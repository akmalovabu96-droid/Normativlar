# accounts/models.py yoki alohida signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):

    if created:
        print("🔔 SIGNAL ISHLADI: Yangi user yaratildi!")

        try:
            group = Group.objects.get(name='User')
            instance.groups.add(group)

            print(f"✅ {instance.username} 'User' groupga qo'shildi")

        except Group.DoesNotExist:
            print("❌ 'User' group topilmadi")

# from .models import Profile
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         from .models import Profile
#         Profile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()