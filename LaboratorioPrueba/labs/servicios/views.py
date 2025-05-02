from rest_framework import viewsets, generics, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
import requests
from .models import Usuario, Servicio, Trabajador, Contratacion, Calificacion, Chat, Mensaje
from .serializers import (
    UsuarioSerializer, ServicioSerializer, TrabajadorSerializer,
    ContratacionSerializer, CalificacionSerializer, ChatSerializer, MensajeSerializer
)

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [IsAuthenticated]

class TrabajadorViewSet(viewsets.ModelViewSet):
    queryset = Trabajador.objects.all()
    serializer_class = TrabajadorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['usuario__username', 'servicio__nombre']
    ordering_fields = ['calificacion_promedio']

    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        trabajador = self.get_object()
        calificaciones = Calificacion.objects.filter(trabajador=trabajador)
        stats = {
            'total_servicios': calificaciones.count(),
            'calificacion_promedio': calificaciones.aggregate(Avg('estrellas'))['estrellas__avg'] or 0,
            'servicios_5_estrellas': calificaciones.filter(estrellas=5).count()
        }
        return Response(stats)

class ContratacionViewSet(viewsets.ModelViewSet):
    queryset = Contratacion.objects.all()
    serializer_class = ContratacionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['fecha_solicitud', 'estado']

    @action(detail=True, methods=['get'])
    def convertir_a_dolares(self, request, pk=None):
        contratacion = self.get_object()
        try:
            response = requests.get('https://dolarapi.com/v1/dolares/blue')
            data = response.json()
            valor_dolar = float(data['venta'])
            monto_dolares = float(contratacion.monto) / valor_dolar
            return Response({
                'monto_pesos': contratacion.monto,
                'valor_dolar': valor_dolar,
                'monto_dolares': round(monto_dolares, 2)
            })
        except Exception as e:
            return Response(
                {'error': 'Error al obtener cotización del dólar'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        calificacion = serializer.save()
        calificacion.trabajador.actualizar_calificacion()

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.es_trabajador:
            return Chat.objects.filter(trabajador__usuario=self.request.user)
        return Chat.objects.filter(cliente=self.request.user)

class MensajeViewSet(viewsets.ModelViewSet):
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(emisor=self.request.user)


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroForm  # You'll need to create this form

def home(request):
    context = {
        'servicios': Servicio.objects.all()[:5],
        'trabajadores_destacados': Trabajador.objects.annotate(
            avg_rating=Avg('calificacion__estrellas')
        ).filter(avg_rating__gte=4)[:5],
        'ultimas_calificaciones': Calificacion.objects.order_by('-fecha')[:5]
    }
    return render(request, 'servicios/home.html', context)

@login_required
def perfil_trabajador(request, trabajador_id):
    trabajador = get_object_or_404(Trabajador, id=trabajador_id)
    context = {
        'trabajador': trabajador,
        'calificaciones': trabajador.calificacion_set.all().order_by('-fecha')
    }
    return render(request, 'servicios/perfil_trabajador.html', context)


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'servicios/registro.html', {'form': form})