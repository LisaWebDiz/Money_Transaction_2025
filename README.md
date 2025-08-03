# Money Transaction API Project 2025

## Описание
API для пополнения баланса пользователя и перевода денег другому пользователю.

## Быстрый запуск с docker
```
git clone https://github.com/yourusername/money_transaction_2025.git
cd money_transaction_2025
cp example.env .env
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## Документация
```
• Swagger: http://localhost:8000/swagger/
• Redoc: http://localhost:8000/redoc/
```

## Примеры использования
### 1. Регистрация нового пользователя с автоматическим получением токена и созданием нулевого баланса:

#### *SWAGGER*
http://localhost:8000/api/schema/swagger-ui/#/
![0](assets/img.png)
![1](assets/img_1.png)

#### *POSTMAN*
![15](assets/img_15.png)

### 2. Авторизация нового пользователя:
#### *SWAGGER*

![2](assets/img_2.png)

#### *POSTMAN*
![16](assets/img_16.png)

### 3. Проверка своего баланса (рубли):
#### *SWAGGER*
![3](assets/img_3.png)

#### *POSTMAN*
![17](assets/img_17.png)

### 4. Пополнение своего баланса (в копейках):
#### *SWAGGER*
![4](assets/img_4.png)

### 5. Результат пополнения (в рублях):
#### *SWAGGER*
![5](assets/img_5.png)

#### *POSTMAN*
![18](assets/img_18.png)

### 6. Регистрация и авторизация еще одного пользователя (по аналогии с 1 и 2). Пополнение баланса (в копейках):
#### *SWAGGER*
![6](assets/img_6.png)

### 7. Результат пополнения (в рублях):
#### *SWAGGER*
![7](assets/img_7.png)

### 8. Перевод другому пользователю (в рублях с копейками):
#### *SWAGGER*
![8](assets/img_8.png)

### 9. Результат перевода (в рублях):
#### *SWAGGER*
![9](assets/img_9.png)

#### *POSTMAN*
![19](assets/img_19.png)

### 10. Просмотр текущего баланса (в рублях):
#### *SWAGGER*
![10](assets/img_10.png)

#### *POSTMAN*
![20](assets/img_20.png)


### 11. Просмотр всех операций текущего пользователя:
#### *SWAGGER*
![11](assets/img_11.png)
![12](assets/img_12.png)

#### *POSTMAN*
![21](assets/img_21.png)

### 12. Перевод другому пользователю при недостаточности средств (пример обработки ошибки):
#### *SWAGGER*
![13](assets/img_13.png)
![14](assets/img_14.png)
