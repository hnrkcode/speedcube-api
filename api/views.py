from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import calculations, models, serializers


class ChangePassword(APIView):
    """Let user change their own password."""

    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):

        try:
            current_password = request.data["currentPassword"]
            new_password = request.data["newPassword"]
            confirmation = request.data["confirmation"]
        except KeyError:
            return Response({"success": False, "message": "Missing attribute."})

        correct_password = request.user.check_password(current_password)

        if not correct_password:
            return Response({"success": False, "message": "Wrong password."})

        if len(new_password) < 8:
            return Response({"success": False, "message": "Too short password."})

        if new_password != confirmation:
            return Response(
                {"success": False, "message": "Confirmation doesn't match."}
            )

        if correct_password:
            request.user.set_password(new_password)
            request.user.save()

            return Response({"success": True, "message": "Password is now changed."})

        return Response({"success": False, "message": "An error occurred."})


class DeleteUserView(APIView):
    """Let user delete their own account."""

    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):

        try:
            username = self.request.user.username
            password = request.data["password"]
        except KeyError as e:
            return Response({"success": False, "message": e})

        user = authenticate(username=username, password=password)

        if user is not None:
            # Delete user from database.
            models.UserModel.objects.get(id=self.request.user.id).delete()

            return Response(
                {"success": True, "message": "Account successfully deleted."}
            )

        return Response({"success": False, "message": "Wrong password."})


@api_view(["POST"])
def register_view(request):
    """Register new user."""

    if request.method == "POST":

        # Check that all necessary attributes are posted to the server.
        try:
            username = request.data["username"]
            password = request.data["password"]
            confirmation = request.data["confirmation"]
        except KeyError:
            return Response({"success": False, "message": "Missing user attribute."})

        if username == "":
            return Response({"success": False, "message": "Please enter a username."})

        if len(password) < 8:
            return Response(
                {
                    "success": False,
                    "message": "The password must be at least 8 characters long.",
                }
            )

        # Make sure the user entered a password that matches the confirmation.
        if password != confirmation:
            return Response(
                {
                    "success": False,
                    "message": "Password and confirmation password don't match.",
                }
            )

        # Create a new user if the username is available.
        try:
            user = models.UserModel.objects.create_user(
                username=username, password=password
            )
            user.save()
        except IntegrityError:
            return Response({"success": False, "message": "Username already taken."})

        return Response({"success": True, "message": "User created."}, status=201)

    return Response({"success": False})


@api_view(["POST"])
def check_view(request, **kwargs):
    """Check if username or email is taken."""

    def is_taken(key, value):
        users = models.UserModel.objects.all()
        values = [getattr(user, key) for user in users]

        if value not in values:
            return False

        return True

    if request.method == "POST":

        key = kwargs["data"]
        value = request.data[key] if key in request.data else None

        # Check if username is taken.
        if key == "username" and key in request.data:
            taken = is_taken(key, value)

            # Log username check up.
            username = models.CheckUsername.objects.create(username=value)
            username.save()

            return Response({"type": key, "value": value, "taken": taken})

        # Check if email is taken.
        elif key == "email" and key in request.data:
            taken = is_taken(key, value)

            # Log email check up.
            email = models.CheckEmail.objects.create(email=value)
            email.save()

            return Response({"type": key, "value": value, "taken": taken})

    return Response({"Error": "Something went wrong."}, status=400)


class UserView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        if kwargs["id"] == request.user.id:
            queryset = models.UserModel.objects.get(id=kwargs["id"])
            serializer = serializers.UserSerializer(queryset)

            return Response({"success": True, "user": serializer.data})

        return Response({"success": False})

    def patch(self, request, **kwargs):
        if kwargs["id"] == request.user.id:
            queryset = models.UserModel.objects.get(id=kwargs["id"])
            serializer = serializers.UserSerializer(
                queryset, data=request.data, partial=True
            )

            try:
                # if request.data["email"] in [getattr(user, "email") for user in models.UserModel.objects.all()]:
                if request.data["email"] != "" and models.UserModel.objects.filter(
                    email__iexact=request.data["email"]
                ).exclude(id=kwargs["id"]):
                    return Response({"success": False, "email": False})
            except KeyError:
                pass

            if serializer.is_valid():
                serializer.save()
                return Response({"success": True})

        return Response({"success": False})


class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def getInfo(self, user):
        queryset = models.UserModel.objects.get(id=user)
        serializer = serializers.UserSerializer(queryset)

        return serializer.data

    def getTimes(self, user):
        queryset = models.TimeModel.objects.filter(user=user).order_by("-created")
        serializer = serializers.TimeSerializer(queryset, many=True)

        return serializer.data

    def getStats(self, user):

        times = models.TimeModel.objects.filter(user=user).order_by("-created")
        data = {
            "total": len(times),
            "statistics": {
                "best": calculations.best_time(times),
                "worst": calculations.worst_time(times),
                "average": calculations.average_time(times),
                "median": calculations.median_time(times),
            },
        }

        return data

    def get(self, request, **kwargs):

        user_id = kwargs["id"]

        if user_id == self.request.user.id:
            return Response(
                {
                    "success": True,
                    "info": self.getInfo(user_id),
                    "stats": self.getStats(user_id),
                    "times": self.getTimes(user_id),
                }
            )

        return Response({"success": False})


class StatisticView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):

        user = self.request.user.id
        times = models.TimeModel.objects.filter(user=user).order_by("-created")
        length = len(times)
        data = {}

        # Limit statistics to the last number of saved times.
        if kwargs and kwargs["amount"] > 0:
            times = times[: kwargs["amount"]]
            data["last"] = len(times)

        data["total"] = length
        data["statistics"] = {
            "best": calculations.best_time(times),
            "worst": calculations.worst_time(times),
            "average": calculations.average_time(times),
            "median": calculations.median_time(times),
        }

        return Response(data)


class TimeViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.TimeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user_id = self.request.user.id
        queryset = models.TimeModel.objects.filter(user=current_user_id).order_by(
            "-created"
        )

        return queryset
