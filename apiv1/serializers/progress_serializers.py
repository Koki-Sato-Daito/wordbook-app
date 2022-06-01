from rest_framework import serializers

from progress.models import Progress


class ProgressSerializer(serializers.ModelSerializer):
    """
    ユーザが試験を中断した際の進捗データについて以下の責務を持ちます。\n
    モデルマネージャのcreate, deleteメソッドを隠蔽させてserializerから簡単にsaveできるようにする。\n
    バリデーションでユニーク制約を守る、ユーザに通知するメッセージの定義。\n
    Prgressモデルをシリアライズ、デシリアライズできる。\n
    OpenAPIスキーマのリクエスト、レスポンス情報の自動生成\n

    注)デシリアライズする際は必ずcontextにユーザオブジェクトを含めてインスタンス化します。\n
        ProgressSerializer(data=data, context={'user': user})\n
    """
    class Meta:
        model = Progress
        fields = ['id', 'user', 'language', 'pos',
                  'mistake', 'index', 'correct_answer_counter']
        # 認証トークンからユーザをコンテキスト経由で取得するため
        read_only_fields = ('user',)

    def validate(self, validated_data):
        """複合ユニーク制約のバリデーション
        Progressモデルの複合ユニーク制約による例外よりもProgressSerializerのvalidateメソッドの例外として
        クライアント側にメッセージを送ったほうがわかりやすいため実装
        """
        user = self.context['user']
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

    def create(self, validated_data):
        return Progress.objects.create(user=self.context['user'], **validated_data)
