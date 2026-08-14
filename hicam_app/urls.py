from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    WorkerProfileCreateView,
    WorkerListView,
    BookingCreateView,
    MyBookingsView,
    CreatorBookingsView,
    BookingStatusView,
    WorkerProfileCheckView,
    ReviewCreateView,
    WorkerReviewsView,
)


urlpatterns = [

    path(
        "register/",
        RegisterView.as_view(),
        name="register"
    ),

    path(
        "login/",
        LoginView.as_view(),
        name="login"
    ),

    path(
        "worker-profile/",
        WorkerProfileCreateView.as_view(),
        name="worker-profile"
    ),

    path(
        "workers/",
        WorkerListView.as_view(),
        name="workers"
    ),

    path(
        "bookings/",
        BookingCreateView.as_view(),
        name="booking"
    ),

    path(
        "my-bookings/",
        MyBookingsView.as_view(),
        name="my-bookings"
    ),

    path(
        "creator-bookings/",
        CreatorBookingsView.as_view(),
        name="creator-bookings"
    ),

    path(
        "bookings/<int:booking_id>/status/",
        BookingStatusView.as_view(),
        name="booking-status"
    ),

    path(
        "worker-profile/check/",
        WorkerProfileCheckView.as_view(),
        name="worker-profile-check"
    ),

    path(
        "reviews/",
        ReviewCreateView.as_view(),
        name="review-create"
    ),

    path(
        "worker-reviews/",
        WorkerReviewsView.as_view(),
        name="worker-reviews"
    ),
]