# ⚡ Quick Start - VoiceCRM

Guía rápida para tener el sistema funcionando en **5 minutos**.

---

## 🚀 Inicio Rápido con Docker

### 1. Prerequisitos

- Docker y Docker Compose instalados
- Clave de API de OpenAI

### 2. Configuración (2 minutos)

```bash
# 1. Clonar repositorio
git clone <repo-url>
cd aud_text

# 2. Configurar API Key de OpenAI
cp .env.example .env
echo "OPENAI_API_KEY=sk-tu-clave-aqui" >> .env

# 3. Levantar servicios
docker-compose up -d
```

### 3. Verificar (1 minuto)

```bash
# Esperar ~30 segundos a que levanten los servicios

# Verificar que backend está corriendo
curl http://localhost:8000/health
# Esperado: {"status":"healthy"}

# Abrir documentación interactiva
open http://localhost:8000/docs
```

---

## 🧪 Probar el sistema (2 minutos)

### Opción A: Usar datos de ejemplo pre-cargados

La base de datos ya incluye:
- 3 usuarios demo (password: `demo1234`)
- 10 empresas
- 20 contactos (¡incluyendo **Germán Palomares**!)
- Interacciones de ejemplo

#### Login con usuario demo

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@voicecrm.com","password":"demo1234"}' \
  | jq -r '.access_token' > token.txt

TOKEN=$(cat token.txt)
```

#### Ver contactos

```bash
curl http://localhost:8000/api/contacts \
  -H "Authorization: Bearer $TOKEN" | jq
```

### Opción B: Procesar audio (con tu OpenAI API Key)

```bash
# 1. Crear audio de prueba (texto a voz con espeak - Linux/Mac)
espeak -v es "He quedado con Germán Palomares mañana a las tres de la tarde para revisar la propuesta" -w test.wav

# 2. Subir y procesar
curl -X POST http://localhost:8000/api/interactions/voice \
  -H "Authorization: Bearer $TOKEN" \
  -F "audio=@test.wav" | jq
```

**Resultado esperado**:
```json
{
  "interaction": {
    "id": 8,
    "contact": {
      "name": "Germán",
      "surname": "Palomares",
      "company": {
        "name": "Acme Corporation"
      }
    },
    "type": "meeting",
    "interaction_date": "2025-11-19T15:00:00"
  },
  "transcript": "He quedado con Germán Palomares mañana...",
  "extracted_entities": {
    "contact_name": "Germán Palomares",
    "action_type": "meeting",
    "date": "2025-11-19T15:00:00",
    "notes": "Revisar la propuesta"
  }
}
```

---

## 🎯 Casos de uso comunes

### Crear nuevo usuario

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "miusuario@example.com",
    "name": "Mi Nombre",
    "password": "password123"
  }'
```

### Crear contacto manualmente

```bash
curl -X POST http://localhost:8000/api/contacts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Pedro",
    "surname": "García",
    "email": "pedro@example.com",
    "company_id": 1
  }'
```

### Ver interacciones de un contacto

```bash
# Ver todas las interacciones con Germán (contact_id=1)
curl http://localhost:8000/api/contacts/1/interactions \
  -H "Authorization: Bearer $TOKEN" | jq
```

---

## 📱 Frontend (Desarrollo)

```bash
cd frontend
npm install
npm run dev
```

Abre http://localhost:5173

---

## 🛑 Detener servicios

```bash
docker-compose down
```

---

## 📚 Siguiente paso

Ver documentación completa en:
- **Despliegue**: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- **Arquitectura**: [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md)
- **API Docs**: http://localhost:8000/docs

---

## ⚠️ Solución rápida de problemas

| Error | Solución |
|-------|----------|
| `Connection refused` | Espera 30-60s a que levanten los servicios |
| `Invalid token` | Vuelve a hacer login y guarda el nuevo token |
| `Contact not found` | El nombre debe existir en BD (ver `SELECT * FROM contacts`) |
| `OpenAI error` | Verifica tu API key en `.env` |

---

**¡Listo! Ya tienes VoiceCRM funcionando.** 🎉

Prueba diciendo nombres de los contactos pre-cargados:
- Germán Palomares
- María González
- Ana Fernández
- Laura Martínez

El sistema los detectará automáticamente y rellenará la empresa y cargo.
