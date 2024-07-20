from djoser import email
from djoser.conf import settings

class AwesomeActivationEmail(email.ActivationEmail):

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()
        context["domain"] = settings.CUSTOM_DOMAIN
        context["username"] = context.get("user").full_name
        return context
    

class ActivateConfirmation(email.ConfirmationEmail):

    def get_context_data(self):
        context = super().get_context_data()
        context["username"] = context.get("user").full_name
        return context


class PasswordResetEmail(email.PasswordResetEmail):

    def get_context_data(self):
        context = super().get_context_data()
        context["domain"] = settings.CUSTOM_DOMAIN
        context["username"] = context.get("user").full_name
        return context

class PasswordChangedConfirmationEmail(email.PasswordChangedConfirmationEmail):

    def get_context_data(self):
        context = super().get_context_data()
        context["domain"] = settings.CUSTOM_DOMAIN
        context["username"] = context.get("user").full_name
        return context