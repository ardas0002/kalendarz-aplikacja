# Kalendarz Wydarzeń

Aplikacja kalendarza wydarzeń oparta na frameworku Flask (backend) oraz statycznym froncie w Nginx, uruchamiana przy pomocy Docker Compose.

## Wymagania wstępne

Aby uruchomić aplikację na Ubuntu, upewnij się, że masz zainstalowane Docker oraz Docker Compose. Zaktualizuj listę pakietów za pomocą `sudo apt update`, zainstaluj potrzebne zależności, uruchamiając `sudo apt install apt-transport-https ca-certificates curl git software-properties-common`, a następnie dodaj klucz GPG Dockera: `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg`. Dodaj repozytorium Dockera: `echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`, zaktualizuj listę pakietów `sudo apt update`, a następnie zainstaluj Dockera za pomocą `sudo apt install docker-ce docker-ce-cli containerd.io`. Aby sprawdzić, czy Docker działa, użyj polecenia `sudo systemctl status docker`. Jeśli chcesz, aby bieżący użytkownik mógł korzystać z Dockera bez użycia `sudo`, dodaj go do grupy `docker` poleceniem `sudo usermod -aG docker ${USER}` i zaloguj się ponownie. Aby zainstalować Docker Compose, użyj polecenia `sudo curl -L "https://github.com/docker/compose/releases/download/v2.5.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`, ustaw uprawnienia do pliku `sudo chmod +x /usr/local/bin/docker-compose`, a następnie sprawdź wersję Docker Compose: `docker-compose --version`.

## Uruchamianie aplikacji

Pobierz repozytorium z kodem aplikacji za pomocą `git clone <URL_do_repozytorium>`, przejdź do katalogu projektu `cd <nazwa_katalogu_projektu>`, a następnie uruchom aplikację za pomocą Docker Compose `docker-compose up --build`. Aplikacja frontendowa powinna być dostępna pod adresem `http://localhost`, a backend pod `http://localhost:5000`. Aby uruchomić aplikację w tle, użyj polecenia `docker-compose up -d --build`. Aby zatrzymać aplikację, użyj `docker-compose down`.

## Problemy i rozwiązania

Brak dostępu do aplikacji z zewnątrz może wynikać z zamkniętych portów w firewallu. Otwórz porty za pomocą `sudo ufw allow 80/tcp` oraz `sudo ufw allow 5000/tcp`. W przypadku problemów możesz sprawdzić logi za pomocą `docker-compose logs` lub logi konkretnego serwisu `docker-compose logs backend`. Test połączenia do API możesz wykonać używając `curl http://localhost:5000/api/events`.

## Aktualizacje i rozwój

Po każdej zmianie w kodzie zbuduj na nowo kontenery za pomocą `docker-compose up --build` lub ponownie uruchom aplikację `docker-compose restart`.

## Uwaga dotycząca zdalnego testowania

Jeśli planujesz testować aplikację na zdalnym serwerze (nie lokalnie), konieczne jest zastąpienie lokalnego endpointu API w pliku script.js. W liniach, gdzie odwołujesz się do API za pomocą fetch, np.:
fetch('http://localhost:5000/api/events?month=${currentMonth}&year=${currentYear}')
zastąp localhost DNS-em lub adresem IP serwera, na którym jest uruchomione docker-compose. Na przykład, jeśli Twój serwer ma adres http://example.com, linia powinna wyglądać tak:
fetch('http://example.com:5000/api/events?month=10&year=2024')
Ta zmiana pozwoli na poprawne połączenie z API podczas zdalnego uruchamiania aplikacji.

