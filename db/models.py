from gino import Gino

db = Gino()


class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode())
    text = db.Column(db.Unicode())


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer(), primary_key=True)
    question_text = db.Column(db.Unicode())
    answer1_text = db.Column(db.Unicode())
    answer2_text = db.Column(db.Unicode())
    answer3_text = db.Column(db.Unicode())
    correct_id = db.Column(db.Integer())
    # TODO: change default value for timeout == 30
    # created vshagur@gmail.com, 2021-02-18
    timeout = db.Column(db.Integer(), default=5)


class Round(db.Model):
    __tablename__ = 'rounds'

    id = db.Column(db.Integer(), primary_key=True)
    game_id = db.Column(db.Integer())
    count = db.Column(db.Integer())  # номер раунда в игре
    winner = db.Column(db.Integer())  # vk_id победителя, 0 если его нет


class User(db.Model):
    __tablename__ = 'users'

    vk_id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.Unicode(), default='noname')
    last_name = db.Column(db.Unicode(), default='noname')


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer(), primary_key=True)
    peer_id = db.Column(db.Integer())  # id беседы
    owner_id = db.Column(db.Integer, db.ForeignKey('users.vk_id')) # vk_id инициатора игры
    status = db.Column(db.Integer(), default=1)  # 1 - process или 0 - done

class Statistic(db.Model):
    __tablename__ = 'users_statistic'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.vk_id'))
    total_games = db.Column(db.Integer())
    win_games = db.Column(db.Integer())

