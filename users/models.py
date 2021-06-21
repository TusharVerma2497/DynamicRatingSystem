from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
import os
from django.dispatch import receiver

class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='default.jpg', upload_to='profile_pics')
    GENDER_CHOICES=(('M','Male'),('F','Female'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = PhoneNumberField(null=True, blank=False, unique=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwargs):
    #     super(profile, self).save(*args, **kwargs)
    #     try:
    #         a=profile.objects.get(id=self.id).image.path
    #     except:
    #         print('not created')
    #     finally:            
    #         super().save()
    #         img=Image.open(self.image.path)
    #         if img.height>300 or img.width>300:
    #             output_size=(300,300)
    #             img.thumbnail(output_size)
    #             img.save(self.image.path)
    #         if a!=profile.objects.get(id=self.id).image.path:
	#             os.remove(a)
# #signals
# def post_user(sender,instance,**kwargs):
#     #instance.profile.save()
#     print(instance.id)
#     p=profile(user_id=instance.id)
#     p.save()

# @receiver(post_save,sender=User)
# def create_profile(sender,instance,created,**kwargs):
#     print('========================================================1')
#     if created:
#         print('========================================================2')
#         profile.object.create_or_get(user=instance)
#         print('========================================================3')

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if kwargs.get('created', True):
        profile.objects.get_or_create(user=instance)
    else:
        p=profile(user_id=instance.id)
        p.save()

# post_save.connect(post_user,sender=User)