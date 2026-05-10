with open("src/core/data/data_source.py", "r") as f:
    content = f.read()

import re

# Fix imports
content = re.sub(r'from typing import List, Dict, Any\nfrom typing import Any, Dict, List\n\nfrom typing import List, Dict, Any', 'from typing import List, Dict, Any', content)

# Fix duplicated function definition
content = content.replace('''    @abstractmethod
    async def get_emails(self, limit: int = 100, offset: int = 0, category_id: int = None, is_unread: bool = None) -> List[Dict[str, Any]]:
    async def get_emails(
        self, limit: int = 100, offset: int = 0, category_id: int = None, is_unread: bool = None
    ) -> List[Dict[str, Any]]:
    async def get_emails(self, limit: int = 100, offset: int = 0, category_id: int = None, is_unread: bool = None) -> List[Dict[str, Any]]:''', '''    @abstractmethod
    async def get_emails(self, limit: int = 100, offset: int = 0, category_id: int = None, is_unread: bool = None) -> List[Dict[str, Any]]:''')

with open("src/core/data/data_source.py", "w") as f:
    f.write(content)
