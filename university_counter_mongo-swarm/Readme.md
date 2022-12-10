# Счетчик (Swarm) с репликацией по веб-сервису

## 1. Настройка репликации (docker-compose)

### 1.1 Настройка образов
Реплики будут собираться из одинаковых обрзов, которые должны где-то лежать.
В примере будет использован локальный реест, поэтому надо указать, что образ
будет браться именно из него, а не из глобального docker hub
```yaml
	image: 127.0.0.1:10000/test_swarm-app
```

### 1.2 Настройка количества реплик
Репликация настраивается 2 подпараметрами в параметре deploy:
1) mode - [global, replicated] - Если global это означает, что данный сервис будет запущен ровно в одном экземпляре на всех возможных нодах. А replicated означает, что n-ое кол-во контейнеров для данного сервиса будет запущено на всех возможных нодах.
2) replicas - n-ое кол-во контейнеров

Примеры Конфигураций:
1. Сервис будет запущен ровно в одном экземпляре на всех возможных нодах
```yaml
	deploy:
		mode: global
```
2. Четыре контейнера для данного сервиса будет запущено на всех возможных нодах
```yaml
	deploy:
		mode: replicated
		replicas: 4
```

## 2 Инициализация Swarm
2.1 Инициализация менеджера
```bash
	docker swarm init
```

Отключение менеджера (управляющего роем) 
```bash
	docker swarm leave --force
```

## 3 Реестр
3.1 Инициализируем локальный реестр в котором будут храниться образы
```bash
	docker service create --name test_swarm-registry --publish published=10000,target=5000 registry:2 
```

3.2 Отправляем приложение в реестр:
```bash
	docker-compose push
```
3.2 Если не получится:
```bash
	docker-compose build university-web-swarm
	docker-compose push university-web-swarm
```

Удаление реестра
```bash
	docker service rm test_swarm-registry
```

## 4 Управление кластером
Управлять приложением можно через команду (docker stack)

4.1 Создадим приложение (без переменных окружения)
(Будут созданы и запущены: сеть и сервисы, которые развернуты в контейнеру registry)
```bash
	docker stack deploy --compose-file docker-compose.yaml test_swarm-app
```

4.1 Создадим приложение (с переменными окружения) 
Переменные окружения теперь не считываются с файла и их нужно передавать вручную:
```bash
	env $(cat .env | xargs) docker stack deploy --compose-file docker-compose.yaml test_swarm-app
```

4.2 Посмотреть контейнеры приложения:
```bash
	docker stack services test_swarm-app
```

4.3 Проверка приложения:
```bash
	wget localhost:8000
```

Удаление приложения
```bash
	docker stack rm test_swarm-app
```

## 5 Удаление
Удаление приложения
```bash
	docker stack rm test_swarm-app
```

Удаление реестра
```bash
	docker service rm test_swarm-registry
```

Отключение менеджера (управляющего роем) 
```bash
	docker swarm leave --force
```