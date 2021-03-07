# foodgram-project
foodgram-project

Web-site for sharing recipes, with the capabilites of creating subscriptions to other users, selecting favorite recipes, creating list of purchases for selected recipes, as well as downloading such a list.


## Getting Started

1. Copy the repository

### Prerequisites

Docker and docker-compose.

### Installing

1. Open the terminal and run "docker-compose up" from the project directory

2. Open another terminal, run "docker-compose exec web /bin/bash" and then run "python manage.py migrate" to establish the DB. 

3. In order to create the superuser, open another terminal and run "docker-compose exec web /bin/bash" (skip if such a terminal already is opened), then run "python manage.py createsuperuser" and follow the instructions. The administrator page is accessible at http://127.0.0.1:8080/admin/.

4. In order to fill out the database with initial tag data, open another terminal and run "docker-compose exec web /bin/bash" (skip if such a terminal already is opened), then run "python manage.py loaddata recipes/fixtures.json"

## Running the tests

None

### Break down into end to end tests

None

### And coding style tests

Included into the Git Actions process.

## Deployment

None

## Built With

Django, Postgresql, Docker, Js, CSS

## Contributing

None

## Versioning

None

## Authors

* **Andrei Storchak** - *Initial work* - [AVStorchak](https://github.com/AVStorchak/)

## License

None

## Acknowledgments

* Yandex.Praktikum
