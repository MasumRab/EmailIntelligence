from src.backend.python_backend import dependencies
from src.backend.python_nlp.smart_filters import SmartFilterManager as Real

def test_dependency_binds_the_real_class():
    assert dependencies.SmartFilterManager is Real
