from rest_framework import serializers


from .models import Country, DXCCEntry, CallSign


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("name", "adif_name", "alpha_2", "alpha_3", "numeric_3")
        read_only = ("name", "adif_name", "alpha_2", "alpha_3", "numeric_3")


class DXCCEntrySerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()

    class Meta:
        model = DXCCEntry
        fields = ("id", "name", "country", "deleted")
        read_only = ("id, ""name", "country", "deleted")


class CallsignSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()
    dxcc = serializers.StringRelatedField()

    class Meta:
        model = CallSign
        fields = ("name", "country", "dxcc", "cq_zone", "itu_zone",
                  "itu_region", "latitude", "longitude")


class MinimalCallsignSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallSign
        fields = ("name",)
