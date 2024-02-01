
# Turnieje w systemie pucharowym Bartosz Wiecheć 

## ISTOTNE!

W systemie utworzone są dwa konta ułatwiające testowanie:

Admin: 
- login: aa
- hasło: aa
 
Zwykły user:
- login: adc
- hasło: adc

Przed wysłaniem z bazy zostały usunięte wszystkie turnieje.

## Wymagania 

Kryterium oraz jakim stopniu spełnione

Użytkownik rejestruje się w aplikacji podając dane, takie jak adres email, 
nazwa, data urodzenia, hasło: Wszystkie wymienione opcje

Użytkownik loguje/wylogowuje się z aplikacji: __Poprawnie działające logowanie i wylogowywanie__

Użytkownik tworzy nowy turniej podając jego nazwę, datę i godzinę rozpoczęcia oraz 
maksymalną ilość graczy: __Możliwość utworzenia turnieju z podanymi danymi__

Użytkownik usuwa turniej z systemu: __Jest opcja usuwania__

Użytkownik dodaje nowych graczy i przyporządkowuje je do określonego turnieju: __Możliwość dodawania gracza i przyporządkowywania go do turnieju.__

Użytkownik wpisuje wyniki pojedynków w kolejnych fazach turnieju: __Wpisywanie wyników w konkretnych fazach__

Użytkownik przegląda historyczne turnieje z określonego przedziału czasu: __Filtrowanie turniejów po określonych przedziałach czasowych__

Parowanie graczy w pierwszej fazie turnieju jest losowe: __Jest losowe__

Aplikacja stosuje podział uprawnień względem różnych użytkowników: __Modyfikacja dostępu zależnie od użytkownika__

Użytkownik anonimowy posiada uprawnienia tylko do przeglądania rozpoczętych turniejów: __Anonimowy widzi tylko rozpoczęte__

Użytkownik zwykły zarządza turniejami przez siebie utworzonymi, przy czym nie ma możliwości
usuwania i edycji turnieju gdy ten już się rozpoczął: __Użytkownik nie edytuje turnieju po jego rozpoczęciu__

## Dodatkowe walory aplikacji:
- Oprócz podstrony z wszystkimi truniejami istnieją dodatkowe:
    - rozpoczęte turnieje
    - zakończone
    - otwarte do rejestracji
    - utworzone przez użytkownika
    - turnieje, w których użytkownik bierze udział
    we wszystkich podstronach istnieje możliwość filtrowania po datach
- Jeśli turniej został zadeklarowany na 32 użytkowników, a zapisanych będzie 15, turniej skróci drabinkę do 16 uczestników.
- Użytkownik może dodawać osoby tylko do swoich turniejów jeśli nie jest superuserem oraz tylko w swoich turniejach wpisywać
    wyniki jeśli nie jest superuserem
- Do turnieju można dodać tylko zarejestrowanych graczy.
