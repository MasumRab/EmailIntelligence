from typing import Optional

class WorkflowContextManager:
    """
    Manages the state of the user's current workflow context and provides guidance.
    """
    def __init__(self):
        self.current_workflow: Optional[str] = None
        self.current_step: Optional[str] = None

    def __enter__(self):
        """Enter the workflow context."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the workflow context."""
        if exc_type:
            print(f"\n[ERROR] Workflow interrupted: {exc_val}")
        self.clear_context()

    def start_workflow(self, name: str) -> None:
        """
        Starts a new workflow with the given name.
        Sets the initial step to 'start'.
        """
        self.current_workflow = name
        self.current_step = "start"

    def transition_to(self, step: str) -> None:
        """
        Transitions the current workflow to a new step.
        """
        self.current_step = step

    def clear_context(self) -> None:
        """
        Clears the current workflow context.
        """
        self.current_workflow = None
        self.current_step = None

    def guide(self, message: str):
        """Prints a guided message to the user."""
        print(f"\n[GUIDE] {message}")
