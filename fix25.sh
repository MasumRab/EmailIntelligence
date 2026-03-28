cat << 'INNER_EOF' > /tmp/repl.txt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import gradio as gr
from backend.python_nlp.nlp_engine import NLPEngine

topic_chart = None
sentiment_chart = None
INNER_EOF
sed -i '2,10d' src/backend/python_backend/gradio_app.py
sed -i -e '/import json/r /tmp/repl.txt' src/backend/python_backend/gradio_app.py
