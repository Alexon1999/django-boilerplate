# Project Local Setup

- [Setting Up the Project Locally](#🧱-setting-up-the-project-locally)
- [Setting up Precommit](#💡-setting-up-precommit)
- [Start project locally with Docker](#📦-start-project-locally-with-docker)
- [Additional Information](#additional-information)


<br>

## 🧱  Setting Up the Project Locally
  ##### create virtual environment

  ```bash
  $ python -m venv venv
  ```

  ##### environment activation
  - windows
  ```bash
  $ .\venv\Scripts\activate
  ```

  - Linux, Unix, MacOS 
  ```bash
  $ source venv/bin/activate
  ```

  ##### dependency installation 

  ```bash
  $ pip install -r .\requirements.txt
  ```

  ##### overload settings with environment variables (launch before run server)
  loads environment variables from an env file into the current shell session
  - Linux, Unix, MacOS 
  ```bash
  $ set -a; source .env.local; set +a;

  # or with the script
  $ source ./scripts/loadenv.sh .env.local
  ```
  - windows
  ```bash
  # powershell
  $  .\scripts\loadenv.ps1 .env.local

  # cmd
  $ .\scripts\loadenv.bat .env.local
  ```

  ##### makemigratoins
  ```
  $ python manage.py makemigrations authentication
  $ python manage.py makemigrations api
  ```

  ##### migrate
  ```
  $ python manage.py migrate
  ```

  ##### launch the backend server
  ```
  $ python manage.py runserver
  ```

  ##### If you need to create a user (admin)
  ```
  $ python manage.py createsuperuser
  ```

<br>

## 💡 Setting up Precommit
It's important to enforce code styling and formatting. we use **[pre-commit](consistent_codebase.md)**. before each commit we do linting and formatting.

**In you IDE, Install following extensions :**
- **Flake8** : linter
- **Black** : formatter

<br>


## 📦 Start project locally with Docker
  ##### docker-compose (recommended)
  ```bash
    $ docker-compose up -d --build
    $ docker-compose exec api python manage.py migrate
    $ docker-compose exec api python manage.py createsuperuser
  ```

  ##### build and run image
  ```bash
    $ docker build -t boilerplate_back .
    $ docker run -it -d --name boilerplate_back -v "./:/home/app" -p 8000:8000 boilerplate_back python manage.py runserver 0.0.0.0:8000
    $ docker exec -it boilerplate_back bash
    $ python manage.py migrate
    $ python manage.py createsuperuser
  ```

<br>


## Additional Information

- 🚢 [How we use Docker Compose to deploy in various environment (development,testing,staging,production)](./docker_compose_configuration.md)