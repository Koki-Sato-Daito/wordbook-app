from djoser.serializers import TokenSerializer


class TokenSerializer(TokenSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = self.context['user']
        return response
