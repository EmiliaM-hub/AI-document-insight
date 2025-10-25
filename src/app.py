#Importujemy potrzebne biblioteki Pythona
import os #pozwala pracować z systemem operacyjnym (zmienne środowiskowe)
from src.form_recognizer import analyze_document # funkcja do analizy dokumentów (ekstrakcja tekstu)
from src.openai_summarizer import summarize_text # funkcja do generowania streszczeń tekstu przy użyciu OpenAI API
import gradio as gr # biblioteka do tworzenia interfejsów webowych/GUI dla modeli ML (proste demo aplikacji)

# Funkcja główna - analiza dokumentu i generowanie streszczenia

