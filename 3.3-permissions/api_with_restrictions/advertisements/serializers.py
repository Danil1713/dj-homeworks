from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
        ]


class AdvertisementSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = [
            'id',
            'title',
            'description',
            'creator',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        if self.instance is None:
            creator = self.context['request'].user
            current_status = AdvertisementStatusChoices.OPEN
        else:
            creator = self.instance.creator
            current_status = self.instance.status

        target_status = data.get('status', current_status)

        if target_status == AdvertisementStatusChoices.OPEN:
            open_advertisements = Advertisement.objects.filter(
                creator=creator,
                status=AdvertisementStatusChoices.OPEN,
            )

            if self.instance is not None:
                open_advertisements = open_advertisements.exclude(
                    pk=self.instance.pk,
                )

            if open_advertisements.count() >= 10:
                raise serializers.ValidationError({
                    'status': (
                        'У пользователя не может быть больше '
                        '10 открытых объявлений.'
                    ),
                })

        return data