from lesson_2 import User, Order, OrderProduct, Product
from sqlalchemy.orm import Session, aliased
from sqlalchemy import insert, select, or_, and_, func
from sqlalchemy.dialects.postgresql import insert as pg_insert
import random
from faker import Faker

class Repo:
    def __init__(self, session: Session):
        self.session = session

    def add_user_v1(
        self,
        telegram_id: int,
        full_name: str,
        language_code: str,
        username: str = None,
        referrer_id: int = None,
    ) -> User:
        user = User(
            telegram_id=telegram_id,
            full_name=full_name,
            language_code=language_code,
            username=username,
            referrer_id=referrer_id,
        )
        self.session.add(user)
        self.session.commit()
        return user

    def add_user_v2(
        self,
        telegram_id: int,
        full_name: str,
        language_code: str,
        username: str = None,
        referrer_id: int = None,
    ) -> User:
        stmt = select(User).from_statement(
            pg_insert(User)
            .values(
                telegram_id=telegram_id,
                full_name=full_name,
                username=username,
                language_code=language_code,
                referrer_id=referrer_id,
            )
            .returning(User)
            .on_conflict_do_update(
                index_elements=[User.telegram_id],
                set_=dict(
                    username=username,
                    full_name=full_name,
                ),
            )

        )
        res = self.session.scalars(stmt).first()
        self.session.commit()
        return res

    def add_order(self, user_id: int) -> Order:
        stmt = select(Order).from_statement(
            pg_insert(Order)
            .values(user_id=user_id)
            .returning(Order)
        )
        result = self.session.scalars(stmt).first()
        self.session.commit()
        return result
    
    def add_product(self, title: str, description: str, price: int) -> Product:
        stmt = select(Product).from_statement(
            pg_insert(Product)
           .values(title=title, description=description, price=price)
           .returning(Product)
        )
        result = self.session.scalars(stmt).first()
        self.session.commit()
        return result
    
    def add_product_to_order(self, order_id: int, product_id: int, quantity: int):
        stmt = (
            pg_insert(OrderProduct)
           .values(order_id=order_id, product_id=product_id, quantity=quantity)
        )
        self.session.execute(stmt)
        self.session.commit()
    
    def get_user_by_telegram_id(self, telegram_id: int) -> User:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def get_all_user(self) -> list[User]:
        stmt = (
            select(User)
            # .where(
            #     or_(
            #         User.username.ilike("%john%"), 
            #         User.full_name.ilike("%doe%")),
            #     User.language_code.ilike("%en%"))
            # .order_by(User.created_at.desc())
            # .limit(10)
            # .having(User.telegram_id > 0)
        )
        result = self.session.execute(stmt)
        return result.scalars().all()
    
    def get_user_orders(self, telegram_id: int) -> list[Order]:
        """
        Retrieve all orders associated with a specific user identified by their Telegram ID.

        This function performs a SQL query to join the Order and User tables,
        filtering for orders belonging to the user with the given Telegram ID.

        Args:
            telegram_id (int): The Telegram ID of the user whose orders are to be retrieved.

        Returns:
            list[Order]: A list of Order objects associated with the specified user.
                         Each Order object includes the full name of the user who placed the order.

        Note:
            The result is made unique to avoid potential duplicate entries.
        """
        stmt = (
            select(User.full_name, Order, OrderProduct.quantity)
            .join(User, Order.user_id == User.telegram_id)
            .join(OrderProduct, Order.order_id == OrderProduct.order_id)
            .where(User.telegram_id == telegram_id)
        )
        result = self.session.execute(stmt)
        return result.unique().all()

    def get_user_language(self, telegram_id: int) -> str:
        stmt = select(User.language_code).where(User.telegram_id == telegram_id)
        result = self.session.execute(stmt)
        return result.scalar()

    def select_all_invited_users(self) -> list[User]:
        ParentUser = aliased(User)
        ReferralUser = aliased(User)

        stmt = (
            select(
                ParentUser.full_name.label('parent_name'),
                ReferralUser.full_name.label('referral_name'),
            ).outerjoin(
                ReferralUser, ReferralUser.referrer_id == ParentUser.telegram_id
            )
        )
        result = repo.session.execute(stmt)
        return result.all()

    def get_total_number_of_orders(self, telegram_id: int) -> int:
        stmt = (
            select(func.count(Order.order_id)).where(Order.user_id == telegram_id)
        )
        result = self.session.scalar(stmt)
        return result

    def get_users_and_numbers_of_orders(self) -> list[list[str, int]]:
        stmt = (
            select(User.full_name, func.count(Order.order_id))
            .join(User, Order.user_id == User.telegram_id)
            .group_by(User.full_name)
        )
        result = self.session.execute(stmt)
        return list(result)

def seed_fake_data(repo: Repo):
    """
    Seed the database with fake data for testing or development purposes.

    This function generates and adds fake users, orders, and products to the database
    using the provided Repo instance. It creates relationships between these entities,
    simulating a realistic dataset.

    Args:
        repo (Repo): An instance of the Repo class used to interact with the database.

    Returns:
        None

    Note:
        - The function uses the Faker library to generate realistic fake data.
        - It creates 10 users, 10 orders, and 10 products.
        - Each order is associated with a random user and contains 3 random products.
        - The seed is set to 0 for reproducibility.
    """
    Faker.seed(0)
    fake = Faker()

    users = []
    orders = []
    products = []

    for _ in range(10):
        referrer_id = None if not users else users[-1].telegram_id
        user = repo.add_user_v2(
            telegram_id=fake.pyint(),
            full_name=fake.name(),
            language_code=fake.language_code(),
            username=fake.user_name(),
            referrer_id=referrer_id,
        )
        users.append(user)

    # add orders
    for _ in range(10):
        order = repo.add_order(
            user_id=random.choice(users).telegram_id,
        )
        orders.append(order)

    # add products
    for _ in range(10):
        product = repo.add_product(
            title=fake.word(),
            description=fake.sentence(),
            price=fake.pyint(),
        )
        products.append(product)

    # add products to orders
    for order in orders:
        # Here we use `sample` function to get list of 3 unique products
        for product in random.sample(products, 3):
            repo.add_product_to_order(
                order_id=order.order_id,
                product_id=product.product_id,
                quantity=fake.pyint(),
            )
    users = []
    orders = []
    products = []

    for _ in range(10):
        referrer_id = None if not users else users[-1].telegram_id
        user = repo.add_user_v2(
            telegram_id=fake.pyint(),
            full_name=fake.name(),
            language_code=fake.language_code(),
            username=fake.user_name(),
            referrer_id=referrer_id,
        )
        users.append(user)

    # add orders
    for _ in range(10):
        order = repo.add_order(
            user_id=random.choice(users).telegram_id,
        )
        orders.append(order)

    # add products
    for _ in range(10):
        product = repo.add_product(
            title=fake.word(),
            description=fake.sentence(),
            price=fake.pyint(),
        )
        products.append(product)

    # add products to orders
    for order in orders:
        # Here we use `sample` function to get list of 3 unique products
        for product in random.sample(products, 3):
            repo.add_product_to_order(
                order_id=order.order_id,
                product_id=product.product_id,
                quantity=fake.pyint(),
            )

if __name__ == "__main__":
    from lesson_2 import Base, engine

    Base.metadata.create_all(engine)

    session = Session(bind=engine)
    repo = Repo(session)
    
    # seed_fake_data(repo)

    # rows = repo.select_all_invited_users()
    # print(rows)

    # Get all user and their orders
    # users = repo.get_all_user()
    # for user in users:
    #     print(user.full_name)
    #     for order in user.orders:
    #         print(f"\tOrder ID: {order.order_id}")
    #         for product_association in order.products:
    #             print(f"\t\tProduct ID: {product_association.product_id}")

    # all_orders = repo.get_user_orders(4104)
    # print(all_orders)

    # numbers_of_orders = repo.get_total_number_of_orders(4104)
    # print(numbers_of_orders)

    # users_and_num_orders = repo.get_users_and_numbers_of_orders()
    # print(users_and_num_orders)