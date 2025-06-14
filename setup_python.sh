#!/bin/bash
# ##############################################################################
# # DEPRECATION NOTICE                                                         #
# ##############################################################################
# # This script (setup_python.sh) is DEPRECATED and should no longer be used.  #
# # It may be removed in future versions.                                      #
# #                                                                            #
# # Please use the main launcher script `launch.py` for all environment setup  #
# # and application management tasks:                                          #
# #                                                                            #
# # python launch.py --stage dev                                               #
# #                                                                            #
# # `launch.py` handles virtual environment creation, dependency installation, #
# # NLTK data downloads, and more. Refer to README_ENV_MANAGEMENT.md for       #
# # details.                                                                   #
# ##############################################################################
# # Proceeding with this script is not recommended.                            #
# ##############################################################################
echo "WARNING: This script (setup_python.sh) is DEPRECATED." >&2
echo "WARNING: Please use 'python launch.py' instead for environment setup." >&2
echo "WARNING: Continuing in 5 seconds..." >&2
sleep 5

# Exit on error
set -e

PYTHON_ALIAS="python3" # Or python, if python3 is not standard
VENV_DIR=".venv"

# Check if Python 3 is installed
if ! command -v $PYTHON_ALIAS &> /dev/null
then
    echo "$PYTHON_ALIAS could not be found. Please install Python 3."
    exit 1
fi

# Check if pip is installed
if ! $PYTHON_ALIAS -m pip --version &> /dev/null
then
    echo "pip could not be found. Please ensure pip is installed for $PYTHON_ALIAS."
    exit 1
fi

echo "Creating virtual environment in $VENV_DIR..."
$PYTHON_ALIAS -m venv $VENV_DIR

echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Setting up NLTK data (stopwords)..."
$PYTHON_ALIAS -m nltk.downloader stopwords

echo "Training placeholder AI models..."
# This part assumes ai_training.py can be modified or called to produce
# the specifically named model files, or we rename them after generation.
# For now, we'll call the script and then rename based on typical output.
# This might need adjustment based on actual output of ai_training.py's main().

# Path to the training script (relative to project root)
AI_TRAINING_SCRIPT="server/python_nlp/ai_training.py"
MODEL_DIR="server/python_nlp" # Where nlp_engine.py expects models

# Run a generic training command (assuming it creates models for different types)
# We'll need to refine this if ai_training.py needs specific arguments for each model type.
echo "Running AI training script (this might take a moment)..."
# The current ai_training.py main() trains only one model (topic) and saves it with a dynamic ID.
# We need to ensure models for sentiment, intent, and urgency are also generated and named correctly.
# For this subtask, we'll assume a simplified approach:
# If ai_training.py's main function can be made to produce these specific files, that's ideal.
# Otherwise, the setup script demonstrates the call and required files.

# Placeholder for actual training calls that would generate the needed models.
# The user will likely need to adapt ai_training.py or this section.
echo "INFO: The following model training is a placeholder."
echo "INFO: You may need to adapt server/python_nlp/ai_training.py to generate all required model types"
echo "INFO: (sentiment_model.pkl, topic_model.pkl, intent_model.pkl, urgency_model.pkl)"
echo "INFO: and place them in the $MODEL_DIR directory."

# Example of running the script (actual model output might vary)
# $PYTHON_ALIAS $AI_TRAINING_SCRIPT

# As the current ai_training.py main() saves one model with a dynamic ID,
# e.g., model_xxxxxxxxxxxx.pkl, we cannot reliably rename it to all four required names.
# For now, we will create dummy placeholder files for the models that nlp_engine.py expects,
# to allow the application to run without immediate errors due to missing files.
# The user MUST replace these with actual trained models.

echo "Creating dummy placeholder model files in $MODEL_DIR..."
echo "IMPORTANT: These are DUMMY models. Replace them with actual trained models for the application to function correctly."

touch "$MODEL_DIR/sentiment_model.pkl"
touch "$MODEL_DIR/topic_model.pkl"
touch "$MODEL_DIR/intent_model.pkl"
touch "$MODEL_DIR/urgency_model.pkl"

# We can try to run the default main from ai_training.py to get at least one model created by the script.
# And then inform the user that other models are dummies.
echo "Attempting to train one sample model using ai_training.py default main..."
if $PYTHON_ALIAS $AI_TRAINING_SCRIPT; then
    echo "INFO: ai_training.py ran. It might have created a model like 'model_xxxxxxxxxxxx.pkl' in the project root."
    echo "INFO: You will need to train models for sentiment, topic, intent, and urgency, "
    echo "INFO: then rename them to sentiment_model.pkl, topic_model.pkl, intent_model.pkl, urgency_model.pkl "
    echo "INFO: and place them in $MODEL_DIR."
else
    echo "WARNING: $AI_TRAINING_SCRIPT failed to run. Placeholder dummy models will be used."
fi


echo ""
echo "Python environment setup complete."
echo "To activate the virtual environment in your shell, run:"
echo "source $VENV_DIR/bin/activate"
echo ""
echo "IMPORTANT: The AI models currently in $MODEL_DIR are placeholders or samples."
echo "You need to train and place valid 'sentiment_model.pkl', 'topic_model.pkl', 'intent_model.pkl', and 'urgency_model.pkl' files in $MODEL_DIR for the NLP features to work correctly."
