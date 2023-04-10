from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler


class RegisterModelSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(label='确认密码',
                                             help_text='确认密码',
                                             max_length=20,
                                             min_length=6,
                                             write_only=True)
    token = serializers.CharField(label='token', help_text='token', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password_confirm', 'email', 'token']
        extra_kwargs = {
            'username': {
                'label': '用户名',
                'help_text': '用户名',
                'min_length': 6,
                'max_length': 20
            },
            'email': {
                'validators': [UniqueValidator(queryset=User.objects.all(), message="邮箱不能重复")],
                'required': True,
                'write_only': True
            },
            'password': {
                'label': '密码',
                'help_text': '密码',
                'write_only': True,
                "max_length": 20,
                "min_length": 6
            },

        }

    def validate(self, attrs):
        if attrs.get('password') == attrs.get('password_confirm'):
            attrs.pop('password_confirm')
            return attrs
        else:
            raise serializers.ValidationError("密码不一致")

    def create(self, validated_data):
        """user = User.objects.create_user(username=validated_data.get('username'),
                                        password=validated_data.get('password'),
                                        email=validated_data.get('email'))"""

        user = User.objects.create_user(**validated_data)
        # 创建payload
        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)
        return user
