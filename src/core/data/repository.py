class EmailRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    async def get_emails(self, limit: int, offset: int, category_id: int, is_unread: bool):
        return await self.db_manager.get_emails(limit=limit, offset=offset, category_id=category_id, is_unread=is_unread)

    async def get_email_by_id(self, email_id: int):
        return await self.db_manager.get_email_by_id(email_id)

    async def search_emails(self, query: str):
        return await self.db_manager.search_emails(query)

    async def create_email(self, email_data: dict):
        return await self.db_manager.create_email(email_data)

    async def update_email(self, email_id: int, email_data: dict):
        return await self.db_manager.update_email(email_id, email_data)
