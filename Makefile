.PHONY: help up down logs restart test clean install

help: ## Mostrar ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

up: ## Levantar todos los servicios
	docker-compose up -d
	@echo "✅ Servicios levantados"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

down: ## Detener todos los servicios
	docker-compose down
	@echo "✅ Servicios detenidos"

logs: ## Ver logs de todos los servicios
	docker-compose logs -f

restart: ## Reiniciar servicios
	docker-compose restart
	@echo "✅ Servicios reiniciados"

test-backend: ## Ejecutar tests del backend
	docker-compose exec backend pytest

clean: ## Limpiar contenedores, volúmenes e imágenes
	docker-compose down -v
	docker system prune -f
	@echo "✅ Limpieza completada"

install-frontend: ## Instalar dependencias del frontend
	cd frontend && npm install

dev-frontend: ## Ejecutar frontend en desarrollo
	cd frontend && npm run dev

install-backend: ## Instalar dependencias del backend (local)
	cd backend && pip install -r requirements.txt

dev-backend: ## Ejecutar backend en desarrollo (local)
	cd backend && uvicorn app.main:app --reload

db-shell: ## Conectar a la base de datos
	docker-compose exec db psql -U voicecrm -d voicecrm

seed: ## Re-poblar base de datos con datos de ejemplo
	docker-compose exec db psql -U voicecrm -d voicecrm -f /docker-entrypoint-initdb.d/02-seed.sql

status: ## Ver estado de los servicios
	docker-compose ps

token: ## Obtener token de demo user
	@curl -s -X POST http://localhost:8000/api/auth/login \
		-H "Content-Type: application/json" \
		-d '{"email":"demo@voicecrm.com","password":"demo1234"}' \
		| jq -r '.access_token'
