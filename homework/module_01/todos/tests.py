from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
from .models import Todo


class TodoModelTest(TestCase):
    """Test cases for the Todo model"""
    
    def setUp(self):
        """Set up test data"""
        self.todo = Todo.objects.create(
            title="Test TODO",
            description="Test description",
            due_date=date.today() + timedelta(days=7)
        )
    
    def test_todo_creation(self):
        """Test that a TODO can be created successfully"""
        self.assertEqual(self.todo.title, "Test TODO")
        self.assertEqual(self.todo.description, "Test description")
        self.assertFalse(self.todo.resolved)
        self.assertIsNotNone(self.todo.created_at)
        self.assertIsNotNone(self.todo.updated_at)
    
    def test_todo_str_representation(self):
        """Test the string representation of a TODO"""
        self.assertEqual(str(self.todo), "Test TODO")
    
    def test_todo_default_resolved_status(self):
        """Test that a new TODO is not resolved by default"""
        new_todo = Todo.objects.create(title="Another TODO")
        self.assertFalse(new_todo.resolved)
    
    def test_todo_optional_fields(self):
        """Test that description and due_date are optional"""
        minimal_todo = Todo.objects.create(title="Minimal TODO")
        self.assertEqual(minimal_todo.description, "")
        self.assertIsNone(minimal_todo.due_date)
    
    def test_todo_ordering(self):
        """Test that TODOs are ordered by created_at descending"""
        todo1 = Todo.objects.create(title="First")
        todo2 = Todo.objects.create(title="Second")
        todos = Todo.objects.all()
        self.assertEqual(todos[0].title, "Second")
        self.assertEqual(todos[1].title, "First")


class TodoListViewTest(TestCase):
    """Test cases for the TODO list view"""
    
    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.url = reverse('todo_list')
        
        # Create test TODOs
        self.todo1 = Todo.objects.create(
            title="TODO 1",
            description="Description 1",
            due_date=date.today()
        )
        self.todo2 = Todo.objects.create(
            title="TODO 2",
            resolved=True
        )
    
    def test_list_view_status_code(self):
        """Test that the list view returns 200 OK"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_list_view_template(self):
        """Test that the correct template is used"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todos/todo_list.html')
    
    def test_list_view_contains_todos(self):
        """Test that all TODOs are displayed"""
        response = self.client.get(self.url)
        self.assertContains(response, "TODO 1")
        self.assertContains(response, "TODO 2")
    
    def test_list_view_context(self):
        """Test that the context contains the correct data"""
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['todos']), 2)


class TodoCreateViewTest(TestCase):
    """Test cases for the TODO create view"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
        self.url = reverse('todo_create')
    
    def test_create_view_status_code(self):
        """Test that the create view returns 200 OK"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_create_view_template(self):
        """Test that the correct template is used"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todos/todo_form.html')
    
    def test_create_todo_valid_data(self):
        """Test creating a TODO with valid data"""
        data = {
            'title': 'New TODO',
            'description': 'New description',
            'due_date': date.today() + timedelta(days=5)
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(Todo.objects.count(), 1)
        todo = Todo.objects.first()
        self.assertEqual(todo.title, 'New TODO')
        self.assertEqual(todo.description, 'New description')
    
    def test_create_todo_minimal_data(self):
        """Test creating a TODO with only required fields"""
        data = {'title': 'Minimal TODO'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 1)
    
    def test_create_todo_invalid_data(self):
        """Test that creating a TODO without title fails"""
        data = {'description': 'No title'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)  # Stays on form
        self.assertEqual(Todo.objects.count(), 0)


class TodoUpdateViewTest(TestCase):
    """Test cases for the TODO update view"""
    
    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.todo = Todo.objects.create(
            title="Original Title",
            description="Original description"
        )
        self.url = reverse('todo_update', args=[self.todo.pk])
    
    def test_update_view_status_code(self):
        """Test that the update view returns 200 OK"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_update_view_template(self):
        """Test that the correct template is used"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todos/todo_form.html')
    
    def test_update_todo_valid_data(self):
        """Test updating a TODO with valid data"""
        data = {
            'title': 'Updated Title',
            'description': 'Updated description',
            'due_date': date.today() + timedelta(days=3),
            'resolved': True
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Title')
        self.assertEqual(self.todo.description, 'Updated description')
        self.assertTrue(self.todo.resolved)
    
    def test_update_todo_mark_resolved(self):
        """Test marking a TODO as resolved"""
        data = {
            'title': self.todo.title,
            'description': self.todo.description,
            'resolved': True
        }
        response = self.client.post(self.url, data)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.resolved)


class TodoDeleteViewTest(TestCase):
    """Test cases for the TODO delete view"""
    
    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.todo = Todo.objects.create(title="To Delete")
        self.url = reverse('todo_delete', args=[self.todo.pk])
    
    def test_delete_view_status_code(self):
        """Test that the delete view returns 200 OK"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_view_template(self):
        """Test that the correct template is used"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todos/todo_confirm_delete.html')
    
    def test_delete_todo(self):
        """Test deleting a TODO"""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 0)
    
    def test_delete_nonexistent_todo(self):
        """Test attempting to delete a nonexistent TODO"""
        url = reverse('todo_delete', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TodoToggleResolvedTest(TestCase):
    """Test cases for toggling TODO resolved status"""
    
    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.todo = Todo.objects.create(
            title="Toggle Test",
            resolved=False
        )
        self.url = reverse('todo_toggle', args=[self.todo.pk])
    
    def test_toggle_resolved_to_true(self):
        """Test toggling a TODO from unresolved to resolved"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.resolved)
    
    def test_toggle_resolved_to_false(self):
        """Test toggling a TODO from resolved to unresolved"""
        self.todo.resolved = True
        self.todo.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertFalse(self.todo.resolved)
    
    def test_toggle_redirects_to_list(self):
        """Test that toggle redirects to the TODO list"""
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('todo_list'))


class TodoIntegrationTest(TestCase):
    """Integration tests for the complete TODO workflow"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
    
    def test_complete_todo_workflow(self):
        """Test creating, updating, resolving, and deleting a TODO"""
        # Create a TODO
        create_url = reverse('todo_create')
        create_data = {
            'title': 'Workflow Test',
            'description': 'Testing complete workflow',
            'due_date': date.today() + timedelta(days=1)
        }
        response = self.client.post(create_url, create_data)
        self.assertEqual(Todo.objects.count(), 1)
        todo = Todo.objects.first()
        
        # Update the TODO
        update_url = reverse('todo_update', args=[todo.pk])
        update_data = {
            'title': 'Updated Workflow Test',
            'description': create_data['description'],
            'due_date': create_data['due_date'],
            'resolved': False
        }
        response = self.client.post(update_url, update_data)
        todo.refresh_from_db()
        self.assertEqual(todo.title, 'Updated Workflow Test')
        
        # Toggle resolved status
        toggle_url = reverse('todo_toggle', args=[todo.pk])
        response = self.client.get(toggle_url)
        todo.refresh_from_db()
        self.assertTrue(todo.resolved)
        
        # Delete the TODO
        delete_url = reverse('todo_delete', args=[todo.pk])
        response = self.client.post(delete_url)
        self.assertEqual(Todo.objects.count(), 0)
