# graphql
Тестовый проект с использованием Graphql

Суть проекта: агрегатор вакансий для рекрутеров. 
Работодатель выставляет вакансию с описанием работы, условиями работы, требованиями к работнику, условиями оплаты работы, вознаграждение рекрутеру за нахождение подходящего кандидата.
Рекрутер просматривает вакансии, отправляет в ответ на вакансию анкету подходящего кандидата, с именем кандидата, итогами интервью. 
Работодатель просматривает поступившие анкеты кандидатов, подтверждает подходящего, вакансия закрывается. 

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
    "createUser": {
      "user": {
        "username": "stepchik",
        "password": "udubat96"
      }
    }
  }
}
```
Верификация токена: 
```
mutation VerifyToken{
  verifyToken(token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InN0YXBhbmNoaWtyZWNydXQiLCJleHAiOjE2MzE3MjY1NTAsIm9yaWdJYXQiOjE2MzE3MjYyNTB9.Lnh3or2bKvmieQ2j0lvPjfVc4otYr0SdkXVTzHuTafA"
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
  }
}
```
Ответ: 
```
{
  "data": {
    "createEmployer": {
      "ok": false
    }
  }
}
```
Пользователь может добавить вакансию для рекрутеров, указав название вакансии , требования к работнику, условия труда, обязанности, уровень оплаты рекрутера (один из 4), размер оплаты рекрутера:
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
  }
}
```
Ответ:
```
{
  "data": {
    "createVacancy": {
      "ok": true
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
  }
}
```
Ответ: 
```
{
  "data": {
    "createEmployer": {
      "ok": true
    }
  }
}
```
Пользователь может просмотреть список активных вакансий (по дефолту, если у пользователя есть профиль рекрутера, показываются заявки его уровня, если указан определенный уровень рекрутера, фильтруется по нему, если ничего не указано и у пользователя нет профиля рекрутера, отображаются все заявки)
```
query Vacancies{
  vacancies(payLevel: "LG"){
    id
    vacancyName
    duties
    requirements
    conditions
    creationDate
    recruiterReward
    creator{
      user{
        firstName
        lastName
      }
      payedVacancies
    }
    active
    payLevel
  }
}
```
Ответ:
```
{
  "data": {
    "vacancies": [
      {
        "id": "2",
        "vacancyName": "вакансия фильтр",
        "duties": "обязанности",
        "requirements": "требования",
        "conditions": "зп",
        "creationDate": "2021-09-15T12:11:55.641805+00:00",
        "recruiterReward": 36,
        "creator": {
          "user": {
            "firstName": "",
            "lastName": ""
          },
          "payedVacancies": 0
        },
        "active": true,
        "payLevel": "LG"
      },
      {
        "id": "3",
        "vacancyName": "Грузчик",
        "duties": "какие-то",
        "requirements": "какие-то",
        "conditions": "какие-то",
        "creationDate": "2021-09-15T16:19:50.473817+00:00",
        "recruiterReward": 1000,
        "creator": {
          "user": {
            "firstName": "Степан",
            "lastName": "Медведев"
          },
          "payedVacancies": 1
        },
        "active": true,
        "payLevel": "LG"
      },
      {
        "id": "5",
        "vacancyName": "Водитель тягача",
        "duties": "График 2/2",
        "requirements": "Категория Е",
        "conditions": "Зп от 60000",
        "creationDate": "2021-09-15T19:00:25.943104+00:00",
        "recruiterReward": 5000,
        "creator": {
          "user": {
            "firstName": "Степан",
            "lastName": "Медведев"
          },
          "payedVacancies": 0
        },
        "active": true,
        "payLevel": "LG"
      }
    ]
```
Пользователь может отправить предложенного кандидата на заявку:
 '''
 mutation CreateCandidate{
  createCandidate(
    contact: "@grakky телеграм", 
    interview: "Ответил на все вопросы", 
    name: "Осипом Максим", 
    vacancyId: 3)
  {
    ok
  }
}
```
Ответ:
```
{
  "data": {
    "createCandidate": {
      "ok": true
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
  }
}
Ответ: 
{
  "data": {
    "proofExit": {
      "ok": true
    }
  }
}
```
