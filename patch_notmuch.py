with open("src/core/notmuch_data_source.py", "r") as f:
    content = f.read()
content = content.replace("from typing import Dict, List, Optional, Any", "from typing import Dict, List, Optional, Any")
content = content.replace("db_manager: Optional['DatabaseManager'] = None", "db_manager: Optional[Any] = None")
with open("src/core/notmuch_data_source.py", "w") as f:
    f.write(content)
