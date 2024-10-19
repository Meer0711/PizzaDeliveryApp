from database import Base
from sqlalchemy import Column,Integer,Boolean,Text,String,ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True,index=True,autoincrement=True)
    username = Column(String(25), unique=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    # Corrected relationship reference
    orders = relationship('Order', back_populates='user')  # Changed 'order' to 'Order'

    def __repr__(self):
        return f"<User {self.username}>"  # Added closing '>' for repr


class Order(Base):
    __tablename__ = 'orders'

    ORDER_STATUSES = [
        ('PENDING', 'pending'),
        ('IN-TRANSIT', 'in-transit'),
        ('DELIVERED', 'delivered')
    ]

    PIZZA_SIZES = [
        ('SMALL', 'small'),
        ('MEDIUM', 'medium'),
        ('LARGE', 'large'),
        ('EXTRA-LARGE', 'extra-large')
    ]

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(String, default="PENDING")  # Change to String
    pizza_size = Column(String, default="SMALL")      # Change to String
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates='orders')  # 'User' with capital 'U'

    def __repr__(self):
        return f"<Order {self.id}>"






