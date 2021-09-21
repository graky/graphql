# graphql
Тестовый проект с использованием Graphql

Суть проекта: агрегатор вакансий для рекрутеров. 
Работодатель выставляет вакансию с описанием работы, условиями работы, требованиями к работнику, условиями оплаты работы, вознаграждение рекрутеру за нахождение подходящего кандидата.
Рекрутер просматривает вакансии, отправляет в ответ на вакансию анкету подходящего кандидата, с именем кандидата, итогами интервью. 
Работодатель просматривает поступившие анкеты кандидатов, подтверждает подходящего, вакансия закрывается. 


## Разворачиваем проект локально
Проект использует python версии 3.9
 - Создаем виртуальное окружение
   ##### virtualenv --python=python3.9 venv
 - Устанавливаем необходимые для работы проекта библиотеки из файла зависимостей
   ##### pip install -r requirements.txt
 - Установить базу данных postgresql
 - В директории easywork создать файл .env 
 - Файл содержит данные необходимые для подключения к БД, имя БД, имя пользователя, пароль, хост, порт
   
```
DATABASE_NAME= db_name
DATABASE_USER= db_user
DATABASE_PASSWORD= db_password
DATABASE_HOST= localhost
DATABASE_PORT = 5432
```
 - Для создания структур в БД, необходимо запустить миграции с помощью команды
   ##### python manage.py migrate
 - Чтобы создать суперпользователя для использования админ панели выполняем команду:
   ##### python manage.py createsuperuser
 - Чтобы запустить проект не локальном сервере выполняем команду:
   ##### python manage.py runserver
 - По адресу http://127.0.0.1:8000/ находится интерактивный интерфейс запросов GraphiQL
 - По адресу http://127.0.0.1:8000/admin входим в админ панель



# Логика с запросами

Регистрация пользователя 
```
mutation CreateUser{
  createUser(
    firstName: "Степан", 
    lastName: "Медведев", 
    password: "udubat96", 
    username:"stapanchik"){
    user{
      username
      password
      }
  }
}
```
Ответ: 
```
{
  "data": {
    "createUser": {
      "user": {
        "username": "stepchik",
        "password": "password"
      }
    }
  }
}
```
Создание токена: 
```
mutation TokenAuth{
  tokenAuth(
    username: "stapanchikrecruteshe", 
    password:"password"
  )
  {
   token
  }
}
```
Ответ:
```
{
  "data": {
    "tokenAuth": {
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImVzZmEiLCJleHAiOjE2MzIxNDgyNzEsIm9yaWdJYXQiOjE2MzIxNDc5NzF9.tFf5Ig1sr1fovAv11yJZyPQg4pJM-WyVby-O6MfdnEc"
    }
  }
}
```
Верификация токена: 
```
mutation VerifyToken{
  verifyToken(token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImVzZmEiLCJleHAiOjE2MzIxNDgyNzEsIm9yaWdJYXQiOjE2MzIxNDc5NzF9.tFf5Ig1sr1fovAv11yJZyPQg4pJM-WyVby-O6MfdnEc"
  )
  {
   payload
  }
}
```
Ответ:
```
{
  "data": {
    "verifyToken": {
      "payload": {
        "username": "stepchik",
        "exp": 1631726550,
        "origIat": 1631726250
      }
    }
  }
}
```
Пользователь может создать себе профиль работодателя: 
```
mutation CreateEmployer{
  createEmployer
  {
   ok
   message
  }
}
```
Ответ: 
```
{
  "data": {
    "createEmployer": {
      "ok": true
      "message": null
    }
  }
}
```
Пользователь может добавить вакансию для рекрутеров, указав название вакансии, требования к работнику, условия труда, обязанности, уровень оплаты рекрутера (один из 4), размер оплаты рекрутера:
```
mutation CreateVacancy{
  createVacancy(
    vacancyName: "Водитель тягача",
    requirements: "Категория Е",
    conditions: "Зп от 60000",
    duties: "График 2/2",
    payLevel: "LG",
    recruiterReward: 5000
  )
  {
   ok
   message
  }
}
```
Ответ:
```
{
  "data": {
    "createVacancy": {
      "ok": true
      "message": null
    }
  }
}
```
Пользователь может создать профиль рекрутера:
```
mutation CreateRecruiter{
  createEmployer
  {
   ok
   message
  }
}
```
Ответ: 
```
{
  "data": {
    "createEmployer": {
      "ok": true
      "message": null
    }
  }
}
```
Пользователь может просмотреть список вакансий. Фильтруется по активно или нет, названию, требованиям, уровню оплаты. 
```
query {
  vacancies(payLevel: "HR", active: true) {
    edges {
      node {
        id
        vacancyName
        duties
        requirements
        conditions
        payLevel
        creationDate
        recruiterReward
        active
        creator {
          fullName
          id
          user {
            username
          }
        }
      }
    }
  }
}
```
Ответ:
```
{
  "data": {
    "vacancies": {
      "edges": [
        {
          "node": {
            "id": "VmFjYW5jeVR5cGU6MQ==",
            "vacancyName": "Водитель тягача",
            "duties": "График 2/2",
            "requirements": "Категория Е",
            "conditions": "ЗП от 60к в месяц",
            "payLevel": "HR",
            "creationDate": "2021-09-15T10:18:13.978916+00:00",
            "recruiterReward": 5000,
            "active": true,
            "creator": {
              "fullName": " ",
              "id": "1",
              "user": {
                "username": "employer_one"
              }
            }
          }
        },
        {
          "node": {
            "id": "VmFjYW5jeVR5cGU6Nw==",
            "vacancyName": "test vacancy",
            "duties": "test duties",
            "requirements": "test requirements",
            "conditions": "test conditions",
            "payLevel": "HR",
            "creationDate": "2021-09-20T07:39:55.475485+00:00",
            "recruiterReward": 5000,
            "active": true,
            "creator": {
              "fullName": "Surname Name",
              "id": "11",
              "user": {
                "username": "testestetstest"
              }
            }
          }
        }
      ]
    }
```

Пользователь по id ноды может запросить вакансию
```
query Vacancy {
  vacancy(id: "VmFjYW5jeVR5cGU6Mw==") {
    id
    vacancyName
    duties
    requirements
    conditions
    payLevel
    creationDate
    recruiterReward
    active
    creator {
      fullName
    }
  }
}
```
Ответ:
```
{
  "data": {
    "vacancy": {
      "id": "VmFjYW5jeVR5cGU6Mw==",
      "vacancyName": "Водитель грузовика",
      "duties": "обязанности определенные",
      "requirements": "test requirements",
      "conditions": "условия особые",
      "payLevel": "LG",
      "creationDate": "2021-09-21T18:25:57.378681+00:00",
      "recruiterReward": 500,
      "active": true,
      "creator": {
        "fullName": "Роман Кириленко"
      }
    }
  }
}
```

Пользователь может отправить предложенного кандидата на заявку:
```
 mutation CreateCandidate{
  createCandidate(
    contact: "@grakky телеграм", 
    interview: "Ответил на все вопросы", 
    name: "Осипом Максим", 
    vacancyId: 3)
  {
    ok
    message
  }
}
```
Ответ:
```
{
  "data": {
    "createCandidate": {
      "ok": true
      "message": null
    }
  }
}
```
Пользователь с профилем работодателя может запросить список кандидатов, предложенных рекрутерами по его заявкам:
```
query Candidates{
  candidates{
    id
    vacancy{
      vacancyName
    }
    recruiter{
      user{
        firstName
        lastName
      }
      closedVacancies
    }
    name
    interview
    contact
  }
}
```
Ответ:
```
{
  "data": {
    "candidates": [
      {
        "id": "3",
        "vacancy": {
          "vacancyName": "Грузчик"
        },
        "recruiter": {
          "user": {
            "firstName": "Степан",
            "lastName": "Медведев"
          },
          "closedVacancies": 1
        },
        "name": "Осипом Максим",
        "interview": "Ответил на все вопросы",
        "contact": "@grakky телеграм"
      },
      {
        "id": "5",
        "vacancy": {
          "vacancyName": "Грузчик"
        },
        "recruiter": {
          "user": {
            "firstName": "Кирилл",
            "lastName": "Медведев"
          },
          "closedVacancies": 0
        },
        "name": "Тихонович Александр",
        "interview": "Не всё знает, но готов работать",
        "contact": "89892468931"
      }
    ]
  }
}
```
Пользователь может одобрить заявку кандидата на предложенную им вакансию, тогда вакансия становится не активна, количество оплаченных работодателем вакансий увеличивает на 1, количество закрытых вакансий рекрутером увеличивается на 1. 
```
mutation ProofExit{
  proofExit(candidateId: 3){
    ok
    message
  }
}
```
Ответ:
```
{
  "data": {
    "proofExit": {
      "ok": true
      "message": null
    }
  }
}
```

Доступен запрос для поиска по работодателям и рекрутерам, ищет пользователей с входящими данными в фамилии или имени 
```
query {
  search(searchText: "Кирил") {
    ... on EmployerType {
      id
      fullName
      user{
        id
      }
    }
    ... on RecruiterType {
      id
      fullName
      user{
        id
      }
    }
  }
}

```
Ответ: 
```
{
  "data": {
    "search": [
      {
        "id": "1",
        "fullName": "Роман Кириленко",
        "user": {
          "id": "1"
        }
      },
      {
        "id": "1",
        "fullName": "Кирилл Медведев",
        "user": {
          "id": "2"
        }
      }
    ]
  }
}
```
