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
sed -i -e '/import gradio as gr/d' -e '/import pandas as pd/d' -e '/import plotly.express as px/d' -e '/import plotly.graph_objects as go/d' -e '/import requests/d' -e '/from backend.python_nlp.nlp_engine import NLPEngine/d' -e '/topic_chart = None/d' -e '/sentiment_chart = None/d' src/backend/python_backend/gradio_app.py
sed -i '1r /tmp/repl.txt' src/backend/python_backend/gradio_app.py
