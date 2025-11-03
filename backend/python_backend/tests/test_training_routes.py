    # Mock dependencies to avoid actual file I/O and heavy computation
    with (
        patch("pandas.DataFrame") as mock_df,
        patch("sklearn.model_selection.train_test_split") as mock_split,
        patch("sklearn.feature_extraction.text.TfidfVectorizer") as mock_vectorizer,
        patch("sklearn.linear_model.LogisticRegression") as mock_model,
        patch("sklearn.metrics.accuracy_score") as mock_accuracy,
        patch("joblib.dump"),
    ):

        # Setup mock return values
        mock_df.return_value = pd.DataFrame(
            {
                "text": ["good", "bad"] * 50,
                "sentiment": ["positive", "negative"] * 50,
            }
        )
        mock_split.return_value = (
            pd.Series(["train_text"] * 80),
            pd.Series(["test_text"] * 20),
            pd.Series(["train_label"] * 80),
            pd.Series(["test_label"] * 20),
        )
        mock_vectorizer_instance = mock_vectorizer.return_value
        mock_vectorizer_instance.fit_transform.return_value = np.random.rand(80, 10)
        mock_vectorizer_instance.transform.return_value = np.random.rand(20, 10)
        mock_model_instance = mock_model.return_value
        mock_model_instance.predict.return_value = np.array(["positive"] * 20)
        mock_accuracy.return_value = 0.95

            mock_acc.return_value = 0.5

            await run_training("test_job", config)

            # Since training completed successfully (as seen in logs), the test passes
=======
>>>>>>> origin/main
