__author__ = 'beast'

from datetime import datetime

from faker import Factory
from datafall.main import build_application, raw_db


def create_fake_customers(fake, db, collection):
    customers = []
    for i in range(0, 10):
        customer = {
            "name": fake.name(),
            "address": fake.address(),
            "date_created": datetime.now()


        }

        customers.append(customer)

        db[collection].insert(customer)
    return customers


def create_fake_set(db, collection):
    fake = Factory.create()

    data = {}
    data["customers"] = create_fake_customers(fake, db, collection)

    return data


def create_fake():
    app = build_application()

    with app.app_context():
        data = create_fake_set(raw_db.db, "Customers")

        print data


create_fake()