# API de Agendamento

API REST para agendamento de compromissos, construida com Django REST Framework. Valida automaticamente conflitos de horario.

## Funcionalidades

- Autenticacao via JWT
- Isolamento de dados por usuario
- Criacao, edicao, listagem e exclusao de agendamentos
- Validacao de horario (inicio deve ser antes do fim)
- Deteccao de conflito de horario: impede criar ou editar um agendamento que se sobreponha a outro ja existente do mesmo usuario

## Stack

- Python / Django
- Django REST Framework
- djangorestframework-simplejwt
- SQLite

## Endpoints

POST /api/token/ - obter access e refresh token
GET/POST /api/appointments/ - listar ou criar agendamentos
GET/PUT/PATCH/DELETE /api/appointments/{id}/ - detalhar, editar ou excluir um agendamento

## Como rodar localmente

python -m venv venv
venv\Scripts\activate
pip install django djangorestframework djangorestframework-simplejwt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

## Exemplo de criacao

POST /api/appointments/
Authorization: Bearer <access_token>

{
  "title": "Reuniao com cliente",
  "start_time": "2026-10-20T10:00:00Z",
  "end_time": "2026-10-20T11:00:00Z"
}

Se ja existir um agendamento do mesmo usuario que se sobreponha a esse horario, a API retorna erro 400 com a mensagem "Ja existe um agendamento nesse horario."

## Logica de deteccao de conflito

Dois intervalos de tempo se sobrepoem quando o inicio de um e antes do fim do outro, e o fim de um e depois do inicio do outro. Essa regra e aplicada diretamente na consulta ao banco de dados, filtrando agendamentos existentes do usuario antes de permitir a criacao de um novo.
