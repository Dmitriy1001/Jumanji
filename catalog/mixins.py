from django.contrib.auth.models import User

from django.shortcuts import redirect


class HasNotCompanyMixin:
    def dispatch(self, *args, **kwargs):
        try:
            self.request.user.company
            return redirect('mycompany_update')
        except User.company.RelatedObjectDoesNotExist:
            return super().dispatch(*args, **kwargs)


class HasCompanyMixin:
    def dispatch(self, *args, **kwargs):
        try:
            self.request.user.company
            return super().dispatch(*args, **kwargs)
        except User.company.RelatedObjectDoesNotExist:
            return redirect('mycompany_letsstart')


class HasNotResumeMixin:
    def dispatch(self, *args, **kwargs):
        try:
            self.request.user.resume
            return redirect('myresume_update')
        except User.resume.RelatedObjectDoesNotExist:
            return super().dispatch(*args, **kwargs)


class HasResumeMixin:
    def dispatch(self, *args, **kwargs):
        try:
            self.request.user.resume
            return super().dispatch(*args, **kwargs)
        except User.resume.RelatedObjectDoesNotExist:
            return redirect('myresume_letsstart')
