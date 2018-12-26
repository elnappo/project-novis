from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions

from .serializers import UserSerializer


class UserUpdate(UpdateView):
    model = get_user_model()
    fields = ['name']
    template_name = 'profile_change.html'
    success_url = reverse_lazy('profile_change')

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
