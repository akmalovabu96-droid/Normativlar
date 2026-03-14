from django.core.mail import send_mail

def send_simple_email():
    send_mail(
        subject="Django email sinovi",
        message="Whenever I test my game project, an unknown bug appears.",
        from_email="akmalovabu96@gmail.com",
        recipient_list=["a39307503@gmail.com", "gafurjonovdavronbek@gmail.com", "freddyfazber040@gmail.com", "giyosoripov4@gmail.com"],
        fail_silently=False,
    )
