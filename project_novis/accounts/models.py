from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import PermissionDenied
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None

    email = models.EmailField(_('Email address'), unique=True, db_index=True)
    name = models.CharField(_('Name'), max_length=200, blank=True, help_text="Your real name, used only for user/callsign validation.")
    display_name = models.CharField(_('Display name'), max_length=200, blank=True, help_text="Your name, shown on your callsign page.")
    bio = models.TextField(blank=True)

    # location
    address = models.TextField(max_length=512, blank=True)
    country = models.ForeignKey("callsign.Country", on_delete=models.SET_NULL, blank=True, null=True)
    # TODO(elnappo) Set when address/country changed
    location = models.PointField(null=True, blank=True)

    # social
    twitter = models.CharField(max_length=64, blank=True, help_text="Twitter username without @")
    youtube = models.CharField("YouTube", max_length=64, blank=True, help_text="YouTube channel ID")
    facebook = models.CharField(max_length=64, blank=True, help_text="Facebook username")
    flickr = models.CharField(max_length=64, blank=True, help_text="flickr username")
    vimeo = models.CharField(max_length=64, blank=True, help_text="Vimeo username")
    skype = models.CharField(max_length=64, blank=True)
    matrix = models.CharField(max_length=128, blank=True)
    jabber = models.CharField(max_length=128, blank=True)

    # default callsign?

    created = models.DateTimeField(_("Created"), auto_now_add=True)
    modified = models.DateTimeField(_("Modified"), auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    @property
    def validated(self) -> bool:
        if hasattr(self, "uservalidation"):
            return self.uservalidation.approved
        else:
            return False

    # TODO(elnappo) Move to app?
    def claim_call_sign(self, callsign):
        if not callsign.owner:
            callsign.owner = self
            callsign.save()
        else:
            raise PermissionDenied("Another user already owns this call sign!")

    @property
    def twitter_profile_url(self) -> str:
        return f"https://twitter.com/{ self.twitter }"

    @property
    def youtube_profile_url(self) -> str:
        return f"https://www.youtube.com/channel/{ self.youtube }"

    @property
    def facebook_profile_url(self) -> str:
        return f"https://www.facebook.com/{ self.facebook }"

    @property
    def flickr_profile_url(self) -> str:
        return f"https://www.flickr.com/photos/{ self.flickr }"

    @property
    def vimeo_profile_url(self) -> str:
        return f"https://vimeo.com/{ self.vimeo }"

    @property
    def jabber_link(self) -> str:
        return f"xmpp:{ self.jabber }"

    @property
    def skype_link(self) -> str:
        return f"skype:{ self.skype }"


class UserValidation(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name="approved_from", blank=True, null=True)
    validation_comment = models.TextField(blank=True)
    validation_file = models.FileField(upload_to='user_validation/', blank=True, null=True)

    created = models.DateTimeField(_("Created"), auto_now_add=True)
    modified = models.DateTimeField(_("Modified"), auto_now=True)
