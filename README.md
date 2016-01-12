django-sns
==========

django-sns

setup:
add "sns" to INSTALLED_APPS

settings:

depending on whether you want to save all notification objects to the database...
SNS_SAVE_NOTIFICATIONS = True/False (default True)

usage:


from sns.signals import sns_signal
from sns.models import Notification

def update_video_asset_status(sender, message, **kwargs):
    pass

sns_signal.connect(update_video_asset_status, sender=Notification, dispatch_uid="update_video_asset_status")

