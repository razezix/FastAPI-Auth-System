# Custom Auth/AuthZ (FastAPI)

## Аутентификация (КТО пользователь?)
- Пароль хранится как bcrypt hash.
- После login создаётся запись в таблице `sessions` и пользователю ставится Cookie `sessionid`.
- Дополнительно возвращается JWT (внутри: uid + sid). JWT проверяется через существование сессии в БД.
- Logout: сессия ревокается (revoked_at), cookie удаляется.
- Soft delete пользователя: is_active=false + revoke всех сессий.

## Авторизация (ЧТО можно?)
RBAC + per-resource rules:
- roles: роли (admin/manager/user)
- resources: ресурсы приложения (products/orders/access_rules)
- user_roles: назначение ролей пользователям
- access_rules: матрица прав (роль -> ресурс -> действия)

Права:
- read_permission: читать только свои объекты (owner_id == user.id)
- read_all_permission: читать все
- create_permission: создавать
- update_permission / update_all_permission: обновлять свои / все
- delete_permission / delete_all_permission: удалять свои / все

Если user не определён -> 401
Если user определён, но нет прав -> 403

## Admin API
Только пользователь с ролью `admin` может:
- управлять roles/resources/access_rules через /api/admin/*
