# FastAPI Auth & Authorization System

A comprehensive authentication and authorization system built with FastAPI, featuring JWT-based authentication, role-based access control (RBAC), and PostgreSQL database integration.

## Features

- **User Authentication**: Register, login, and manage user accounts with secure password hashing using bcrypt
- **JWT Tokens**: JSON Web Token-based authentication with access and refresh tokens
- **Role-Based Access Control (RBAC)**: Fine-grained permission management with roles and permissions
- **Database Integration**: SQLAlchemy ORM with PostgreSQL support
- **Email Validation**: Built-in email validation using pydantic-settings
- **Middleware Authentication**: Custom authentication middleware for request validation
- **Demo Data**: Pre-seeded test data for easy testing

## Tech Stack

- **Framework**: FastAPI 0.110+
- **Server**: Uvicorn 0.27+
- **Database**: PostgreSQL with SQLAlchemy 2.0+
- **Authentication**: JWT (PyJWT 2.8+) + Bcrypt 4.1+
- **Validation**: Pydantic 2.6+ and Pydantic-Settings 2.2+
- **Email**: Email-validator 2.0+

## Project Structure

```
app/
├── accounts/           # User account management
│   ├── models.py      # SQLAlchemy models
│   ├── schemas.py     # Pydantic request/response schemas
│   ├── router.py      # API endpoints
│   └── service.py     # Business logic
├── access/            # Role-based access control
│   ├── models.py      # Permission and role models
│   ├── schemas.py     # Access control schemas
│   ├── router.py      # Admin endpoints
│   ├── service.py     # Access control logic
│   └── seed.py        # Initial data seeding
├── business/          # Business logic endpoints
│   ├── mock_data.py   # Mock data for testing
│   └── router.py      # Protected business endpoints
├── core/              # Core configurations
│   ├── config.py      # Application settings
│   ├── database.py    # Database configuration
│   ├── security.py    # Security utilities
│   └── auth_middleware.py  # Custom authentication middleware
├── main.py            # Application entry point
└── requirements.txt   # Project dependencies
```

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip or poetry

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd FastAPI Auth
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/fastapi_auth
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. **Run the application**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs` (Swagger UI)
- Alternative Documentation: `http://localhost:8000/redoc` (ReDoc)

## Authentication Flow

1. User registers with email and password
2. Password is hashed using bcrypt
3. User logs in with credentials
4. Server generates JWT access token
5. Client includes token in `Authorization: Bearer <token>` header
6. Middleware validates token on each request
7. User can access protected endpoints based on their role

## API Endpoints

### Authentication (Accounts)
- `POST /register` - Register new user
- `POST /login` - Login user
- `GET /me` - Get current user (requires auth)

### Access Control (Admin)
- `GET /roles` - List all roles (requires admin)
- `POST /roles` - Create new role (requires admin)
- `GET /permissions` - List all permissions (requires admin)
- `POST /permissions` - Create new permission (requires admin)

### Business Logic
- Protected endpoints for authenticated users with specific roles

## Key Components

### Authentication Middleware
Custom middleware that validates JWT tokens on each request and attaches user information to the request context.

### Role-Based Access Control
Flexible permission system allowing:
- Multiple roles per user
- Multiple permissions per role
- Fine-grained endpoint protection

### Security Features
- Password hashing with bcrypt
- JWT token validation
- Request middleware for automatic authentication
- Role and permission-based authorization

## Example Usage

```python
# Login
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Get current user (with token)
curl -X GET "http://localhost:8000/me" \
  -H "Authorization: Bearer <your_token>"
```

## Testing

The application comes pre-seeded with test data. Check `app/access/seed.py` for default users and roles.

## License

This project is provided as-is for educational and development purposes.

---

# FastAPI Auth & Authorization System

Полнофункциональная система аутентификации и авторизации, разработанная на FastAPI с поддержкой JWT-токенов, управления доступом на основе ролей (RBAC) и интеграцией с PostgreSQL.

## Возможности

- **Аутентификация пользователей**: Регистрация, вход и управление учетными записями с безопасным хешированием паролей через bcrypt
- **JWT токены**: Аутентификация на основе JSON Web Token с токенами доступа и обновления
- **Управление доступом на основе ролей (RBAC)**: Детальное управление разрешениями с ролями и правами доступа
- **Интеграция с базой данных**: ORM SQLAlchemy с поддержкой PostgreSQL
- **Валидация Email**: Встроенная валидация электронной почты с использованием pydantic-settings
- **Middleware аутентификации**: Пользовательское middleware для валидации запросов
- **Демо-данные**: Предзагруженные тестовые данные для удобного тестирования

## Технологический стек

- **Framework**: FastAPI 0.110+
- **Сервер**: Uvicorn 0.27+
- **База данных**: PostgreSQL со SQLAlchemy 2.0+
- **Аутентификация**: JWT (PyJWT 2.8+) + Bcrypt 4.1+
- **Валидация**: Pydantic 2.6+ и Pydantic-Settings 2.2+
- **Email**: Email-validator 2.0+

## Структура проекта

```
app/
├── accounts/           # Управление учетными записями пользователей
│   ├── models.py      # SQLAlchemy модели
│   ├── schemas.py     # Pydantic схемы запросов/ответов
│   ├── router.py      # API endpoints
│   └── service.py     # Бизнес-логика
├── access/            # Управление доступом на основе ролей
│   ├── models.py      # Модели разрешений и ролей
│   ├── schemas.py     # Схемы управления доступом
│   ├── router.py      # Admin endpoints
│   ├── service.py     # Логика управления доступом
│   └── seed.py        # Инициализация начальных данных
├── business/          # Endpoints бизнес-логики
│   ├── mock_data.py   # Mock данные для тестирования
│   └── router.py      # Защищенные endpoints
├── core/              # Основные конфигурации
│   ├── config.py      # Настройки приложения
│   ├── database.py    # Конфигурация базы данных
│   ├── security.py    # Утилиты безопасности
│   └── auth_middleware.py  # Пользовательское middleware аутентификации
├── main.py            # Точка входа приложения
└── requirements.txt   # Зависимости проекта
```

## Начало работы

### Предварительные требования

- Python 3.9+
- PostgreSQL 12+
- pip или poetry

### Установка

1. **Клонируйте репозиторий**
```bash
git clone <repository-url>
cd FastAPI Auth
```

2. **Создайте виртуальное окружение**
```bash
python -m venv .venv
source .venv/bin/activate  # На Windows: .venv\Scripts\activate
```

3. **Установите зависимости**
```bash
pip install -r requirements.txt
```

4. **Настройте переменные окружения**
Создайте файл `.env` в корне проекта:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/fastapi_auth
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. **Запустите приложение**
```bash
uvicorn app.main:app --reload
```

API будет доступен по адресу `http://localhost:8000`
- API документация: `http://localhost:8000/docs` (Swagger UI)
- Альтернативная документация: `http://localhost:8000/redoc` (ReDoc)

## Процесс аутентификации

1. Пользователь регистрируется с email и паролем
2. Пароль хешируется с помощью bcrypt
3. Пользователь входит в систему с учетными данными
4. Сервер генерирует JWT токен доступа
5. Клиент включает токен в заголовок `Authorization: Bearer <token>`
6. Middleware валидирует токен при каждом запросе
7. Пользователь получает доступ к защищенным endpoints в зависимости от его роли

## API Endpoints

### Аутентификация (Accounts)
- `POST /register` - Регистрация нового пользователя
- `POST /login` - Вход пользователя
- `GET /me` - Получить информацию текущего пользователя (требуется аутентификация)

### Управление доступом (Admin)
- `GET /roles` - Список всех ролей (требуется admin)
- `POST /roles` - Создание новой роли (требуется admin)
- `GET /permissions` - Список всех разрешений (требуется admin)
- `POST /permissions` - Создание нового разрешения (требуется admin)

### Бизнес-логика
- Защищенные endpoints для аутентифицированных пользователей с определенными ролями

## Основные компоненты

### Middleware аутентификации
Пользовательское middleware, которое валидирует JWT токены при каждом запросе и присоединяет информацию пользователя к контексту запроса.

### Управление доступом на основе ролей
Гибкая система разрешений, позволяющая:
- Несколько ролей на одного пользователя
- Несколько разрешений на одну роль
- Детальную защиту endpoints

### Особенности безопасности
- Хеширование паролей с bcrypt
- Валидация JWT токенов
- Middleware запросов для автоматической аутентификации
- Авторизация на основе ролей и разрешений

## Пример использования

```python
# Вход
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Получить информацию текущего пользователя (с токеном)
curl -X GET "http://localhost:8000/me" \
  -H "Authorization: Bearer <your_token>"
```

## Тестирование

Приложение поставляется с предзагруженными тестовыми данными. Проверьте `app/access/seed.py` для стандартных пользователей и ролей.

## 📄 Лицензия

Этот проект предоставляется в том виде, в каком он есть, в образовательных и разработочных целях.
