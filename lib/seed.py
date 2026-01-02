#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie

def seed_data():
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Clear existing data
    session.query(Freebie).delete()
    session.query(Dev).delete()
    session.query(Company).delete()
    session.commit()

    # Create sample companies
    company1 = Company(name="TechCorp", founding_year=2000)
    company2 = Company(name="InnoSoft", founding_year=2010)

    # Create sample developers
    dev1 = Dev(name="Alice")
    dev2 = Dev(name="Bob")

    session.add_all([company1, company2, dev1, dev2])
    session.commit()

    # Create sample freebies using the Freebie model
    freebie1 = Freebie(
        item_name='Sticker Pack',
        value=5,
        dev_id=dev1.id,
        company_id=company1.id
    )
    freebie2 = Freebie(
        item_name='T-Shirt',
        value=20,
        dev_id=dev2.id,
        company_id=company2.id
    )
    freebie3 = Freebie(
        item_name='Water Bottle',
        value=15,
        dev_id=dev1.id,
        company_id=company2.id
    )

    session.add_all([freebie1, freebie2, freebie3])
    session.commit()
    session.close()
    
    print("Seeding complete!")

if __name__ == '__main__':
    seed_data()
