from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)

from .models import Sensor
from .serializers import (
    MeasurementSerializer,
    SensorDetailSerializer,
    SensorSerializer,
)


class SensorListCreateView(ListCreateAPIView):
    queryset = Sensor.objects.order_by('id')
    serializer_class = SensorSerializer
    pagination_class = None


class SensorDetailView(RetrieveUpdateAPIView):
    queryset = Sensor.objects.prefetch_related('measurements')
    serializer_class = SensorDetailSerializer


class MeasurementCreateView(CreateAPIView):
    serializer_class = MeasurementSerializer
