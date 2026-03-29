"""
Tagging Extension for Notmuch Data Source (Deprecated)

This module previously provided extended functionality for tagging emails with AI analysis
and smart filtering capabilities. This functionality has been consolidated into the 
main NotmuchDataSource class to reduce duplication and improve maintainability.

The file is kept for backward compatibility but is now deprecated.
"""

import logging
from typing import Any, Dict, List, Optional

from .notmuch_data_source import NotmuchDataSource

logger = logging.getLogger(__name__)


class TaggingNotmuchDataSource(NotmuchDataSource):
    """
    DEPRECATED: This class is deprecated. Use NotmuchDataSource directly.
    
    The tagging functionality has been consolidated into the main NotmuchDataSource class.
    This class is kept for backward compatibility only.
    """

    def __init__(self, db_path: Optional[str] = None):
        super().__init__(db_path)
        logger.warning("TaggingNotmuchDataSource is deprecated. Use NotmuchDataSource directly.")


# For backward compatibility, we can also provide a simple function
def get_tagging_notmuch_data_source(db_path: Optional[str] = None) -> NotmuchDataSource:
    """
    DEPRECATED: Get a NotmuchDataSource instance with tagging capabilities.
    
    This function is provided for backward compatibility. The tagging functionality
    is now part of the main NotmuchDataSource class.
    
    Args:
        db_path: Path to the notmuch database
        
    Returns:
        NotmuchDataSource: An instance of NotmuchDataSource with tagging capabilities
    """
    logger.warning("get_tagging_notmuch_data_source is deprecated. Use NotmuchDataSource directly.")
    return NotmuchDataSource(db_path)