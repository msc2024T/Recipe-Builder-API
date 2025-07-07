# Recipe Builder API

A comprehensive Django REST API for managing recipes, meal plans, and user authentication with Azure Blob Storage integration for image uploads.

## 🌐 Live Demo

**API Base URL:** `recipe-builder-api-dud9e3hxfcabexhd.canadacentral-01.azurewebsites.net`

## 🍳 What the Project Does

Recipe Builder API is a complete backend solution for recipe management applications that provides:

### Core Features

- **User Authentication**: JWT-based authentication with secure signup and login
- **Recipe Management**: Full CRUD operations for recipes with image support
- **Meal Planning**: Create and manage meal plans with date ranges and recipe assignments
- **Image Upload**: Azure Blob Storage integration for recipe and profile images
- **User Profiles**: User profile management with customizable profile pictures
- **RESTful API**: Clean, consistent API endpoints following REST principles

### Technical Features

- **Django REST Framework**: Professional API development with serializers and viewsets
- **JWT Authentication**: Secure token-based authentication with refresh tokens
- **Azure Integration**: Cloud storage for scalable image management
- **PostgreSQL Support**: Production-ready database with SQLite fallback
- **Environment Configuration**: Secure configuration management with django-environ
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **Service Layer Architecture**: Clean separation of business logic and API endpoints

## 🚀 How to Install and Run It

### Prerequisites

- **Python 3.11+**
- **Poetry** (recommended) or pip
- **PostgreSQL** (optional - SQLite is used by default)
- **Azure Storage Account** (for image uploads)

### Installation Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/Recipe_Builder_api.git
   cd Recipe_Builder_api
   ```

2. **Install dependencies using Poetry** (recommended)

   ```bash
   poetry install
   ```

   Or using pip:

   ```bash
   pip install -r requirements.txt
   ```

3. **Activate the virtual environment**

   With Poetry:

   ```bash
   poetry shell
   ```

   Or find your Poetry environment:

   ```bash
   poetry env info --path
   # Then activate manually:
   # Windows: & "path\Scripts\activate.ps1"
   # Linux/Mac: source path/bin/activate
   ```

4. **Set up environment variables**

   Create a `.env` file in the root directory:

   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

   # Database (optional - leave empty for SQLite)
   DB_NAME=recipe_builder_db
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432

   # Azure Storage (required for image uploads)
   AZURE_BLOB_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=your_account;AccountKey=your_key;EndpointSuffix=core.windows.net
   AZURE_STORAGE_CONTAINER_NAME=your_container_name
   AZURE_STORAGE_ACCOUNT_NAME=your_account_name
   AZURE_STORAGE_KEY=your_storage_key
   ```

5. **Run database migrations**

   ```bash
   poetry run python manage.py migrate
   ```

6. **Create a superuser** (optional)

   ```bash
   poetry run python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   poetry run python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## 📡 API Examples

### Base URL

```
http://localhost:8000/
```

### Authentication Endpoints

#### User Registration

```http
POST /users/signup/
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:**

```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "profile": {
    "id": 1,
    "profile_picture": null
  }
}
```

#### User Login

```http
POST /users/login/
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response:**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

### Recipe Endpoints

#### Get All Recipes

```http
GET /recipes/
Authorization: Bearer <access_token>
```

**Response:**

```json
[
  {
    "id": 1,
    "title": "Spaghetti Carbonara",
    "instructions": "1. Cook pasta in salted water\n2. Mix eggs with cheese\n3. Combine with hot pasta",
    "image_id": 1,
    "image_url": "https://yourstorageaccount.blob.core.windows.net/container/image.jpg",
    "created_at": "2025-01-15T10:30:00Z",
    "created_by": 1,
    "is_deleted": false
  }
]
```

#### Create Recipe

```http
POST /recipes/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Chicken Stir Fry",
  "instructions": "1. Heat oil in wok\n2. Add chicken and cook until done\n3. Add vegetables and stir fry",
  "image_id": 2
}
```

#### Get Single Recipe

```http
GET /recipes/recipe/1/
Authorization: Bearer <access_token>
```

#### Update Recipe

```http
PUT /recipes/recipe/1/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Updated Recipe Title",
  "instructions": "Updated cooking instructions...",
  "image_id": 3
}
```

#### Delete Recipe

```http
DELETE /recipes/recipe/1/
Authorization: Bearer <access_token>
```

**Response:**

```json
{
  "message": "Recipe deleted successfully"
}
```

### Meal Plan Endpoints

#### Get All Meal Plans

```http
GET /meal-plans/
Authorization: Bearer <access_token>
```

**Response:**

```json
[
  {
    "id": 1,
    "title": "Weekly Meal Plan",
    "start_date": "2025-01-15",
    "end_date": "2025-01-21",
    "created_at": "2025-01-10T09:00:00Z",
    "created_by": 1,
    "is_deleted": false
  }
]
```

#### Create Meal Plan

```http
POST /meal-plans/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Mediterranean Week",
  "start_date": "2025-02-01",
  "end_date": "2025-02-07"
}
```

#### Get Meal Plan Details

```http
GET /meal-plans/1/
Authorization: Bearer <access_token>
```

#### Update Meal Plan

```http
PUT /meal-plans/1/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Updated Meal Plan Title",
  "start_date": "2025-02-01",
  "end_date": "2025-02-10"
}
```

#### Delete Meal Plan

```http
DELETE /meal-plans/1/
Authorization: Bearer <access_token>
```

**Response:**

```json
{
  "message": "Meal plan deleted successfully"
}
```

### Meal Plan Recipe Management

#### Get Recipes in Meal Plan

```http
GET /meal-plans/1/recipes/
Authorization: Bearer <access_token>
```

**Response:**

```json
[
  {
    "id": 1,
    "meal_plan": 1,
    "recipe": {
      "id": 1,
      "title": "Spaghetti Carbonara",
      "instructions": "Cooking instructions...",
      "image_url": "https://example.com/image.jpg"
    },
    "planned_date": "2025-01-15",
    "meal_type": "dinner"
  }
]
```

#### Add Recipes to Meal Plan

```http
POST /meal-plans/1/recipes/
Authorization: Bearer <access_token>
Content-Type: application/json

[
  {
    "recipe_id": 1,
    "planned_date": "2025-01-15",
    "meal_type": "lunch"
  },
  {
    "recipe_id": 2,
    "planned_date": "2025-01-16",
    "meal_type": "dinner"
  }
]
```

#### Remove Recipe from Meal Plan

```http
DELETE /meal-plans/1/recipes/?meal_plan_recipe_id=1
Authorization: Bearer <access_token>
```

### Image Upload Endpoints

#### Upload Image

```http
POST /images/upload/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

image: <image-file>
```

**Response:**

```json
{
  "id": 1,
  "name": "recipe_image.jpg",
  "extension": "jpg",
  "created_at": "2025-01-15T10:30:00Z",
  "uploaded_by": 1
}
```

### Authentication Headers

All protected endpoints require the JWT token in the Authorization header:

```http
Authorization: Bearer <your-jwt-access-token>
```

### Error Responses

All endpoints return consistent error responses:

```json
{
  "error": "Error message describing what went wrong"
}
```

**Common HTTP Status Codes:**

- `200 OK` - Success
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

### Token Refresh

When your access token expires, use the refresh token:

```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "your-refresh-token"
}
```

## 🛠 Development

### Project Structure

```
Recipe_Builder_api/
├── recipebuilder/          # Main Django project
│   ├── settings.py         # Django settings with environment variables
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── users/                  # User authentication and profiles
│   ├── models.py          # User Profile model
│   ├── views.py           # UserSignupView, UserLoginView
│   ├── serializers.py     # User serializers
│   ├── services.py        # User business logic
│   └── urls.py            # Authentication endpoints
├── recipes/                # Recipe management
│   ├── models.py          # Recipe model
│   ├── views.py           # Recipe CRUD operations
│   ├── serializers.py     # Recipe serializers
│   ├── services.py        # Recipe business logic
│   └── urls.py            # Recipe endpoints
├── mealplans/             # Meal planning system
│   ├── models.py          # MealPlan and MealPlanRecipe models
│   ├── views.py           # Meal plan CRUD and recipe management
│   ├── serializers.py     # Meal plan serializers
│   ├── services.py        # Meal plan business logic
│   └── urls.py            # Meal plan endpoints
├── images/                # Image management
│   ├── models.py          # Image model
│   ├── views.py           # Image upload views
│   ├── serializers.py     # Image serializers
│   ├── services.py        # Azure Blob Storage integration
│   └── urls.py            # Image endpoints
├── .env                   # Environment variables (not in repo)
├── pyproject.toml         # Poetry configuration
├── requirements.txt       # Pip requirements
└── README.md             # This file
```

### Available Commands

```bash
# Development
poetry run python manage.py runserver    # Start development server
poetry run python manage.py test         # Run tests
poetry run python manage.py shell        # Django shell

# Database
poetry run python manage.py migrate      # Apply migrations
poetry run python manage.py makemigrations # Create migrations
poetry run python manage.py createsuperuser # Create admin user

# Dependencies
poetry add <package-name>                 # Add new dependency
poetry export -f requirements.txt --output requirements.txt # Update requirements.txt
```

### Environment Variables

| Variable                       | Description                   | Required            |
| ------------------------------ | ----------------------------- | ------------------- |
| `SECRET_KEY`                   | Django secret key             | Yes                 |
| `DEBUG`                        | Debug mode (True/False)       | Yes                 |
| `ALLOWED_HOSTS`                | Comma-separated allowed hosts | Yes                 |
| `CORS_ALLOWED_ORIGINS`         | Comma-separated CORS origins  | Yes                 |
| `DB_NAME`                      | Database name                 | No (SQLite default) |
| `DB_USER`                      | Database user                 | No                  |
| `DB_PASSWORD`                  | Database password             | No                  |
| `DB_HOST`                      | Database host                 | No                  |
| `DB_PORT`                      | Database port                 | No                  |
| `AZURE_BLOB_CONNECTION_STRING` | Azure Storage connection      | Yes                 |
| `AZURE_STORAGE_CONTAINER_NAME` | Azure container name          | Yes                 |
| `AZURE_STORAGE_ACCOUNT_NAME`   | Azure account name            | Yes                 |
| `AZURE_STORAGE_KEY`            | Azure storage key             | Yes                 |

## 🔧 Tech Stack

- **Django 5.2.3** - Web framework
- **Django REST Framework 3.16.0** - API development
- **SimpleJWT 5.5.0** - JWT authentication
- **django-environ 0.12.0** - Environment variables
- **django-cors-headers 4.7.0** - CORS support
- **dj-database-url 3.0.1** - Database URL configuration
- **Pillow 11.2.1** - Image processing
- **Azure Storage** - Cloud storage for images
- **PostgreSQL** - Production database
- **Poetry** - Dependency management

## 🚀 Deployment

### Production Setup

1. **Set environment variables** on your hosting platform
2. **Configure PostgreSQL database**
3. **Set up Azure Blob Storage**
4. **Install dependencies**: `pip install -r requirements.txt`
5. **Run migrations**: `python manage.py migrate`
6. **Collect static files**: `python manage.py collectstatic`
7. **Start server** with your platform's method

### Popular Deployment Platforms

- **Heroku** - Easy deployment with Procfile
- **Railway** - Automatic deployments from Git
- **DigitalOcean App Platform** - Container deployments
- **AWS Elastic Beanstalk** - Scalable deployments
- **Google Cloud Run** - Serverless containers

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Contact

For questions or support, please open an issue in the GitHub repository.

---

**Built with Django REST Framework and Azure Cloud Services**
