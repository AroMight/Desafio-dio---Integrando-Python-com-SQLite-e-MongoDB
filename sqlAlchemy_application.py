from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, inspect, select

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"
    # atributos
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    fullname = Column(String)

    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User (id={self.id}, name={self.name}, fullname={self.fullname})"


class Address(Base):
    __tablename__ = "address"
    # atributos
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_address = Column(String(40), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="address")

    def __repr__(self):
        return f"Address (id={self.id}, email_address={self.email_address})"


# conexão com o banco de dados

engine = create_engine("sqlite://")

# criando as classes como tabelas no banco de dados

Base.metadata.create_all(engine)

insp = inspect(engine)

# investiga o esquema de banco de dados

print(insp.has_table('user_account'))
print(insp.get_table_names())
print(insp.get_table_names())

with Session(engine) as session:
    denilson = User(
        name='denilson',
        fullname='denilson silva',
        address=[Address(email_address='aromight@lol.com')]
    )

    luciane = User(
        name='luciane',
        fullname='luciane sousa',
        address=[Address(email_address='taifu@lol.com'),
                Address(email_address='lu@gmail.com')]
    )

    sandy = User(
        name='sandy',
        fullname='sandy juniors',
    )

    # enviando para o BD
    session.add_all([denilson, sandy, luciane])

    session.commit()

stmt = select(User).where(User.name.in_(['denilson','luciane','sandy']))
# for user in session.scalars(stmt):
#     print(user.name)

stmt_adress = select(Address).where(Address.user_id.in_([2]))
for user in session.scalars(stmt_adress):
    print(user)
