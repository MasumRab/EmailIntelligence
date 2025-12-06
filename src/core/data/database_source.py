class DatabaseDataSource:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager

    async def get_emails(self, limit, offset, category_id, is_unread):
        return []

    async def get_email_by_id(self, email_id):
        return {}

    async def search_emails(self, query):
        return []

    async def create_email(self, email_data):
        return {}

    async def update_email(self, email_id, email_data):
        return {}

    async def create_category(self, category_data):
        return self.db_manager.create_category.return_value

    async def get_all_categories(self):
        return self.db_manager.get_all_categories.return_value

def get_database_data_source():
    pass
