from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy


class UserUpdate(UpdateView):
    model = get_user_model()
    fields = ['first_name', 'last_name']
    template_name = 'profile_change.html'
    success_url = reverse_lazy('profile_change')

    def get_object(self, queryset=None):
        return self.request.user
