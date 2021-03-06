from api.models import db

class UserFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def as_dict(self):
        obj_d = {
            'id': self.id,
            'author_id': self.author_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'description': self.description,
        }
        return obj_d
