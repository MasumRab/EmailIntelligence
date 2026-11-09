import pytest

from backend.node_engine.security_manager import SecurityManager


# Mock Workflow class for testing
class MockWorkflow:
    def __init__(
        self,
        workflow_id: str,
        name: str,
        owner_id: str,
        is_safe: bool = False,
        is_public: bool = False,
    ):
        self.workflow_id = workflow_id
        self.name = name
        self.owner_id = owner_id
        self.is_safe = is_safe
        self.is_public = is_public
        self.__tablename__ = "workflows"  # Mimic SQLAlchemy table name


# Mock User class for testing
class MockUser:
    def __init__(self, user_id: str):
        self.id = user_id


@pytest.fixture
def security_manager_fixture():
    user_roles = {
        "admin_user": ["admin"],
        "editor_user": ["editor", "user"],
        "basic_user": ["user"],
        "owner_user": ["user"],
        "anonymous": ["guest"],
    }
    return SecurityManager(user_roles)


def test_admin_has_all_permissions(security_manager_fixture):
    sm = security_manager_fixture
    admin_user = MockUser("admin_user")
    workflow = MockWorkflow("wf1", "Test Workflow", "owner_user", is_safe=False)

    assert sm.has_permission(admin_user, "execute", workflow) is True
    assert sm.has_permission(admin_user, "edit", workflow) is True
    assert sm.has_permission(admin_user, "view", workflow) is True
    assert sm.has_permission(admin_user, "non_existent_action", None) is True


def test_editor_can_execute_safe_workflow(security_manager_fixture):
    sm = security_manager_fixture
    editor_user = MockUser("editor_user")
    safe_workflow = MockWorkflow("wf2", "Safe Workflow", "owner_user", is_safe=True)
    unsafe_workflow = MockWorkflow("wf3", "Unsafe Workflow", "owner_user", is_safe=False)

    assert sm.has_permission(editor_user, "execute", safe_workflow) is True
    assert sm.has_permission(editor_user, "execute", unsafe_workflow) is False


def test_editor_can_edit_owned_workflow(security_manager_fixture):
    sm = security_manager_fixture
    editor_user = MockUser("editor_user")
    owned_workflow = MockWorkflow("wf4", "Owned Workflow", "editor_user")
    other_workflow = MockWorkflow("wf5", "Other Workflow", "another_user")

    assert sm.has_permission(editor_user, "edit", owned_workflow) is True
    assert (
        sm.has_permission(editor_user, "edit", other_workflow) is True
    )  # Editors can edit any workflow


def test_basic_user_cannot_execute_or_edit(security_manager_fixture):
    sm = security_manager_fixture
    basic_user = MockUser("basic_user")
    workflow = MockWorkflow("wf6", "Basic Workflow", "owner_user", is_safe=True)

    assert sm.has_permission(basic_user, "execute", workflow) is False
    assert sm.has_permission(basic_user, "edit", workflow) is False


def test_basic_user_can_view_public_workflow(security_manager_fixture):
    sm = security_manager_fixture
    basic_user = MockUser("basic_user")
    public_workflow = MockWorkflow("wf7", "Public Workflow", "owner_user", is_public=True)
    private_workflow = MockWorkflow("wf8", "Private Workflow", "owner_user", is_public=False)

    assert sm.has_permission(basic_user, "view", public_workflow) is True
    assert sm.has_permission(basic_user, "view", private_workflow) is False


def test_owner_can_execute_and_edit_their_workflow(security_manager_fixture):
    sm = security_manager_fixture
    owner_user = MockUser("owner_user")
    owned_workflow = MockWorkflow("wf9", "Owned Workflow", "owner_user", is_safe=False)
    other_workflow = MockWorkflow("wf10", "Other Workflow", "another_user", is_safe=True)

    assert (
        sm.has_permission(owner_user, "execute", owned_workflow) is True
    )  # Owner can execute their own, even if not safe
    assert sm.has_permission(owner_user, "edit", owned_workflow) is True
    assert sm.has_permission(owner_user, "execute", other_workflow) is False
    assert sm.has_permission(owner_user, "edit", other_workflow) is False


def test_anonymous_user_no_permissions(security_manager_fixture):
    sm = security_manager_fixture
    anonymous_user = MockUser("anonymous")
    workflow = MockWorkflow("wf11", "Anon Workflow", "owner_user", is_safe=True, is_public=False)

    assert sm.has_permission(anonymous_user, "execute", workflow) is False
    assert sm.has_permission(anonymous_user, "edit", workflow) is False
    assert sm.has_permission(anonymous_user, "view", workflow) is False


def test_no_user_id_returns_false(security_manager_fixture):
    sm = security_manager_fixture

    class UserWithoutId:
        pass

    user_no_id = UserWithoutId()
    workflow = MockWorkflow("wf12", "No ID Workflow", "owner_user")

    assert sm.has_permission(user_no_id, "execute", workflow) is False


def test_resource_not_workflow(security_manager_fixture):
    sm = security_manager_fixture
    editor_user = MockUser("editor_user")

    class OtherResource:
        pass

    other_resource = OtherResource()

    assert sm.has_permission(editor_user, "execute", other_resource) is False
