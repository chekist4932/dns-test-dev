# Задание №1
## Создать API для управления продажами в сети магазинов бытовой техники
### Используемый стэк
- Фреймворк для разработки -  FastAPI
- База данных - Postgres

### Сущности системы
- Товар
- Магазин
- Город (в одном городе может быть несколько магазинов)
- Продажи (одна продажа может содержать несколько товаров)

### Функциональность
- CRUD-операции на сущности Товар, Магазин, Город, Продажи
- Методы api для:
	- Получения продаж в разрезе:
		- Каждого города
		- Каждого магазина
		- Каждого товара
	- Получения продаж за последние **N** суток
	- Получения продаж с суммой более (или менее) **N**  денежных единиц
	- Получения продаж с количеством товаров более (или менее) **N** штук
	- Получения конкретных продаж (по идентификатору)
	- Все перечисленные выше пункты (в контексте продаж) должны быть комбинируемы (например, иметь возможность одновременно выбирать продажи с суммой более 5000 руб. и из города Владивостока) (* задача со звездочкой - считать как доп. балл)


### Дополнительные требования, Будет плюсом но не обязательно.
- Обеспечить миграции БД
- Обернуть в docker-контейнер
- Составить docker-compose
