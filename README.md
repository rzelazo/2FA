# 2FA

## Szablon aplikacji webowej implementującej mechanizm uwierzytelniania dwuetapowego. 
Jako drugi czynnik uwierzytelniający zastosowano weryfikację za pomocą kodu weryfikacyjnego wysyłanego użytkownikowi w postaci wiadomości SMS.

### Wykorzystywana technologia:
#### Serwer:
- [Python 3.9](https://www.python.org/downloads/release/python-390/)
- [Django 3.2.5](https://pypi.org/project/Django/3.2.5/)
- [python-decouple 3.6](https://pypi.org/project/python-decouple/3.6) -> separacja wrażliwych danych z kodu serwera (np. tokena do wykorzystywanego API Twilio lub SECRET KEY serwera Django)
- [django-crispy-forms 1.8.1](https://pypi.org/project/django-crispy-forms/1.8.1/)

#### Biblioteka umożliwiająca wysyłanie wiadomości SMS do użytkownika za pośrednictwem serwisu [Twilio](https://www.twilio.com/):
- [twilio 7.9.1](https://pypi.org/project/twilio/7.9.1/)


## Instrukcja uruchomienia serwera
Wymienione komendy wykonywane są przy założeniu, że znajdujemy się w folderze root projektu (czyli folderze zawierającym foldery TwoFactorAuth, codes, templates, users oraz pliki manage.py i requirements.txt).

### 1. Pobranie wymaganych zależności wyszczególnionych w pliku [requirements.txt](https://github.com/rzelazo/2FA/blob/main/requirements.txt).
```
pip install -r requirements.txt
```
### 2. Utworzenie w folderze root projektu pliku konfiguracyjnego ".env" przechowującego zmienne środowiskowe wykorzystywane przez serwer.
```
touch .env
```
### 3. Zdefiniowanie zmiennych środowiskowych wykorzystywanych przez serwer w pliku .env
Należy edytować plik .env i umieścić w nim następujące zmienne środowiskowe:
```
DJANGO_SECRET_KEY=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
```
- #### Zmienna DJANGO_SECRET_KEY
Wartość zmiennej DJANGO_SECRET_KEY wygenerować możemy w konsoli Django:
```
from django.core.management.utils import get_random_secret_key  
get_random_secret_key()
```
Zwróconą przez funkcję wartość należy przypisać do zmiennej DJANGO_SECRET_KEY w pliku .env

- #### Zmienne TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
Wartości powyższych zmiennych uzyskać można w zakładce console zakładając darmowe konto próbne na stronie serwisu Twilio ([rejestracja](https://www.twilio.com/try-twilio) wymaga jedynie podania adresu email). 
Po zalogowaniu i przeklikaniu przez wstęp wymagane wartości dostępne będą w zakładce [*console* serwisu Twilio](https://console.twilio.com/) w sekcji *Account Info*.
![image](https://user-images.githubusercontent.com/62251572/170882138-b9446e60-de9e-45b0-80e0-10b3e8cdbdf2.png)

### 4. Utworzenie bazy danych serwera (SQLite3) na podstawie plików migracji z folderów migrations projektu
W konsoli systemowej (znajdując się w folderze root projektu) należy wywołać polecenie:
```
python manage.py migrate
```
### 5. Uruchomienie serwera
Jeśli wszystko poszło pomyślnie, możemy uruchomić serwer w konsoli systemowej wywołując polecenie:
```
python manage.py runserver <numer portu>
```
gdzie `<numer portu>` jest opcjonalnym parametrem definiującym to, na którym porcie chcemy uruchomić serwer.

## Prezentacja działania programu

### Strona logowania - pierwszy etap uwierzytelniania:
![image](https://user-images.githubusercontent.com/62251572/170883022-2fcd0d89-8aae-4ee7-8bc6-5af5c53ab5ea.png)

### Strona weryfikacji kodu SMS - drugi etap uwierzytelniania:
![image](https://user-images.githubusercontent.com/62251572/170883192-7f8576b5-ade3-4a95-a204-7590a0f4c595.png)

#### W tym momencie serwer wysyła do użytkownika próbującego się zalogować wiadomość SMS z jednorazowym kodem weryfikacyjnym:
![image](https://user-images.githubusercontent.com/62251572/170883237-5e901f81-b559-494b-8ea9-5e520bc54041.png)

#### Użytkownik wprowadza do odpowiedniego okna kod otrzymany w wiadomości:
![image](https://user-images.githubusercontent.com/62251572/170883273-28594da0-4930-474b-8c9a-0be784aae545.png)

### Jeżeli wprowadzony kod weryfikacyjny jest poprawny - użytkownik zostaje zalogowany do bieżącej sesji i uzyskuje dostęp do serwisu:
![image](https://user-images.githubusercontent.com/62251572/170883378-1a5f0d43-8e79-4676-94ee-f5654fae3af1.png)

### Jeżeli wprowadzony kod weryfikacyjny nie jest poprawny - wygenerowany zostaje nowy kod weryfikacyjny, a stary zostaje unieważniony:
Nowo wygenerowany kod wysyłany jest do użytkownika w kolejnej wiadomości SMS
![image](https://user-images.githubusercontent.com/62251572/170883505-ea041e6e-0f8a-491e-aaf8-10ce9ba7dd1c.png)

### Strona rejestracji nowego użytkownika:
(wymaga podania numeru telefonu, na który wysyłane będą wiadomości SMS z kodem weryfikacyjnym)
![image](https://user-images.githubusercontent.com/62251572/170883632-debe8cb8-29d2-424d-8804-c590bc38f843.png)

### Rejestracja nowego użytkownika wymaga weryfikacji podanego numeru telefonu w sposób analogiczny do działania drugiego czynnika uwierzytelniania:
![image](https://user-images.githubusercontent.com/62251572/170883760-f28042d8-ec75-4516-b0da-c8cfc99aa12b.png)
![image](https://user-images.githubusercontent.com/62251572/170883794-87aaa4c8-b64c-4367-8926-143888cb077a.png)
![image](https://user-images.githubusercontent.com/62251572/170883809-2b69072c-082f-49df-8f53-cffc9c58161e.png)

### Po pomyślnym zarejestrowaniu nowy użytkownik zostaje zalogowany do bieżącej sesji i uzyskuje dostęp do serwisu:
![image](https://user-images.githubusercontent.com/62251572/170883857-d1c2f173-16f2-4a24-b6f1-d2873b3995e2.png)
