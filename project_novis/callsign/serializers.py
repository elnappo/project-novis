from rest_framework import serializers


from .models import Country, DXCCEntry, CallSign, DMRID, CallSignPrefix


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name", "adif_name", "alpha_2", "alpha_3", "numeric_3")
        read_only = ("id", "name", "adif_name", "alpha_2", "alpha_3", "numeric_3")


class DXCCEntrySerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()

    class Meta:
        model = DXCCEntry
        fields = ("id", "name", "country", "deleted")
        read_only = ("id", "name", "country", "deleted")


class DMRIDSerializer(serializers.ModelSerializer):
    callsign = serializers.StringRelatedField()
    brandmeister_profile_url = serializers.URLField(read_only=True)

    class Meta:
        model = DMRID
        fields = ("name", "callsign", "brandmeister_profile_url", "active", "issued")
        read_only = ("name", "callsign", "brandmeister_profile_url", "active", "issued")


class CallsignSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()
    dxcc = serializers.StringRelatedField()
    dmr_ids = serializers.StringRelatedField(many=True, required=False, read_only=True)
    prefix = serializers.StringRelatedField(read_only=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.set_default_meta_data()
        instance.save()
        return instance

    class Meta:
        model = CallSign
        fields = ("name", "prefix", "country", "dxcc", "cq_zone", "itu_zone",
                  "itu_region", "latitude", "longitude", "type", "dstar", "dmr_ids", "created_by")


class CallSignPrefixSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()

    class Meta:
        model = CallSignPrefix
        fields = ("name", "country", "dxcc", "cq_zone", "itu_zone", "itu_region", "continent", "latitude", "longitude", "utc_offset", "type")
        read_only = ("name", "country", "dxcc", "cq_zone", "itu_zone", "itu_region", "continent", "latitude", "longitude", "utc_offset", "type")
