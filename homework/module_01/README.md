# Django TODO Application

A simple TODO application built with Django that allows you to create, edit, delete, and manage TODOs with due dates.

## Features

- ✅ Create new TODOs with title, description, and due date
- ✏️ Edit existing TODOs
- 🗑️ Delete TODOs
- ✔️ Mark TODOs as resolved/unresolved
- 📅 Assign due dates to TODOs
- 📊 View all TODOs in a clean, organized list
- 🎨 User-friendly interface with color-coded status

## Setup Instructions

### Prerequisites

- Python 3.x installed on your system

### Installation

1. The virtual environment is already set up in the `venv` folder.

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

3. Django is already installed. If you need to reinstall:
   ```bash
   pip install django
   ```

4. The database migrations have already been applied.

### Running the Application

1. Make sure you're in the `module_01` directory and the virtual environment is activated:
   ```bash
   source venv/bin/activate
   ```

2. Start the development server:
   ```bash
   python manage.py runserver
   ```

3. Open your web browser and navigate to:
   ```
   http://127.0.0.1:8000/
   ```

### Running Tests

The application includes comprehensive unit tests covering all main functionality. To run the tests:

```bash
# Activate virtual environment if not already activated
source venv/bin/activate

# Run all tests
python manage.py test todos

# Run tests with verbose output
python manage.py test todos -v 2

# Run a specific test class
python manage.py test todos.tests.TodoModelTest
```

**Test Coverage:**
- ✅ 26 unit tests covering:
  - Todo model creation and validation
  - List, create, update, and delete views
  - Toggle resolved functionality
  - Form validation
  - Complete integration workflow
  - Edge cases and error handling

### Creating an Admin User (Optional)

To access the Django admin interface:

```bash
python manage.py createsuperuser
```

Follow the prompts to create a username and password, then access the admin at:
```
http://127.0.0.1:8000/admin/
```

## Usage

### Creating a TODO

1. Click the "Add New TODO" button on the main page
2. Fill in the title (required)
3. Optionally add a description and due date
4. Click "Save"

### Editing a TODO

1. Click the "Edit" button next to any TODO
2. Modify the fields as needed
3. You can also mark it as resolved from the edit page
4. Click "Save"

### Marking as Resolved

- Click the "Resolve" button next to any TODO to mark it as complete
- Click "Unresolve" to mark it as pending again
- Resolved TODOs appear with a green background and strikethrough text

### Deleting a TODO

1. Click the "Delete" button next to any TODO
2. Confirm the deletion on the confirmation page

## Project Structure

```
module_01/
├── manage.py
├── venv/                       # Virtual environment
├── todoproject/                # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── todos/                      # TODO app
    ├── models.py              # Todo model definition
    ├── views.py               # View logic
    ├── urls.py                # URL routing
    ├── admin.py               # Admin interface configuration
    ├── templates/
    │   └── todos/
    │       ├── base.html           # Base template
    │       ├── todo_list.html      # TODO list view
    │       ├── todo_form.html      # Create/Edit form
    │       └── todo_confirm_delete.html  # Delete confirmation
    └── migrations/            # Database migrations
```

## Model Structure

The `Todo` model includes:

- **title**: CharField (max 200 characters) - Required
- **description**: TextField - Optional
- **due_date**: DateField - Optional
- **resolved**: BooleanField - Default: False
- **created_at**: DateTimeField - Auto-generated
- **updated_at**: DateTimeField - Auto-updated

## Technologies Used

- **Django 5.2.8**: Web framework
- **SQLite**: Database (default Django database)
- **Python 3**: Programming language
