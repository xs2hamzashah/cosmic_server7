from django.core.mail import send_mail

from cosmic_server7.settings import EMAIL_HOST_USER


def send_approval_notification(seller):
    subject = 'Your Solar Solution Has Been Approved'
    message = 'Congratulations! Your solar solution has been approved and is now live on the platform.'
    recipient_list = [seller.email]
    # recipient_list = []

    send_mail(subject, message, EMAIL_HOST_USER, recipient_list)
