# 🚀 FastAPI Authentication & Authorization System

---

## 📌 Project Overview (EN)

This project is a **custom authentication and authorization backend system** built with **FastAPI**.  
It clearly separates **authentication (who the user is)** from **authorization (what the user can do)**.

The system is **not based on built-in framework authentication**, but implements its own logic:
- password hashing
- session management
- JWT tokens
- role-based access control (RBAC)

The project was created as a **test / educational assignment** to demonstrate backend security fundamentals.

---

## ⚙️ Technologies Used

- **FastAPI** — backend web framework  
- **SQLAlchemy** — ORM for database interaction  
- **PostgreSQL / SQLite** — relational database  
- **bcrypt** — secure password hashing  
- **JWT (PyJWT)** — token-based authentication  
- **Pydantic** — request/response validation  
- **Uvicorn** — ASGI server  
- **Git / GitHub** — version control  

---

## 🔐 Authentication Features

- User registration (full name, email, password)
- Secure password storage using bcrypt
- Login with email and password
- Session-based authentication using HTTP-only cookies
- JWT token generation linked to database sessions
- Logout with session revocation
- Soft delete user (`is_active = false`)
- Automatic user identification on subsequent requests

---

## 🛂 Authorization System (RBAC)

The project implements **Role-Based Access Control** using database-driven rules.

### Database entities:
- `users` — application users  
- `sessions` — active user sessions  
- `roles` — user roles (admin, manager, user)  
- `resources` — protected application resources  
- `user_roles` — role assignments  
- `access_rules` — permissions matrix  

### Supported permissions:
- read / read_all  
- create  
- update / update_all  
- delete / delete_all  

### API behavior:
- **401 Unauthorized** — user is not authenticated  
- **403 Forbidden** — user is authenticated but has no permission  

---

## 👨‍💼 Admin API

Users with the `admin` role can:
- manage roles
- manage resources
- manage access rules (permissions)

Authorization rules are applied **dynamically at runtime**.

---

## 🧩 Mock Business Logic

Mock business endpoints are implemented for demonstration:
- `/api/products`
- `/api/orders`

No database tables are required for business objects — only authorization logic is enforced.

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

# 🚀 FastAPI система аутентификации и авторизации

---

## 📌 Описание проекта

Данный проект представляет собой **кастомную backend-систему аутентификации и авторизации**, реализованную с использованием **FastAPI**.

В проекте чётко разделены ключевые понятия:
- **Аутентификация** — определяет, *кто* пользователь
- **Авторизация** — определяет, *какие действия* пользователь может выполнять

Система **не использует готовые механизмы аутентификации фреймворка**, а реализует собственную логику управления доступом.

Проект выполнен в рамках **учебного / тестового задания** и демонстрирует базовые и продвинутые принципы безопасности backend-приложений.

---

## ⚙️ Используемые технологии

- **FastAPI** — backend-фреймворк
- **SQLAlchemy** — ORM для работы с базой данных
- **PostgreSQL / SQLite** — реляционная база данных
- **bcrypt** — безопасное хеширование паролей
- **JWT (PyJWT)** — токены аутентификации
- **Pydantic** — валидация входящих и исходящих данных
- **Uvicorn** — ASGI-сервер
- **Git / GitHub** — контроль версий

---

## 🔐 Аутентификация

Реализованный функционал:
- Регистрация пользователей (ФИО, email, пароль)
- Хранение паролей в виде bcrypt-хэшей
- Вход в систему по email и паролю
- Создание и хранение пользовательских сессий в базе данных
- Авторизация через HTTP-only cookie
- Генерация JWT-токенов, связанных с сессиями
- Logout с отзывом активной сессии
- Мягкое удаление пользователя (`is_active = false`)
- Автоматическое определение пользователя при последующих запросах

---

## 🛂 Авторизация (RBAC)

В проекте реализована **ролевая модель разграничения доступа (RBAC)**.

### Структура базы данных:
- `users` — пользователи системы
- `sessions` — пользовательские сессии
- `roles` — роли пользователей (admin, manager, user)
- `resources` — защищённые ресурсы приложения
- `user_roles` — связь пользователей и ролей
- `access_rules` — правила доступа к ресурсам

### Поддерживаемые права:
- чтение (только своих объектов / всех объектов)
- создание
- обновление (только своих объектов / всех объектов)
- удаление (только своих объектов / всех объектов)

### Поведение API:
- **401 Unauthorized** — пользователь не аутентифицирован
- **403 Forbidden** — пользователь аутентифицирован, но доступ запрещён

---

## 👨‍💼 Административный API

Пользователи с ролью `admin` имеют доступ к API для:
- управления ролями
- управления ресурсами
- изменения и назначения правил доступа

Правила доступа применяются **динамически**, без изменения кода приложения.

---

## 🧩 Mock бизнес-объекты

Для демонстрации работы системы реализованы mock-endpoints:
- `/api/products`
- `/api/orders`

Таблицы для бизнес-объектов намеренно не создаются — проверяется исключительно логика авторизации.

---

## ▶️ Запуск проекта

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
