from rest_framework import serializers
from core.models import Kurs, Blatt, Dozent, Kursleiter

class KursleiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kursleiter
        fields = ('email', 'vorname', 'nachname','kurs', 'rolle',)
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}


class KursSerializer(serializers.ModelSerializer):
    kursleiter = KursleiterSerializer(many=True, read_only=True)
    
    class Meta:
        model = Kurs
        fields = '__all__'  # ('kurs', 'beschreibung', 'ref_id', 'dozent', )


class DozentSerializer(serializers.ModelSerializer):
    kurs = KursSerializer(many=True, read_only=True)
    class Meta:
        model = Dozent
        fields = '__all__'


class BlattSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blatt
        fields = ['pk', 'ass_name', 'ass_id', 'kurs']

    def save(self):
        ass_id = self.validated_data['ass_id']
        # if Blatt.objects.get(ass_id=ass_id).exist():
        #     raise serializers.ValidationError({'error': 'Übungsblatt existiert bereits!'})

        blatt = Blatt(ass_name = self.validated_data['ass_name'],
                    ass_id = self.validated_data['ass_id'],
                    kurs=self.validated_data['kurs'],)

        blatt.save()

        return blatt


