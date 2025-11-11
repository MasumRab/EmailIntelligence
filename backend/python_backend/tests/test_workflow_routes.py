    assert (
        response_activate.json()["message"]
        == "Active legacy workflow set to 'my_brand_new_workflow'."
    )

    # 3. Verify the mocks were called as expected
    expected_config = new_workflow_config.copy()
    expected_config.update({"workflow_type": "legacy", "nodes": [], "connections": []})
    mock_workflow_engine.create_and_register_workflow_from_config.assert_called_once_with(
        expected_config
    )
    mock_workflow_engine.set_active_workflow.assert_called_with("my_brand_new_workflow")
=======
>>>>>>> origin/main
