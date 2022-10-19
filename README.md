# Django template

## Technologies

- [X] Python
- [X] Django
- [X] Django Rest Framework
- [X] Docker
- [X] Postgresql

## Environments

This template is thinked and designed for the docker environment. It is not recommended to use it without docker.


### How to use Docker dev

1. create a file named `.env` containing the required environment variables (read the next section)
2. run `docker-compose up --build`
3. work with your local files
4. execute commands inside the container. ex `docker exec -it django_template-app_1 python manage.py makemigrations`

### Features

|                                    | Docker Dev |
|------------------------------------|:----------:|
| Auto-reload                        |     ✅      |
| Auto migrate at start              |     ✅      |
| Auto requirements install at start |     ✅      |
| Database                           |  MariaDB   |
| Database port publicly exposed     |     ✅      |
| Reverse proxy (Nginx)              |     ❌      |
| Debug                              |     ✅      |
| Admin page                         |     ✅      |
| Serving media automatically        |
| CORS allow all                     |     ✅      |
| Allow all hosts                    |     ✅      |

### Required environment variables

- ✅ Required
- ❌ Not required
- ⚠️ Optional

|                                     |   Docker Dev   |
|-------------------------------------|:--------------:|
| POSTGRES_PASSWORD                   |       ✅        |
| SECRET_KEY (default string for dev) |       ⚠️       |
| ALLOWED_HOSTS (all for dev)         |       ❌        |
| CORS_ALLOWED_ORIGINS (all for dev)  |       ❌        |
| EMAIL_HOST                          |       ⚠️       |
| EMAIL_HOST_PASSWORD                 |       ⚠️       |
| EMAIL_HOST_USER                     |       ⚠️       |
| EMAIL_PORT (default EMAIL_PORT)     |       ⚠️       |

### Example .env

```
POSTGRES_PASSWORD=somerandomstring
SECRET_KEY=anotherrandomstring
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_PASSWORD=gmailpassword
EMAIL_HOST_USER=yourmail@gmail.com
EMAIL_PORT=587
ALLOWED_HOSTS=localhost,127.0.0.1,api.something.it
CORS_ALLOWED_ORIGINS=https://frontend.com,https://sub.frontend.com
```
