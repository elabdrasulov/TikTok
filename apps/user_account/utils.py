from config.celery_ import app
from django.core.mail import send_mail

@app.task
def send_activation_code(user_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    user = User.objects.get(id=user_id)
    user.generate_activation_code()
    user.set_activation_code()
    activation_url = f'http://127.0.0.1:8000/user_account/activate/{user.activation_code}'
    message = f'Activate your account, following this link {activation_url}'
    send_mail("Activate account", message, "tiktok@gmail.com", [user.email, ])

@app.task
def password_confirm(user_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    user = User.objects.get(id=user_id)
    activation_url = f'http://127.0.0.1:8000/user_account/password_confirm/{user.activation_code}'
    message = f"""
    Do you want to change password?
    Confirm password changes: {activation_url}
    """
    send_mail(
        "Please confirm new changes", 
        message, "tiktok@gmail.com", [user.email, ]
    )

   