# tournament-manager

System do organizowania i zarządzania turniejami.

Do systemu dodawane są drużyny z podstawowymi informacjami jak nazwa i lista członków.
Drużyny mogą być dodawane do stworzonych turniejów / wysłać zgłoszenie.

Turnieje mogą być w formie tabel punktowych z meczami każdy z każdym (np. fazy grupowe w piłce nożnej), w formie drabinki turniejowej (losowane pary, zwycięzca przechodzi dalej).

Specjalni użytkownicy - sędziowie - mogą rozpoczynać mecze i w ich trakcie zaznaczać/dodawać otrzymane przez drużyny punkty, wyniki dostępne będą na żywo

Oprócz tego dostępne będą aktualne ogólne statystyki, tabele i drabinki dla poszczególnych turniejów.

Dodatkowo mechanizm misji, dodatkowych sposobów otrzymywania punktów opcjonalnych (zliczanych w osobnej tabeli, która nie wpływa na tą główną) lub kluczowych (liczonych do głównej punktacji wpływającej na przebieg turnieju), zależnie ustawień samego turnieju.

ewentualne CI / CD i zakładanie kont przez media społecznościowe

Wstępna, przykładowa lista modeli:

Game np. tenis, siatkówka, League of legends
    name (str)

Drużyna

- Zarządca drużyny (użytkownik)
- Nazwa (str)
- Lista członków drużyny ()

Zgłoszenie

- Nazwa drużyny (Drużyna)
- Nazwa turnieju (Tournament)
- Czy zaakceptowana (bool)

Tournament

- Nazwa (str)
- miejsce (str)
- Data startu turnieju
- Data końca turnieju
- forma rozgrywek np.(fazy grupowe / drabinka / faza grupowa + drabinka) (enum)
- domyślny czas meczu (optional, time?)
- Lista sędziów Referee (użytkowników)
- Lista drużyn

Mecz

- Drużyna A (Drużyna)
- Drużyna B (Drużyna)
- Wynik druzyny A (wynik)
- Wynik druzyny B (wynik)
- Winner (Drużyna)
- czy mecz skończony (bool)
- turniej (Tournament)
get_winner()

Wynik

- Wartość wyniku (float)
- czy wynik zatwierdzony przez sędziego (bool)

## TODO:

- [ ] Logowanie sie
- [ ] Rejestracja

## Strony

## MVP v0

- Strona do logowania
- Strona do rejestracji
- Strona Główna
  - przyciski zaloguj sie / zarejestruj lub wyloguj się (base_template)

## MVP v1

Dla zalogowanych:

1. Zalogować
2. Różne opcje działań
   - Stworzenie drużyny
   - Dołączanie do drużyny
   - Stworzenie turnieju
   - Zgłaszanie drużyny do turnieju
3. Modele potrzebne:
   - Użytkownik
   - Drużyna
   - Turniej
   - Sport
4. Strona główna
   - Lista turniejów przyszłych obecnych przeszłych

## MVP v2

    1. Generowanie drabinki itp.

## Commands

- `docker-compose exec web python3 manage.py startapp app_name`
- `docker-compose exec web python manage.py createsuperuser`
- `docker-compose exec web python manage.py makemigrations`
- `docker-compose exec web python manage.py migrate`
- `docker-compose up --build`
