    assert (
        activate_response.json()["message"] == "Active legacy workflow set to 'example_uppercase'."
    )

    # 2. Prepare the email data
    new_email_data = {
        "sender": "plugin.test@example.com",
        "senderEmail": "plugin.test@example.com",
        "subject": "a subject to be uppercased",
        "content": "This is a test of the plugin workflow.",
        "time": datetime.now().isoformat(),
    }

    # The database create_email method needs to be mocked to return a valid email dictionary
    # The real workflow will add 'workflow_status' and change the subject.
    processed_data = new_email_data.copy()
    processed_data["subject"] = "A SUBJECT TO BE UPPERCASED"
    processed_data["workflow_status"] = "processed_by_example_uppercase_workflow"

    # We need to mock the return value from the db create call
    mock_db_manager.create_email.return_value = create_mock_email(10, **processed_data)

    # 3. Create the email, which will trigger the newly activated workflow
    create_response = client_with_real_workflows.post("/api/emails", json=new_email_data)

    # 4. Assert that the workflow was correctly applied
    assert create_response.status_code == 200
    response_data = create_response.json()
    assert response_data["subject"] == "A SUBJECT TO BE UPPERCASED"

    # Also assert that the AI engine was NOT called, since the uppercase workflow doesn't use it
    mock_ai_engine.analyze_email.assert_not_called()
=======
>>>>>>> origin/main
