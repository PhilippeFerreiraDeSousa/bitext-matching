import graphene
from graphene_django_extras.subscription import Subscription
from .serializers import UserSerializer, GroupSerializer


class AlignementInfoSubscription(Subscription):
    class Meta:
        serializer_class = UserSerializer
        stream = 'alignment_info'
        description = 'Alignment Info Subscription'
