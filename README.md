# Stolarnia_uWuja
## Opis aplikacji
<p align="justify">
&emsp; Program ma na celu pomoc w zarządzaniu stolarnią. Jednakże jest to miejsce w którym nie produkuje się mebli, a opakowania potrzebne później do transportu towarów (np. palety 120x80, skrzynki z płyty OSB). 

&emsp; Każdy produkt (np. skrzynka) składa się z (najczęściej) z kilku komponentów (gwoździe, deski, klocki, itp) oraz należy do pewnej kategorii produktów (paleta, skrzynka, stabilizator, itp). Każdy komponent jest z pewnego rodzaju materiału (deska 19mm, płyta OSB, itp). W naszej rzeczywistości istnieć będą również klienci. 

&emsp; Główną funkcjonalnością (oprócz dodawania nowych produktów i klientów do bazy) jest dodawanie zamówień do listy już obecnych. Zamówienie zawiera w sobie niezbędne dane klienta, oraz ilość konkretnych produktów które ma wykonać do określonej daty. 

&emsp; Administrator systemu (czyt. kierownik zakładu) jest jedyną osobą wymaganą do działania systemu (zakładamy że stolarnia jest niewielka, więc takie rozwiązanie w zupełności wystarczy). Oprócz tego można wyświetlać dane produktów.
</p>

___

## Diagram UML
<p align="center">
  <br><img src="Photos/uml.png">
</p>

___

## Uruchomienie aplikacji
&emsp; Aplikacja została napisana przy użyciu języka Python. Korzysta z biblioteki `http.server` do komunikacji z użytkownikiem oraz z biblioteki `sqlite3` do zarządzania bazą danych. Aplikacje należy włączyć z poziomu pliku `main.py` intefejs włączy się natomiast w przeglądarce pod adresem `127.0.0.1` (localhost) na porcie `8404`.

___