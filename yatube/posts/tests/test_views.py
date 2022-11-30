from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Post, Group

User = get_user_model()


class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='UserHasNoName')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание группы',
        )
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user,
            group=cls.group,
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем авторизованный клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse(
                'posts:group_posts', kwargs={'slug': 'test-slug'}
            ),
            'posts/profile.html': reverse(
                'posts:profile', kwargs={'username': self.user.username}
            ),
            'posts/post_detail.html': reverse(
                'posts:post_detail', kwargs={'post_id': self.post.pk}
            ),
            'posts/create_post.html': reverse(
                'posts:post_edit', kwargs={'post_id': self.post.pk}
            ),
            'posts/create_post.html': reverse('posts:post_create'),
        }
        # Проверяем, что при обращении к name вызывается соотв HTML-шаблон
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        group_title_0 = first_object.group.title
        post_text_0 = first_object.text
        group_slug_0 = first_object.group.slug
        self.assertEqual(group_title_0, self.group.title)
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(group_slug_0, self.group.slug)

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:group_posts', kwargs={'slug': 'test-slug'}))
        first_object = response.context['page_obj'][0]
        post_group_0 = first_object.group.title
        self.assertEqual(post_group_0, PostsPagesTests.group.title)
        self.assertEqual(len(response.context['page_obj']), 1)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': self.user.username}))
        first_object = response.context['page_obj'][0]
        post_group_0 = first_object.author
        self.assertEqual(post_group_0, PostsPagesTests.post.author)
        self.assertEqual(len(response.context['page_obj']), 1)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:post_detail', kwargs={'post_id': self.post.pk}))
        first_object = response.context['post']
        self.assertEqual(first_object.pk, PostsPagesTests.post.pk)

    def test_post_create_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='UserHasNoName')
        cls.group1 = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание группы',
        )
        cls.post1 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост1',
            group=cls.group1
        )
        cls.post2 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост2',
            group=cls.group1
        )
        cls.post3 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост3',
            group=cls.group1
        )
        cls.post4 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост4',
            group=cls.group1
        )
        cls.post5 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост5',
            group=cls.group1
        )
        cls.post6 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост6',
            group=cls.group1
        )
        cls.post7 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост7',
            group=cls.group1
        )
        cls.post8 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост8',
            group=cls.group1
        )
        cls.post9 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост9',
            group=cls.group1
        )
        cls.post10 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост10',
            group=cls.group1
        )
        cls.post11 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост11',
            group=cls.group1
        )
        cls.post12 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост12',
            group=cls.group1
        )
        cls.post13 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост13',
            group=cls.group1
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_page_contains_ten_records(self):
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_three_records(self):
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_first_page_group_list_contains_ten_records(self):
        response = self.client.get(reverse(
            'posts:group_posts', kwargs={'slug': 'test_slug'}))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_first_page_profile_contains_ten_records(self):
        response = self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': 'UserHasNoName'}))
        self.assertEqual(len(response.context['page_obj']), 10)
