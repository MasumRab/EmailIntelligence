import pytest
from src.backend.node_engine.node_base import NodePort, DataType, BaseNode, _UNSET, ExecutionContext

class DummyNode(BaseNode):
    async def execute(self, context: ExecutionContext) -> dict:
        return {}

def test_optional_port_no_value():
    node = DummyNode()
    node.input_ports.append(NodePort("opt1", DataType.STRING, required=False, default_value="default_str"))
    node.set_inputs({})
    assert node.inputs.get("opt1") == "default_str"
    assert node.validate_inputs() == {"valid": True, "errors": []}

def test_optional_port_explicit_value():
    node = DummyNode()
    node.input_ports.append(NodePort("opt1", DataType.STRING, required=False, default_value="default_str"))
    node.input_ports.append(NodePort("opt2", DataType.STRING, required=False, default_value="default_str"))
    node.set_inputs({"opt1": "explicit_str", "opt2": None})
    assert node.inputs.get("opt1") == "explicit_str"
    assert node.inputs.get("opt2") is None

def test_required_port_missing():
    node = DummyNode()
    node.input_ports.append(NodePort("req1", DataType.STRING, required=True))
    node.set_inputs({})
    res = node.validate_inputs()
    assert res["valid"] is False
    assert "Required input 'req1' is missing" in res["errors"]

def test_default_value_repr():
    port1 = NodePort("port1", DataType.STRING, required=False)
    assert "default_value=<unset>" in repr(port1)
    
    port2 = NodePort("port2", DataType.STRING, required=False, default_value="val")
    assert "default_value='val'" in repr(port2)

def test_required_and_default_raises():
    with pytest.raises(ValueError, match="required port 'req_err' cannot declare a default_value"):
        NodePort("req_err", DataType.STRING, required=True, default_value="val")

def test_optional_port_no_default_no_injection():
    node = DummyNode()
    node.input_ports.append(NodePort("opt1", DataType.STRING, required=False)) # no default provided, implicitly _UNSET
    node.set_inputs({})
    assert "opt1" not in node.inputs
