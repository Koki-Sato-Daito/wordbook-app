from rest_framework import serializers

from progress.models import Progress


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ['id', 'user', 'language', 'pos',
                  'mistake', 'index', 'correct_answer_counter']

    def validate(self, validated_data):
        # 複合ユニーク制約のバリデーション
        user = validated_data.get('user')
        language = validated_data.get('language')
        pos = validated_data.get('pos')
        mistake = validated_data.get('mistake')

        already_exist = Progress.objects.filter(
            user=user, language=language, pos=pos, mistake=mistake)
        if already_exist:
            raise serializers.ValidationError(
                'すでに進捗データが存在します。書き換えるには削除してください。'
                f'Progress(user={user}, language={language}, pos={pos}, mistake={mistake}'
            )
        return validated_data
