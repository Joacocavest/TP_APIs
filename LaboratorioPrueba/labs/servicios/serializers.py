from rest_framework import serializers
from .models import Usuario, Servicio, Trabajador, Contratacion, Calificacion, Chat, Mensaje

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'email', 'es_trabajador', 'direccion', 'telefono')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'

class TrabajadorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    servicio = ServicioSerializer()
    
    class Meta:
        model = Trabajador
        fields = '__all__'

class ContratacionSerializer(serializers.ModelSerializer):
    monto_dolares = serializers.SerializerMethodField()

    class Meta:
        model = Contratacion
        fields = '__all__'

    def get_monto_dolares(self, obj):
        return obj.get_monto_dolares()

    def validate_direccion_servicio(self, value):
        if self.instance and self.instance.estado != 'PENDIENTE':
            raise serializers.ValidationError("No se puede modificar la dirección una vez iniciado el servicio")
        return value

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = '__all__'

    def validate(self, data):
        if data['contratacion'].estado != 'COMPLETADO':
            raise serializers.ValidationError("Solo se puede calificar servicios completados")
        return data

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensaje
        fields = '__all__'