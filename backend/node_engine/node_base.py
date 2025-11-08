from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List

class DataType(Enum):
    EMAIL_LIST = "email_list"
    JSON = "json"

class NodePort:
    def __init__(self, name: str, data_type: DataType, required: bool = True, description: str = ""):
        self.name = name
        self.data_type = data_type
        self.required = required
        self.description = description

class ExecutionContext:
    def __init__(self):
        self._errors = []

    def add_error(self, node_id: str, message: str):
        self._errors.append({"node_id": node_id, "message": message})

    def get_errors(self) -> List[Dict[str, Any]]:
        return self._errors

class BaseNode(ABC):
    def __init__(self, node_id: str, name: str, description: str):
        self.node_id = node_id
        self.name = name
        self.description = description
        self.input_ports: List[NodePort] = []
        self.output_ports: List[NodePort] = []
        self.inputs: Dict[str, Any] = {}

    def set_input(self, port_name: str, value: Any):
        self.inputs[port_name] = value

    @abstractmethod
    async def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        pass
