from sqlalchemy.orm import DeclarativeBase, declared_attr



class Base(DeclarativeBase):
    id: any
    __name__: str

    __allow_unmapped__ = True

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()
