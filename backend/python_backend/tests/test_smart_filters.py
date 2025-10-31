"""
Comprehensive unit tests for smart_filters.py

Tests all smart filter operations including:
- Filter creation and management
- Priority handling
- Filter application
- Edge cases and error handling
"""

import pytest
from datetime import datetime
from backend.python_backend.smart_filters import (
    SmartFilter,
    SmartFilterManager,
    FilterCondition,
    FilterAction
)


class TestFilterCondition:
    """Test suite for FilterCondition class."""
    
    def test_create_sender_condition(self):
        """Test creating a sender-based condition."""
        condition = FilterCondition(field="sender", operator="equals", value="test@example.com")
        assert condition.field == "sender"
        assert condition.operator == "equals"
        assert condition.value == "test@example.com"
    
    def test_create_subject_condition(self):
        """Test creating a subject-based condition."""
        condition = FilterCondition(field="subject", operator="contains", value="urgent")
        assert condition.field == "subject"
        assert condition.operator == "contains"
        assert condition.value == "urgent"
    
    def test_condition_equality(self):
        """Test condition equality comparison."""
        cond1 = FilterCondition(field="sender", operator="equals", value="test@example.com")
        cond2 = FilterCondition(field="sender", operator="equals", value="test@example.com")
        cond3 = FilterCondition(field="sender", operator="contains", value="test")
        
        assert cond1 == cond2
        assert cond1 != cond3
    
    def test_condition_with_different_operators(self):
        """Test various operator types."""
        operators = ["equals", "contains", "starts_with", "ends_with", "regex", "greater_than", "less_than"]
        for op in operators:
            condition = FilterCondition(field="sender", operator=op, value="test")
            assert condition.operator == op
    
    def test_condition_serialization(self):
        """Test condition can be converted to dict."""
        condition = FilterCondition(field="sender", operator="equals", value="test@example.com")
        data = condition.to_dict()
        
        assert data["field"] == "sender"
        assert data["operator"] == "equals"
        assert data["value"] == "test@example.com"
    
    def test_condition_from_dict(self):
        """Test creating condition from dictionary."""
        data = {"field": "sender", "operator": "contains", "value": "example"}
        condition = FilterCondition.from_dict(data)
        
        assert condition.field == "sender"
        assert condition.operator == "contains"
        assert condition.value == "example"


class TestFilterAction:
    """Test suite for FilterAction class."""
    
    def test_create_move_action(self):
        """Test creating a move action."""
        action = FilterAction(type="move", value="Archive")
        assert action.type == "move"
        assert action.value == "Archive"
    
    def test_create_label_action(self):
        """Test creating a label action."""
        action = FilterAction(type="label", value="Important")
        assert action.type == "label"
        assert action.value == "Important"
    
    def test_create_delete_action(self):
        """Test creating a delete action."""
        action = FilterAction(type="delete")
        assert action.type == "delete"
        assert action.value is None
    
    def test_action_serialization(self):
        """Test action can be converted to dict."""
        action = FilterAction(type="move", value="Spam")
        data = action.to_dict()
        
        assert data["type"] == "move"
        assert data["value"] == "Spam"
    
    def test_action_from_dict(self):
        """Test creating action from dictionary."""
        data = {"type": "label", "value": "Work"}
        action = FilterAction.from_dict(data)
        
        assert action.type == "label"
        assert action.value == "Work"
    
    def test_action_types(self):
        """Test various action types."""
        action_types = ["move", "label", "delete", "forward", "star", "archive"]
        for action_type in action_types:
            action = FilterAction(type=action_type, value="test")
            assert action.type == action_type


class TestSmartFilter:
    """Test suite for SmartFilter class."""
    
    def test_create_basic_filter(self):
        """Test creating a basic filter."""
        condition = FilterCondition(field="sender", operator="equals", value="test@example.com")
        action = FilterAction(type="move", value="Important")
        
        filter_obj = SmartFilter(
            name="Test Filter",
            conditions=[condition],
            actions=[action],
            priority=1
        )
        
        assert filter_obj.name == "Test Filter"
        assert len(filter_obj.conditions) == 1
        assert len(filter_obj.actions) == 1
        assert filter_obj.priority == 1
        assert filter_obj.enabled is True
    
    def test_filter_with_multiple_conditions(self):
        """Test filter with multiple conditions."""
        cond1 = FilterCondition(field="sender", operator="equals", value="test@example.com")
        cond2 = FilterCondition(field="subject", operator="contains", value="urgent")
        action = FilterAction(type="label", value="Urgent")
        
        filter_obj = SmartFilter(
            name="Multi-condition Filter",
            conditions=[cond1, cond2],
            actions=[action]
        )
        
        assert len(filter_obj.conditions) == 2
    
    def test_filter_with_multiple_actions(self):
        """Test filter with multiple actions."""
        condition = FilterCondition(field="sender", operator="contains", value="spam")
        action1 = FilterAction(type="move", value="Spam")
        action2 = FilterAction(type="label", value="Junk")
        
        filter_obj = SmartFilter(
            name="Multi-action Filter",
            conditions=[condition],
            actions=[action1, action2]
        )
        
        assert len(filter_obj.actions) == 2
    
    def test_filter_enabled_disabled(self):
        """Test filter enable/disable state."""
        condition = FilterCondition(field="sender", operator="equals", value="test@example.com")
        action = FilterAction(type="delete")
        
        filter_obj = SmartFilter(
            name="Disabled Filter",
            conditions=[condition],
            actions=[action],
            enabled=False
        )
        
        assert filter_obj.enabled is False
    
    def test_filter_priority_ordering(self):
        """Test filters can be ordered by priority."""
        cond = FilterCondition(field="sender", operator="equals", value="test@example.com")
        act = FilterAction(type="move", value="Test")
        
        filter1 = SmartFilter(name="High Priority", conditions=[cond], actions=[act], priority=1)
        filter2 = SmartFilter(name="Low Priority", conditions=[cond], actions=[act], priority=10)
        
        assert filter1.priority < filter2.priority
    
    def test_filter_matches_email_simple(self):
        """Test filter matching against email."""
        condition = FilterCondition(field="sender", operator="equals", value="test@example.com")
        action = FilterAction(type="move", value="Important")
        filter_obj = SmartFilter(name="Test", conditions=[condition], actions=[action])
        
        email = {"sender": "test@example.com", "subject": "Test Email"}
        assert filter_obj.matches(email) is True
        
        email2 = {"sender": "other@example.com", "subject": "Test Email"}
        assert filter_obj.matches(email2) is False
    
    def test_filter_serialization(self):
        """Test filter serialization to dict."""
        condition = FilterCondition(field="sender", operator="equals", value="test@example.com")
        action = FilterAction(type="move", value="Archive")
        filter_obj = SmartFilter(name="Test Filter", conditions=[condition], actions=[action], priority=5)
        
        data = filter_obj.to_dict()
        
        assert data["name"] == "Test Filter"
        assert data["priority"] == 5
        assert data["enabled"] is True
        assert len(data["conditions"]) == 1
        assert len(data["actions"]) == 1
    
    def test_filter_from_dict(self):
        """Test creating filter from dictionary."""
        data = {
            "name": "Test Filter",
            "priority": 3,
            "enabled": True,
            "conditions": [
                {"field": "sender", "operator": "contains", "value": "test"}
            ],
            "actions": [
                {"type": "label", "value": "Test"}
            ]
        }
        
        filter_obj = SmartFilter.from_dict(data)
        
        assert filter_obj.name == "Test Filter"
        assert filter_obj.priority == 3
        assert len(filter_obj.conditions) == 1
        assert len(filter_obj.actions) == 1


class TestSmartFilterManager:
    """Test suite for SmartFilterManager class."""
    
    @pytest.fixture
    def manager(self):
        """Fixture providing a fresh filter manager."""
        return SmartFilterManager()
    
    @pytest.fixture
    def sample_filter(self):
        """Fixture providing a sample filter."""
        condition = FilterCondition(field="sender", operator="equals", value="test@example.com")
        action = FilterAction(type="move", value="Important")
        return SmartFilter(name="Sample Filter", conditions=[condition], actions=[action])
    
    def test_create_manager(self, manager):
        """Test creating a filter manager."""
        assert manager is not None
        assert len(manager.filters) == 0
    
    def test_add_filter(self, manager, sample_filter):
        """Test adding a filter to manager."""
        filter_id = manager.add_filter(sample_filter)
        
        assert filter_id is not None
        assert len(manager.filters) == 1
        assert manager.get_filter(filter_id) == sample_filter
    
    def test_add_multiple_filters(self, manager):
        """Test adding multiple filters."""
        cond = FilterCondition(field="sender", operator="equals", value="test@example.com")
        act = FilterAction(type="move", value="Test")
        
        filter1 = SmartFilter(name="Filter 1", conditions=[cond], actions=[act], priority=1)
        filter2 = SmartFilter(name="Filter 2", conditions=[cond], actions=[act], priority=2)
        filter3 = SmartFilter(name="Filter 3", conditions=[cond], actions=[act], priority=3)
        
        id1 = manager.add_filter(filter1)
        id2 = manager.add_filter(filter2)
        id3 = manager.add_filter(filter3)
        
        assert len(manager.filters) == 3
        assert id1 != id2 != id3
    
    def test_remove_filter(self, manager, sample_filter):
        """Test removing a filter."""
        filter_id = manager.add_filter(sample_filter)
        assert len(manager.filters) == 1
        
        manager.remove_filter(filter_id)
        assert len(manager.filters) == 0
    
    def test_get_filter(self, manager, sample_filter):
        """Test retrieving a filter by ID."""
        filter_id = manager.add_filter(sample_filter)
        retrieved = manager.get_filter(filter_id)
        
        assert retrieved == sample_filter
        assert retrieved.name == "Sample Filter"
    
    def test_get_nonexistent_filter(self, manager):
        """Test retrieving a non-existent filter."""
        result = manager.get_filter("nonexistent-id")
        assert result is None
    
    def test_update_filter(self, manager, sample_filter):
        """Test updating a filter."""
        filter_id = manager.add_filter(sample_filter)
        
        updated_filter = SmartFilter(
            name="Updated Filter",
            conditions=sample_filter.conditions,
            actions=sample_filter.actions,
            priority=10
        )
        
        manager.update_filter(filter_id, updated_filter)
        retrieved = manager.get_filter(filter_id)
        
        assert retrieved.name == "Updated Filter"
        assert retrieved.priority == 10
    
    def test_list_filters(self, manager):
        """Test listing all filters."""
        cond = FilterCondition(field="sender", operator="equals", value="test@example.com")
        act = FilterAction(type="move", value="Test")
        
        filter1 = SmartFilter(name="Filter 1", conditions=[cond], actions=[act])
        filter2 = SmartFilter(name="Filter 2", conditions=[cond], actions=[act])
        
        manager.add_filter(filter1)
        manager.add_filter(filter2)
        
        all_filters = manager.list_filters()
        assert len(all_filters) == 2
    
    def test_filters_sorted_by_priority(self, manager):
        """Test filters are returned sorted by priority."""
        cond = FilterCondition(field="sender", operator="equals", value="test@example.com")
        act = FilterAction(type="move", value="Test")
        
        filter1 = SmartFilter(name="Low Priority", conditions=[cond], actions=[act], priority=10)
        filter2 = SmartFilter(name="High Priority", conditions=[cond], actions=[act], priority=1)
        filter3 = SmartFilter(name="Medium Priority", conditions=[cond], actions=[act], priority=5)
        
        manager.add_filter(filter1)
        manager.add_filter(filter2)
        manager.add_filter(filter3)
        
        sorted_filters = manager.get_sorted_filters()
        
        assert sorted_filters[0].name == "High Priority"
        assert sorted_filters[1].name == "Medium Priority"
        assert sorted_filters[2].name == "Low Priority"
    
    def test_apply_filters_to_email(self, manager):
        """Test applying filters to an email."""
        condition = FilterCondition(field="sender", operator="equals", value="test@example.com")
        action = FilterAction(type="label", value="Important")
        filter_obj = SmartFilter(name="Test Filter", conditions=[condition], actions=[action])
        
        manager.add_filter(filter_obj)
        
        email = {"sender": "test@example.com", "subject": "Test"}
        applied_actions = manager.apply_filters(email)
        
        assert len(applied_actions) > 0
        assert applied_actions[0].type == "label"
    
    def test_disabled_filters_not_applied(self, manager):
        """Test that disabled filters are not applied."""
        condition = FilterCondition(field="sender", operator="equals", value="test@example.com")
        action = FilterAction(type="move", value="Spam")
        filter_obj = SmartFilter(
            name="Disabled Filter",
            conditions=[condition],
            actions=[action],
            enabled=False
        )
        
        manager.add_filter(filter_obj)
        
        email = {"sender": "test@example.com", "subject": "Test"}
        applied_actions = manager.apply_filters(email)
        
        assert len(applied_actions) == 0
    
    def test_export_filters(self, manager, sample_filter):
        """Test exporting filters to dict format."""
        manager.add_filter(sample_filter)
        exported = manager.export_filters()
        
        assert isinstance(exported, list)
        assert len(exported) == 1
        assert exported[0]["name"] == "Sample Filter"
    
    def test_import_filters(self, manager):
        """Test importing filters from dict format."""
        filters_data = [
            {
                "name": "Imported Filter 1",
                "priority": 1,
                "enabled": True,
                "conditions": [{"field": "sender", "operator": "equals", "value": "test@example.com"}],
                "actions": [{"type": "move", "value": "Archive"}]
            },
            {
                "name": "Imported Filter 2",
                "priority": 2,
                "enabled": True,
                "conditions": [{"field": "subject", "operator": "contains", "value": "urgent"}],
                "actions": [{"type": "label", "value": "Urgent"}]
            }
        ]
        
        manager.import_filters(filters_data)
        
        assert len(manager.filters) == 2


class TestFilterEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_conditions_list(self):
        """Test filter with empty conditions list."""
        action = FilterAction(type="move", value="Test")
        with pytest.raises(ValueError):
            SmartFilter(name="Empty Conditions", conditions=[], actions=[action])
    
    def test_empty_actions_list(self):
        """Test filter with empty actions list."""
        condition = FilterCondition(field="sender", operator="equals", value="test@example.com")
        with pytest.raises(ValueError):
            SmartFilter(name="Empty Actions", conditions=[condition], actions=[])
    
    def test_invalid_priority(self):
        """Test filter with invalid priority."""
        condition = FilterCondition(field="sender", operator="equals", value="test@example.com")
        action = FilterAction(type="move", value="Test")
        
        with pytest.raises(ValueError):
            SmartFilter(name="Invalid Priority", conditions=[condition], actions=[action], priority=-1)
    
    def test_invalid_operator(self):
        """Test condition with invalid operator."""
        with pytest.raises(ValueError):
            FilterCondition(field="sender", operator="invalid_operator", value="test")
    
    def test_invalid_action_type(self):
        """Test action with invalid type."""
        with pytest.raises(ValueError):
            FilterAction(type="invalid_type", value="test")
    
    def test_filter_with_none_values(self):
        """Test handling of None values."""
        with pytest.raises(TypeError):
            FilterCondition(field=None, operator="equals", value="test")
    
    def test_manager_remove_nonexistent_filter(self):
        """Test removing a non-existent filter."""
        manager = SmartFilterManager()
        with pytest.raises(KeyError):
            manager.remove_filter("nonexistent-id")


class TestFilterOperators:
    """Test different filter operators."""
    
    def test_equals_operator(self):
        """Test equals operator."""
        condition = FilterCondition(field="sender", operator="equals", value="test@example.com")
        filter_obj = SmartFilter(
            name="Equals Test",
            conditions=[condition],
            actions=[FilterAction(type="label", value="Test")]
        )
        
        assert filter_obj.matches({"sender": "test@example.com"}) is True
        assert filter_obj.matches({"sender": "other@example.com"}) is False
    
    def test_contains_operator(self):
        """Test contains operator."""
        condition = FilterCondition(field="subject", operator="contains", value="urgent")
        filter_obj = SmartFilter(
            name="Contains Test",
            conditions=[condition],
            actions=[FilterAction(type="label", value="Test")]
        )
        
        assert filter_obj.matches({"subject": "This is urgent"}) is True
        assert filter_obj.matches({"subject": "Regular email"}) is False
    
    def test_starts_with_operator(self):
        """Test starts_with operator."""
        condition = FilterCondition(field="subject", operator="starts_with", value="RE:")
        filter_obj = SmartFilter(
            name="Starts With Test",
            conditions=[condition],
            actions=[FilterAction(type="label", value="Reply")]
        )
        
        assert filter_obj.matches({"subject": "RE: Previous email"}) is True
        assert filter_obj.matches({"subject": "New email"}) is False
    
    def test_ends_with_operator(self):
        """Test ends_with operator."""
        condition = FilterCondition(field="sender", operator="ends_with", value="@company.com")
        filter_obj = SmartFilter(
            name="Ends With Test",
            conditions=[condition],
            actions=[FilterAction(type="label", value="Company")]
        )
        
        assert filter_obj.matches({"sender": "user@company.com"}) is True
        assert filter_obj.matches({"sender": "user@other.com"}) is False
    
    def test_regex_operator(self):
        """Test regex operator."""
        condition = FilterCondition(field="subject", operator="regex", value=r"\d{3}-\d{4}")
        filter_obj = SmartFilter(
            name="Regex Test",
            conditions=[condition],
            actions=[FilterAction(type="label", value="Has Number")]
        )
        
        assert filter_obj.matches({"subject": "Order 123-4567"}) is True
        assert filter_obj.matches({"subject": "No number here"}) is False


class TestFilterCombinations:
    """Test combinations of filters and conditions."""
    
    def test_multiple_conditions_all_match(self):
        """Test filter with all conditions matching."""
        cond1 = FilterCondition(field="sender", operator="contains", value="example.com")
        cond2 = FilterCondition(field="subject", operator="contains", value="urgent")
        
        filter_obj = SmartFilter(
            name="Multi Condition",
            conditions=[cond1, cond2],
            actions=[FilterAction(type="label", value="Important")]
        )
        
        email = {"sender": "user@example.com", "subject": "Urgent matter"}
        assert filter_obj.matches(email) is True
        
        email2 = {"sender": "user@example.com", "subject": "Regular matter"}
        assert filter_obj.matches(email2) is False
    
    def test_priority_based_execution(self):
        """Test filters execute in priority order."""
        manager = SmartFilterManager()
        
        # High priority filter
        cond1 = FilterCondition(field="sender", operator="contains", value="spam")
        filter1 = SmartFilter(
            name="Spam Filter",
            conditions=[cond1],
            actions=[FilterAction(type="move", value="Spam")],
            priority=1
        )
        
        # Low priority filter
        cond2 = FilterCondition(field="sender", operator="contains", value="@")
        filter2 = SmartFilter(
            name="All Email Filter",
            conditions=[cond2],
            actions=[FilterAction(type="label", value="Email")],
            priority=10
        )
        
        manager.add_filter(filter2)
        manager.add_filter(filter1)
        
        email = {"sender": "spam@example.com"}
        actions = manager.apply_filters(email)
        
        # Spam filter should execute first
        assert actions[0].type == "move"
        assert actions[0].value == "Spam"