from sqlalchemy import Column, Integer, String, ForeignKey, func, MetaData
from sqlalchemy.orm import relationship, backref, declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    # Relationship to freebies
    freebies = relationship('Freebie', back_populates='company')
    
    # Relationship to devs through freebies
    devs = relationship('Dev', secondary='freebies', back_populates='companies', viewonly=True)

    def give_freebie(self, dev, item_name, value):
        # Creates a new Freebie associated with THIS company and the GIVEN dev
        new_freebie = Freebie(
            item_name=item_name,
            value=value,
            dev=dev,
            company=self
        )
        return new_freebie

    @classmethod
    def oldest_company(cls, session):
        # Uses the session to find the company with the minimum founding_year
        return session.query(cls).order_by(cls.founding_year).first()

    def __repr__(self):
        return f'<Company {self.name}>'

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    # Relationship to freebies
    freebies = relationship('Freebie', back_populates='dev')
    
    # Relationship to companies through freebies
    companies = relationship('Company', secondary='freebies', back_populates='devs', viewonly=True)

    def received_one(self, item_name):
        # Returns True if any freebie name matches the input
        return any(f.item_name == item_name for f in self.freebies)

    def give_away(self, dev, freebie):
        # Only change owner if the freebie currently belongs to THIS dev instance
        if freebie.dev == self:
            freebie.dev = dev
        else:
            print(f"{self.name} does not own {freebie.item_name}!")

    def __repr__(self):
        return f'<Dev {self.name}>'

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    
    # Foreign Keys
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))
    
    # Relationships
    dev = relationship('Dev', back_populates='freebies')
    company = relationship('Company', back_populates='freebies')

    def print_details(self):
        # Accesses the related dev and company names through the relationships
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"

    def __repr__(self):
        return f'<Freebie {self.item_name}>'