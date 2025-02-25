# Реорганизација на проектот

Овој проект ги користи MVC и N-tier архитектурите. Главниот проект работи на портата 8000, додека микросервисот за логин/регистрација е поставен на портата 8001. 

## Користење Docker

Проектот е контејнизиран со Docker. Главниот сервер (backend) работи на портата **8000**, а микросервисот за логин/регистрација работи на портата **8001**. Frontend-от работи на портата **3000**. PostgreSQL базата на податоци е хостирана на **Supabase** и работи на портата **6543**, така што не е потребна во Dockerfile-овите.

### Структура на проектот:

- **Backend**: Главниот сервер кој користи порта 8000.
- **Микросервис за логин/регистрација**: Сервис за логин/регистрација кој работи на портата 8001.
- **Frontend**: Платформа работи на порта 3000, која е прилагодена да го користи микросервисот на портата 8001 за логин и регистрација.