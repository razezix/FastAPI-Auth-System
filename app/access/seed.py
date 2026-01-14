from sqlalchemy.orm import Session
from app.accounts.models import User
from app.access.models import Role, Resource, AccessRule, UserRole
from app.core.security import hash_password

def seed_if_empty(db: Session):
    # если роли уже есть — считаем что сидирование сделано
    if db.query(Role).first():
        return

    admin = Role(name="admin", description="Администратор")
    manager = Role(name="manager", description="Менеджер")
    user = Role(name="user", description="Пользователь")
    db.add_all([admin, manager, user])
    db.commit()
    db.refresh(admin); db.refresh(manager); db.refresh(user)

    products = Resource(code="products", description="Товары (mock)")
    orders = Resource(code="orders", description="Заказы (mock)")
    access_rules = Resource(code="access_rules", description="Правила доступа")
    db.add_all([products, orders, access_rules])
    db.commit()
    db.refresh(products); db.refresh(orders); db.refresh(access_rules)

    # admin: всё
    for res in [products, orders, access_rules]:
        db.add(AccessRule(
            role_id=admin.id, resource_id=res.id,
            read_permission=True, read_all_permission=True,
            create_permission=True,
            update_permission=True, update_all_permission=True,
            delete_permission=True, delete_all_permission=True
        ))

    # manager: read_all + create + update_all, без delete
    for res in [products, orders]:
        db.add(AccessRule(
            role_id=manager.id, resource_id=res.id,
            read_permission=True, read_all_permission=True,
            create_permission=True,
            update_permission=True, update_all_permission=True,
            delete_permission=False, delete_all_permission=False
        ))

    # user: create + read/update/delete только свои
    for res in [products, orders]:
        db.add(AccessRule(
            role_id=user.id, resource_id=res.id,
            read_permission=True, read_all_permission=False,
            create_permission=True,
            update_permission=True, update_all_permission=False,
            delete_permission=True, delete_all_permission=False
        ))

    db.commit()

    # тестовые пользователи
    def mk_user(email: str, full_name: str, password: str) -> User:
        u = User(full_name=full_name, email=email.lower(), password_hash=hash_password(password), is_active=True)
        db.add(u)
        db.commit()
        db.refresh(u)
        return u

    u_admin = mk_user("admin@example.com", "Admin", "admin123")
    u_manager = mk_user("manager@example.com", "Manager", "manager123")
    u_user = mk_user("user@example.com", "User", "user123")

    db.add_all([
        UserRole(user_id=u_admin.id, role_id=admin.id),
        UserRole(user_id=u_manager.id, role_id=manager.id),
        UserRole(user_id=u_user.id, role_id=user.id),
    ])
    db.commit()
