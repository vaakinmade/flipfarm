from src.adapters.app.application import db


class User(db.Model):
    __tablename__ = 'investor'
    id = db.Column(db.Integer, primary_key=True)
    id_ = db.Column(db.String(255))
    first_name = db.Column(db.String(255), index=True)
    last_name = db.Column(db.String(255), index=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255), index=True)
    date_of_birth = db.Column(db.Date)
    is_active = db.Column(db.Boolean, index=True)
    created_at = db.Column(db.DateTime, index=True)
    investments = db.relationship('Investment', backref='user_investment', lazy='dynamic')


class Commodity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_ = db.Column(db.String(255))
    name = db.Column(db.String(100), index=True)
    amount = db.Column(db.Integer, index=True)
    fund_status = db.Column(db.String(50))
    interest_yield = db.Column(db.Float, index=True)
    created_at = db.Column(db.DateTime, index=True)
    location = db.Column(db.String(100), index=True)
    duration = db.Column(db.Integer, index=True)
    category = db.Column(db.String(100), index=True)
    amount_raised = db.Column(db.Integer, index=True)
    location_thumbnail = db.Column(db.String(250))
    investments = db.relationship('Investment', backref='commodities_invested', lazy='dynamic')


class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_ = db.Column(db.String(255))
    amount = db.Column(db.Integer, index=True)
    status = db.Column(db.String(50))
    maturity_date = db.Column(db.DateTime, index=True)
    investor_id = db.Column(db.Integer, db.ForeignKey('investor.id'))
    commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'))
    created_at = db.Column(db.DateTime, index=True)
    updated_at = db.Column(db.DateTime, index=True)
