from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer
from .models import UserValidation


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    fields = ['name', 'display_name', 'address', 'country', 'bio']
    template_name = 'profile_change.html'
    success_url = reverse_lazy('profile_change')

    def get_object(self, queryset=None):
        return self.request.user


class UserSocialUpdate(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    fields = ['twitter', 'youtube', 'facebook', 'flickr', 'vimeo', 'skype', 'matrix', 'jabber']
    template_name = 'social_change.html'
    success_url = reverse_lazy('profile_social_change')

    def get_object(self, queryset=None):
        return self.request.user


class CurrentUserAPIView(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    lookup_field = None
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        print(request.user.validated)
        partial = kwargs.pop('partial', False)
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class UserValidationView(LoginRequiredMixin, CreateView):
    template_name = "validation.html"
    model = UserValidation
    fields = ['validation_file', 'validation_comment']
    success_url = reverse_lazy('profile_validation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['user_validation'] = UserValidation.objects.get(user=self.request.user)
        except UserValidation.DoesNotExist:
            context['user_validation'] = None
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return super().form_valid(form)


class APIKeyView(LoginRequiredMixin, DetailView):
    model = Token
    template_name = 'profile_api.html'

    def get_object(self, queryset=None):
        return self.model.objects.get_or_create(user=self.request.user, defaults={"user": self.request.user})[0]
