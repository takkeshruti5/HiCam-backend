from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate

# Import models
from .models import User, WorkerProfile, Booking, Review

# Import serializers
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    WorkerProfileSerializer,
    BookingSerializer,
    ReviewSerializer
)


# ---------------- REGISTER ----------------

# API used to create a new user
class RegisterView(generics.CreateAPIView):

    # User records this API works with
    queryset = User.objects.all()

    # Handles username, email and password
    serializer_class = RegisterSerializer


# ---------------- LOGIN ----------------

# API used for user login
class LoginView(APIView):

    def post(self, request):

        # Validate login data
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            # Check username and password
            user = authenticate(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"]
            )

            # Login successful
            if user:
                return Response({
                    "message": "Login successful",
                    "username": user.username
                })

            # Wrong login details
            return Response(
                {"message": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ---------------- WORKER PROFILE ----------------

# API used to create worker profile
class WorkerProfileCreateView(APIView):

    def post(self, request):

        # Get username from frontend
        username = request.data.get("username")

        try:
            # Find the user
            user = User.objects.get(username=username)

        except User.DoesNotExist:

            return Response(
                {"message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validate profile data
        serializer = WorkerProfileSerializer(
            data=request.data
        )

        if serializer.is_valid():

            # Connect profile with user
            serializer.save(user=user)

            return Response(
                {"message": "Worker Profile Created"},
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ---------------- ALL WORKERS ----------------

# API used to show all creators
class WorkerListView(generics.ListAPIView):

    queryset = WorkerProfile.objects.all()

    serializer_class = WorkerProfileSerializer


# ---------------- BOOKING ----------------

# API used to create a booking
class BookingCreateView(APIView):

    def post(self, request):

        # Get client and worker usernames
        username = request.data.get("username")
        worker_username = request.data.get("worker_username")

        try:

            # Find client
            user = User.objects.get(
                username=username
            )

            # Find creator profile
            worker = WorkerProfile.objects.get(
                user__username=worker_username
            )

        except User.DoesNotExist:

            return Response(
                {"message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except WorkerProfile.DoesNotExist:

            return Response(
                {"message": "Worker not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validate booking data
        serializer = BookingSerializer(
            data=request.data
        )

        if serializer.is_valid():

            # Save booking with client and creator
            serializer.save(
                user=user,
                worker=worker
            )

            return Response(
                {"message": "Booking created successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ---------------- MY BOOKINGS ----------------

# API used to show client's bookings
class MyBookingsView(APIView):

    def get(self, request):

        # Get username from URL
        username = request.query_params.get("username")

        try:

            # Find client
            user = User.objects.get(
                username=username
            )

        except User.DoesNotExist:

            return Response(
                {"message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get bookings made by this client
        bookings = Booking.objects.filter(
            user=user
        )

        serializer = BookingSerializer(
            bookings,
            many=True
        )

        return Response(serializer.data)


# ---------------- CREATOR BOOKINGS ----------------

# API used to show bookings received by creator
class CreatorBookingsView(APIView):

    def get(self, request):

        # Get creator username
        username = request.query_params.get("username")

        try:

            # Find creator profile
            worker = WorkerProfile.objects.get(
                user__username=username
            )

        except WorkerProfile.DoesNotExist:

            return Response(
                {"message": "Worker profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get bookings for this creator
        bookings = Booking.objects.filter(
            worker=worker
        )

        serializer = BookingSerializer(
            bookings,
            many=True
        )

        return Response(serializer.data)


# ---------------- UPDATE BOOKING STATUS ----------------

# API used to accept, reject or complete booking
class BookingStatusView(APIView):

    def patch(self, request, booking_id):

        try:

            # Find booking
            booking = Booking.objects.get(
                id=booking_id
            )

        except Booking.DoesNotExist:

            return Response(
                {"message": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get new status
        new_status = request.data.get("status")

        # Check valid status
        if new_status not in [
            "Accepted",
            "Rejected",
            "Completed"
        ]:

            return Response(
                {"message": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update booking status
        booking.status = new_status
        booking.save()

        return Response({
            "message": f"Booking {new_status.lower()}",
            "status": booking.status
        })


# ---------------- CHECK WORKER PROFILE ----------------

# API used to check if user already has creator profile
class WorkerProfileCheckView(APIView):

    def get(self, request):

        # Get username from URL
        username = request.query_params.get(
            "username"
        )

        try:

            # Find existing profile
            profile = WorkerProfile.objects.get(
                user__username=username
            )

        except WorkerProfile.DoesNotExist:

            # Profile does not exist
            return Response({
                "exists": False
            })

        # Convert profile to JSON
        serializer = WorkerProfileSerializer(
            profile
        )

        return Response({
            "exists": True,
            "profile": serializer.data
        })


# ---------------- CREATE REVIEW ----------------

# API used by client to submit a review
class ReviewCreateView(APIView):

    def post(self, request):

        # Get review details
        username = request.data.get("username")
        booking_id = request.data.get("booking")
        rating = request.data.get("rating")
        comment = request.data.get("comment")

        try:

            # Find client
            user = User.objects.get(
                username=username
            )

        except User.DoesNotExist:

            return Response(
                {"message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:

            # Find client's booking
            booking = Booking.objects.get(
                id=booking_id,
                user=user
            )

        except Booking.DoesNotExist:

            return Response(
                {"message": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Review only after event is completed
        if booking.status != "Completed":

            return Response(
                {
                    "message":
                    "You can review only completed bookings"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Stop duplicate reviews
        if Review.objects.filter(
            booking=booking
        ).exists():

            return Response(
                {
                    "message":
                    "You already reviewed this booking"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check rating value
        try:
            rating = int(rating)

        except (TypeError, ValueError):

            return Response(
                {"message": "Invalid rating"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Rating must be between 1 and 5
        if rating < 1 or rating > 5:

            return Response(
                {
                    "message":
                    "Rating must be between 1 and 5"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save review
        review = Review.objects.create(
            booking=booking,
            user=user,
            worker=booking.worker,
            rating=rating,
            comment=comment
        )

        return Response(
            {
                "message":
                "Review submitted successfully",
                "review_id": review.id
            },
            status=status.HTTP_201_CREATED
        )


# ---------------- WORKER REVIEWS ----------------

# API used to show reviews received by creator
class WorkerReviewsView(APIView):

    def get(self, request):

        # Get creator username
        username = request.query_params.get(
            "username"
        )

        try:

            # Find creator profile
            worker = WorkerProfile.objects.get(
                user__username=username
            )

        except WorkerProfile.DoesNotExist:

            return Response(
                {"message": "Worker not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get all reviews for this creator
        reviews = Review.objects.filter(
            worker=worker
        ).order_by("-created_at")

        # Convert reviews to JSON
        serializer = ReviewSerializer(
            reviews,
            many=True
        )

        return Response(serializer.data)