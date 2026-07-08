# culinary-hub-back

Small FastAPI backend for recipe data stored in MongoDB.

## Requirements

- Python 3.14+
- uv
- MongoDB

## Endpoints

- `GET /` health check
- `GET /recipes/?limit=8&skip=0`
- `GET /recipes/search?q=pasta&limit=8&skip=0`
- `GET /recipes/{id}`
- `POST /recipes/`
- `PUT /recipes/{id}`
- `DELETE /recipes/{id}`
