class DbClient():
    def __init__(self, config):
        self.config = config
        from db.models import Document, Game, Round, User, Question
        self.document = Document
        self.game = Game
        self.round = Round
        self.user = User
        self.question = Question
        self.db = None

    async def connect(self, application):
        await self.db.set_bind(
            f'postgresql://{self.config.get("db_host")}/{self.config.get("db_name")}'
        )
