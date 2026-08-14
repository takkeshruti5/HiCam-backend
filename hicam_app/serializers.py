from rest_framework import serializers
from .models import User, WorkerProfile , Booking , Review

# ---------------- REGISTER ----------------

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# ---------------- LOGIN ----------------

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class WorkerProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source="user.username")

    class Meta:
        model = WorkerProfile

        fields = [
            "username",
            "speciality",
            "device",
            "price_per_hour",
            "location",
            "bio",
        ]

class BookingSerializer(serializers.ModelSerializer):

    worker_username = serializers.CharField(
        source="worker.user.username",
        read_only=True
    )

    worker_speciality = serializers.CharField(
        source="worker.speciality",
        read_only=True
    )

    class Meta:
        model = Booking
        fields = [
            "id",
            "user",
            "worker",
            "worker_username",
            "worker_speciality",
            "event_type",
            "event_date",
            "start_time",
            "duration",
            "location",
            "message",
            "status",

        ]

        read_only_fields = [
            "user",
            "worker",
            "worker_username",
            "worker_speciality",
        ]
class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = [
            "id",
            "booking",
            "user",
            "worker",
            "rating",
            "comment",
            "created_at",
        ]
        read_only_fields = [
            "user",
            "worker",
            "created_at",
        ]
# ---------------- REVIEW SERIALIZER ----------------

# Converts review data into JSON
class ReviewSerializer(serializers.ModelSerializer):

    # Show client's username
    user_username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    # Show creator's username
    worker_username = serializers.CharField(
        source="worker.user.username",
        read_only=True
    )

    class Meta:

        model = Review

        fields = [
            "id",
            "booking",
            "user",
            "user_username",
            "worker",
            "worker_username",
            "rating",
            "comment",
            "created_at",
        ]

        # These values come from the booking/user
        read_only_fields = [
            "user",
            "worker",
            "user_username",
            "worker_username",
            "created_at",
        ]