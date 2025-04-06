from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import time
import threading
from django.db import transaction

# step 1: checking if django signals execute synchronously
@receiver(post_save.send(User))
def user_signal(sender,instance,**kwargs):
    print("Signals received for:",instance.usrename)
    time.sleep(5)  #simulate delay
    print("signals execution completed.")

# creating a user instance will trigger the signals immediately in the same thread
user=User.objects.create(username="testuser")
print("User creation finished.")


# step 2: checking oif django signals run in the same thread


@receiver(post_save, sender=User)
def user_signal(sender, instance, **kwargs):
    print("Signal thread:", threading.current_thread().name)

print("Main thread:", threading.current_thread().name)
user=User.objects.create(username='testuser')


# step 3: checking if django signals run in the same database transaction

@receiver(post_save, sender=User)
def user_signal(sender, instance, **kwargs):
    print("Signal executed before transaction commit.")

with transaction.atomic():
    user = User.objects.create(username='testuser')
    print("User created inside transaction.")

