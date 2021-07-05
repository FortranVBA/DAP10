"""Project OC DAP 10 - Account serializers file."""

from account.models import Person
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer used for registration."""

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        """Serializer meta properties."""

        model = Person
        fields = ("username", "password")

    def create(self, validated_data):
        """Register a person as user."""
        person = Person.objects.create(
            username=validated_data["username"],
        )

        person.set_password(validated_data["password"])
        person.save()

        return person


class PersonSerializer(serializers.ModelSerializer):
    """Person serializer."""

    class Meta:
        """Serializer meta properties."""

        model = Person
        fields = ["id", "username"]
