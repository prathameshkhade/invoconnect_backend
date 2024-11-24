from django.shortcuts import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from time import timezone
from .models import User
from .permissions import IsAdmin, IsOwnerOrAdmin, IsAuthenticated
from .serializers import UserSerializer


# Create your views here.
class UserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = UserSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == User.UserType.ADMIN:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    @action(detail=False, methods=['post'])
    def register(self, request):
        """Only for business owner registration"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_verification_email.delay(user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        total_users = User.objects.filter(user_type=User.UserType.BUSINESS_OWNER).count()
        active_users = User.objects.filter(
            user_type=User.UserType.BUSINESS_OWNER,
            is_active=True
        ).count()
        recent_registrations = User.objects.filter(
            user_type=User.UserType.BUSINESS_OWNER,
            created_at__gte=timezone.now() - timezone.timedelta(days=30)
        ).count()

        return Response({
            'total_users': total_users,
            'active_users': active_users,
            'recent_registrations': recent_registrations,
            'verification_pending': User.objects.filter(
                user_type=User.UserType.BUSINESS_OWNER,
                is_verified=False
            ).count()
        })
