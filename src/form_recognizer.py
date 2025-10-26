#Importujemy potrzebne biblioteki Pythona
import os #pozwala pracować z systemem operacyjnym (zmienne środowiskowe)
import requests  # biblioteka do pobierania plików z GitHub (lub innych HTTP)
from azure.ai.formrecognizer import DocumentAnalysisClient # klient do analizy dokumentów przy użyciu Azure Form Recognizer (OCR, ekstrakcja danych)
from azure.core.credentials import AzureKeyCredential # zarządza uwierzytelnianiem do usług Azure (klucz API)
from dotenv import load_dotenv # ładuje zmienne środowiskowe z pliku .env do os.environ

# Wczytanie zmiennych z .env
load_dotenv()
endpoint = os.getenv("FORM_RECOGNIZER_ENDPOINT")
key = os.getenv("FORM_RECOGNIZER_KEY")
# przypominajka - żeby utworzyć .env z kluczem i endpoint do Azure
if not endpoint or not key:
    raise ValueError("Nie ustawiono FORM_RECOGNIZER_ENDPOINT lub FORM_RECOGNIZER_KEY w .env")

# Utworzenie klienta do Azzure Form Recognizer
client = DocumentAnalysisClient(
    endpoint=endpoint, 
    credential=AzureKeyCredential(key)
    )

# Pobieranie dokumentu - dwa rozwiązania - do decyzji, który zostawimy finalnie:
# 1. Folder z dokumentami utworzony lokalnie
DATASET_PATH = os.path.join(os.path.dirname(__file__), "../data/test_docs") # trzeba podać ścieżkę lokalną (jeśli dokumnety sa zapisane lokalnie)

# 2. Funkcja do pobierania dokumentów bezpośrednio z datasetu zamieszczonego na GitHub
# Bez klonowania repozytorium. Pobiera plik z GitHub i zapisuje tymczasowo lokalnie. Zwraca ścieżkę do pobranego pliku.
def download_file_from_github(url, local_filename="temp_document"):
    response = requests.get(url) #pobiera plik z URL
    if response.status_code != 200: # jeśli błąd HTTP (200 jest kodem 'OK')
        raise ValueError(f"Nie udało się pobrać pliku: {url}") # przerwij z komunikatem błędu

    # Automatycznie wykrywa i dodaje rozszerzenie pilku z URL
    # Po co? Ponieważ plik jest pobierany tymczasowo lokalnie, a zapisanie go z właściwym rozszerzeniem 
    # pozwala bibliotece Azure Form Recognizer poprawnie rozpoznać jego typ
    if "." in url.split("/")[-1]: ## sprawdza czy ostatnia część URL (nazwa pliku) zawiera kropkę (oznaka rozszerzenia)
        ext = url.split("/")[-1].split(".")[-1] # wyciąga rozszerzenie
        local_filename += f".{ext}" # dodaje rozszerzenie do nazwy lokalnego pliku

    with open(local_filename, "wb") as f: # otwiera plik w trybie zapisu binarnego (konieczny dla plików nie-tekstowych, np. PDF)
        f.write(response.content) # zapisuje zawartość do pliku lokalnego

    return local_filename # zwraca ścieżkę do zapisanego pliku

# Główna funkcja analizująca dokument
# Część, która została napisana - dot. obsługi dokumentów PDF/DOCS zapisanych
# w różnych źródłach (lokalnie i zdlanie) z automatycznym zarządzaniem ścieżkami
# dwa rozwiązania i walidacja - czy plik istnieje
def analyze_document(file_path_or_url):
    # Obsługa plików z GitHub
    if file_path_or_url.startswith("http"): # tu należy wpisać ścieżkę do dokumentów na GitHub
        file_path = download_file_from_github(file_path_or_url)
        remove_after = True  # usuwa plik tymczasowy po zakończeniu analizy
    # Obsługa plików zapisanych lokalnie
    else:
        # jeśli podano tylko nazwę pliku, dołącz do folderu DATASET_PATH
        if not os.path.isabs(file_path_or_url):
            file_path = os.path.join(DATASET_PATH, file_path_or_url)
        else:
            file_path = file_path_or_url
        remove_after = False # nie usuwa plików lokalnych po analizie

    # Walidacja - czy plik istnieje
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Plik nie istnieje: {file_path}") # informacja o błędzie

    # Analiza dokumentu przez Form Recognizer
    # otwiera plik i wysyła do Azure
    try:
        with open(file_path, "rb") as f:
            poller = client.begin_analyze_document(
                "prebuilt-document",  # model do ogólnej analizy dokumentów
                document=f
            )
        
        result = poller.result()  # czeka na wynik analizy
        
        # Wydobycie całego tekstu z dokumentu
        extracted_text = ""
        for page in result.pages:
            for line in page.lines:
                extracted_text += line.content + "\n"
        
        return extracted_text
    # Usuwa plik tymczasowy jeśli był pobrany z GitHub
    finally:
        if remove_after and os.path.exists(file_path):
            os.remove(file_path)
