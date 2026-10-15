from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'title', 'start_time', 'end_time', 'created_at']

    def validate(self, data):
        start = data.get('start_time')
        end = data.get('end_time')

        if start >= end:
            raise serializers.ValidationError('O horário de início deve ser antes do horário de término.')

        user = self.context['request'].user

        conflicts = Appointment.objects.filter(
            user=user,
            start_time__lt=end,
            end_time__gt=start,
        )

        if self.instance:
            conflicts = conflicts.exclude(id=self.instance.id)

        if conflicts.exists():
            raise serializers.ValidationError('Já existe um agendamento nesse horário.')

        return data