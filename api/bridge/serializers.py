from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from .models import *


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Report
        fields = ['id',
                  'username',
                  'content_type',
                  'content_id',
                  'content_text',
                  'time',
                  'reason',
                  'reporter'
                  ]


class DynamicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dynamic
        fields = ['id',
                  'time',
                  'username',
                  'discuss',
                  'comment ', ]


class CommentSerializerAlter(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'notshow',
                  'replyto', 'discuss', 'text', 'commenter', 'time']


class CommentSerializer(serializers.ModelSerializer):
    replyto = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'notshow',
                  'replyto', 'discuss', 'text', 'commenter', 'time']


class DiscussWithTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = DiscussWithTag
        fields = ['id',
                  'tag',
                  'text',
                  'time',
                  'starter',
                  'isshow',
                  'title',
                  ]


class DiscussSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        qs = Comment.objects.filter(notshow=False, discuss=obj)
        serializer = CommentSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Discuss
        fields = ['id', 'title', 'starter',
                  'text', 'isshow', 'time', 'tags', 'comments']


class ChatMessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'isshow_sender',
                  'isshow_receiver', 'isread_receiver', 'text', 'receiver', 'time']


class NotifySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notify
        fields = ['username', 'isread', 'from_who',
                  'time', 'event_type', 'discuss_title']


class UserInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['id', 'username', 'birthday', 'avatar', 'introduce', 'email']
        # lookup_field = 'owner'
        # extra_kwargs = {
        #     'url': {'lookup_field': 'username'}
        # }


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'password', 'email', 'is_superuser']
        # lookup_field = 'username'
        extra_kwargs = {

            'url': {'lookup_field': 'username'}
        }
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


# owner = serializers.ReadOnlyField(source='owner.username')
# 外链字段
    # snippets = serializers.HyperlinkedRelatedField(
    #     many=True, view_name='snippet-detail', read_only=True)
