# AI-document-insight
Asystent AI do analizy dokumentów (PDF, DOCX), który automatycznie generuje streszczenia i listy kluczowych punktów.  
Projekt realizowany z wykorzystaniem **Azure Form Recognizer SDK** oraz **Azure OpenAI SDK**.

## Cel
celem jest stworzenie asystenta biurowego, który przekształca długie dokumenty w krótkie podsumowania.

## Zakres prac
1. Przygotowanie zestawu dokumentów testowych (wykorzystane zostały doc z https://www.kaggle.com/datasets) 
2. Konfiguracja i użycie **Azure Form Recognizer SDK**
3. Integracja z **Azure OpenAI SDK** (generacja streszczeń i kluczowych punktów)
4. Testy jakości (trafność, kompletność streszczeń)
5. Stworzenie interfejsu demo (upload PDF → streszczenie) z użyciem **Gradio**
6. Dokumentacja i prezentacja

## Struktura projektu
- data/test_docs/ # dokumenty testowe
- src/ # kod źródłowy aplikacji:
    - app.py
    - form_recognizer.py
    - openai_summarizer.py
    - utils.py
- requirements.txt
- README.md