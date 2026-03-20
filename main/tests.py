import pytest
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import resolve, reverse

from .forms import ContactForm
from .models import Contact, Project


@pytest.fixture
def project_data():
    return {
        'title': 'Portfolio Site',
        'description': 'A clean portfolio website built with Django.',
        'link': 'https://example.com/project',
    }


@pytest.fixture
def contact_data():
    return {
        'name': 'Avery Chen',
        'email': 'avery@example.com',
        'message': 'Hello, I would like to collaborate.',
    }


@pytest.fixture
def project(project_data):
    return Project.objects.create(**project_data)


@pytest.fixture
def contact(contact_data):
    return Contact.objects.create(**contact_data)


@pytest.fixture
def superuser(db):
    User = get_user_model()
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123',
    )


@pytest.mark.django_db
class TestModels:
    def test_project_creation_and_fields(self, project, project_data):
        assert project.title == project_data['title']
        assert project.description == project_data['description']
        assert project.link == project_data['link']

    def test_contact_creation_and_fields(self, contact, contact_data):
        assert contact.name == contact_data['name']
        assert contact.email == contact_data['email']
        assert contact.message == contact_data['message']
        assert contact.created_at is not None

    def test_project_str(self, project):
        assert str(project) == project.title

    def test_contact_str(self, contact, contact_data):
        assert str(contact) == f"{contact_data['name']} ({contact_data['email']})"


@pytest.mark.django_db
class TestViews:
    def test_homepage_loads(self, client):
        response = client.get(reverse('main:home'))
        assert response.status_code == 200

    def test_homepage_template_used(self, client):
        response = client.get(reverse('main:home'))
        assert 'index.html' in [t.name for t in response.templates]

    def test_projects_in_context(self, client, project):
        response = client.get(reverse('main:home'))
        assert 'projects' in response.context
        assert project in response.context['projects']


@pytest.mark.django_db
class TestUrls:
    def test_home_url_resolves(self):
        resolver = resolve('/')
        assert resolver.view_name == 'main:home'


@pytest.mark.django_db
class TestForms:
    def test_valid_contact_form(self, contact_data):
        form = ContactForm(data=contact_data)
        assert form.is_valid()

    @pytest.mark.parametrize(
        'data',
        [
            {'name': '', 'email': '', 'message': ''},
            {'name': 'Name', 'email': 'not-an-email', 'message': 'Hi'},
        ],
    )
    def test_invalid_contact_form(self, data):
        form = ContactForm(data=data)
        assert not form.is_valid()


@pytest.mark.django_db
class TestDatabase:
    def test_contact_form_saves_to_db(self, client, contact_data):
        response = client.post(reverse('main:home'), data=contact_data)
        assert response.status_code == 302
        assert Contact.objects.filter(email=contact_data['email']).exists()


@pytest.mark.django_db
class TestIntegration:
    def test_user_submits_contact_form(self, client, contact_data):
        response = client.post(reverse('main:home'), data=contact_data, follow=True)
        assert response.status_code == 200
        assert Contact.objects.filter(email=contact_data['email']).exists()
        messages = list(response.context['messages'])
        assert any('Thanks for reaching out' in str(message) for message in messages)


@pytest.mark.django_db
class TestAdmin:
    def test_models_registered(self):
        assert Project in admin.site._registry
        assert Contact in admin.site._registry

    def test_admin_login(self, client, superuser):
        logged_in = client.login(username='admin', password='adminpass123')
        assert logged_in
        response = client.get('/admin/')
        assert response.status_code == 200
