from flask.config import T
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from flask_sqlalchemy import SQLAlchemy
from typing import List


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Vehicles(Base):
    __tablename__ = "vehicle"

    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(db.String(17), unique=True)
    customer_phone: Mapped[str] = mapped_column(db.String(11), db.ForeignKey("customer.phone_number"), nullable=True)

    customer: Mapped["Customers"] = relationship("Customers", back_populates="vehicles",foreign_keys=[customer_phone])
    service_tickets: Mapped[List["Service_Tickets"]] = relationship("Service_Tickets", back_populates="vehicle")

class Customers(Base):
    __tablename__ = "customer"

    phone_number: Mapped[str] = mapped_column(db.String(11), primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(db.String(100))
    vin: Mapped[str] = mapped_column(db.ForeignKey("vehicle.vin"), nullable=True)

    service_tickets: Mapped[List["Service_Tickets"]] = relationship(back_populates = "customer")
    vehicles: Mapped[List["Vehicles"]] = relationship("V"
    "ehicles", back_populates = "customer", foreign_keys = [Vehicles.customer_phone])

class Mechanics(Base):
    __tablename__ = "mechanic"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[str] = mapped_column(db.String(11))
    name: Mapped[str] = mapped_column(db.String(100))
    skill_level:  Mapped[str] = mapped_column(db.String(7))
    hourly_rate: Mapped[int]

    service_tickets: Mapped[List["Service_Tickets"]] = relationship(back_populates = "mechanic", foreign_keys = "[Service_Tickets.mechanic_id]")

class Service_Tickets(Base):
    __tablename__ = "service_ticket"

    ticket_id: Mapped[int] = mapped_column(primary_key=True)
    customer_phone: Mapped[str] = mapped_column(db.String(11), db.ForeignKey("customer.phone_number"))
    vin: Mapped[str] = mapped_column(db.ForeignKey("vehicle.vin"), nullable=True)
    mechanic_id: Mapped[int] = mapped_column(db.ForeignKey("mechanic.id"))
    services: Mapped[str] = mapped_column(db.String(10000))

    customer: Mapped["Customers"] = relationship(back_populates = "service_tickets")
    mechanic: Mapped["Mechanics"] = relationship(back_populates = "service_tickets")
    vehicle: Mapped["Vehicles"] = relationship(back_populates = "service_tickets")



