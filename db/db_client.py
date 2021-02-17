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

    def setup(self, application):
        application.on_startup.append(self._on_connect)
        application.on_cleanup.append(self._on_disconnect)

    async def _on_connect(self, application):
        from db.models import db

        host = self.config.get("db_host")
        name = self.config.get("db_name")
        user = self.config.get("db_user")
        password = self.config.get("db_password")

        await db.set_bind(f'postgresql://{user}:{password}@{host}/{name}')

        self.db = db
        application["db_client"] = self

    async def _on_disconnect(self, _):
        if self.db is not None:
            await self.db.pop_bind().close()
