import unittest
from backend.node_engine.node_base import DataType, GenericType
from backend.node_engine.workflow_engine import WorkflowEngine

class TestGenericTypes(unittest.TestCase):
    def setUp(self):
        self.engine = WorkflowEngine()

    def test_generic_type_instantiation(self):
        """Test creating GenericType instances."""
        # List[String]
        list_str = GenericType(DataType.LIST, [DataType.STRING])
        self.assertEqual(list_str.base_type, DataType.LIST)
        self.assertEqual(list_str.type_parameters, [DataType.STRING])
        self.assertEqual(str(list_str), "list[string]")

        # Dict[String, Number]
        dict_str_num = GenericType(DataType.DICT, [DataType.STRING, DataType.NUMBER])
        self.assertEqual(dict_str_num.base_type, DataType.DICT)
        self.assertEqual(dict_str_num.type_parameters, [DataType.STRING, DataType.NUMBER])
        self.assertEqual(str(dict_str_num), "dict[string, number]")

        # List[List[String]] (Nested)
        nested = GenericType(DataType.LIST, [list_str])
        self.assertEqual(nested.base_type, DataType.LIST)
        self.assertEqual(nested.type_parameters[0], list_str)
        self.assertEqual(str(nested), "list[list[string]]")

    def test_basic_compatibility(self):
        """Test compatibility of identical generic types."""
        type1 = GenericType(DataType.LIST, [DataType.STRING])
        type2 = GenericType(DataType.LIST, [DataType.STRING])
        self.assertTrue(self.engine._validate_type_compatibility(type1, type2))

        type3 = GenericType(DataType.LIST, [DataType.NUMBER])
        self.assertFalse(self.engine._validate_type_compatibility(type1, type3))

    def test_any_compatibility(self):
        """Test compatibility with ANY."""
        # List[Any] accepts List[String] ? No, usually covariance is tricky.
        # But here we implement: _validate_type_compatibility checks recursively.
        # DataType.ANY matches anything.

        # Target: List[Any], Source: List[String]
        # Should be compatible if Any matches String.
        target = GenericType(DataType.LIST, [DataType.ANY])
        source = GenericType(DataType.LIST, [DataType.STRING])
        self.assertTrue(self.engine._validate_type_compatibility(source, target))

        # Target: List[String], Source: List[Any]
        # Should be compatible? If source is List[Any], it might contain Non-Strings.
        # But _validate_type_compatibility(Any, String) -> True?
        # Let's check logic:
        # if target_type == DataType.ANY: return True
        # if source_type == target_type: return True
        # ...
        # return False

        # So Any matches Any, but Any does NOT match String as source.
        # wait, _validate_type_compatibility(source=ANY, target=STRING) -> False
        # Correct. You can't pass Any to String safely.

        self.assertFalse(self.engine._validate_type_compatibility(target, source))


    def test_nested_compatibility(self):
        """Test nested generic types compatibility."""
        # List[List[Any]] vs List[List[String]]
        target = GenericType(DataType.LIST, [GenericType(DataType.LIST, [DataType.ANY])])
        source = GenericType(DataType.LIST, [GenericType(DataType.LIST, [DataType.STRING])])
        self.assertTrue(self.engine._validate_type_compatibility(source, target))

    def test_backward_compatibility(self):
        """Test compatibility with deprecated EMAIL_LIST."""
        # EMAIL_LIST -> List[Email]
        source = DataType.EMAIL_LIST
        target = GenericType(DataType.LIST, [DataType.EMAIL])
        self.assertTrue(self.engine._validate_type_compatibility(source, target))

        # List[Email] -> EMAIL_LIST
        source = GenericType(DataType.LIST, [DataType.EMAIL])
        target = DataType.EMAIL_LIST
        self.assertTrue(self.engine._validate_type_compatibility(source, target))

        # EMAIL_LIST -> List[String] (Should fail)
        source = DataType.EMAIL_LIST
        target = GenericType(DataType.LIST, [DataType.STRING])
        self.assertFalse(self.engine._validate_type_compatibility(source, target))

    def test_mixed_compatibility(self):
        """Test compatibility between GenericType and simple DataType."""
        # GenericType -> ANY
        source = GenericType(DataType.LIST, [DataType.STRING])
        target = DataType.ANY
        self.assertTrue(self.engine._validate_type_compatibility(source, target))

if __name__ == '__main__':
    unittest.main()
