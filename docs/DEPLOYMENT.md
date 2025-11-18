# Guía de Despliegue - VoiceCRM

Esta guía explica cómo desplegar y ejecutar el sistema VoiceCRM completo.

---

## Prerequisitos

### Software necesario

- **Docker** y **Docker Compose** (recomendado para despliegue rápido)
- **Node.js 18+** y **npm** (para desarrollo frontend)
- **Python 3.11+** (para desarrollo backend)
- **PostgreSQL 15** (si no usas Docker)

### Credenciales requeridas

- **OpenAI API Key**: Necesaria para Whisper (speech-to-text) y GPT-4 (NLP)
 - Obtén tu clave en: https://platform.openai.com/api-keys
 - Costo aproximado: $0.006/minuto de audio + $0.002-0.01 por extracción NLP

---

## Opción 1: Despliegue con Docker (Recomendado)

### Paso 1: Clonar repositorio

```bash
git clone <repo-url>
cd aud_text
```

### Paso 2: Configurar variables de entorno

```bash
# Copiar ejemplo de .env
cp .env.example .env

# Editar .env y añadir tu OpenAI API Key
nano .env # o usar tu editor preferido
```

**Contenido de `.env`**:
```bash
OPENAI_API_KEY=sk-tu-api-key-aqui
```

### Paso 3: Levantar servicios

```bash
# Levantar base de datos y backend
docker-compose up -d

# Ver logs
docker-compose logs -f backend
```

### Paso 4: Verificar que está funcionando

```bash
# Backend API
curl http://localhost:8000/health
# Respuesta esperada: {"status":"healthy"}

# Documentación interactiva
open http://localhost:8000/docs
```

### Paso 5: Probar la API

#### Crear usuario
```bash
curl -X POST http://localhost:8000/api/auth/register \
 -H "Content-Type: application/json" \
 -d '{
 "email": "test@example.com",
 "name": "Usuario Test",
 "password": "password123"
 }'
```

#### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
 -H "Content-Type: application/json" \
 -d '{
 "email": "test@example.com",
 "password": "password123"
 }'
```

Guarda el `access_token` que recibes en la respuesta.

#### Listar contactos (usando token)
```bash
curl http://localhost:8000/api/contacts \
 -H "Authorization: Bearer TU_ACCESS_TOKEN_AQUI"
```

### Paso 6: Probar procesamiento de voz

#### Crear archivo de audio de prueba (Linux/Mac)

```bash
# Opción 1: Grabar tu voz (requiere sox)
rec -r 16000 -c 1 test_audio.wav
# Habla: "He quedado con Germán Palomares el próximo viernes"
# Ctrl+C para detener

# Opción 2: Usar text-to-speech (requiere espeak)
espeak -v es "He quedado con Germán Palomares el próximo viernes" -w test_audio.wav
```

#### Subir audio para procesamiento

```bash
curl -X POST http://localhost:8000/api/interactions/voice \
 -H "Authorization: Bearer TU_ACCESS_TOKEN_AQUI" \
 -F "audio=@test_audio.wav"
```

**Respuesta esperada**:
```json
{
 "interaction": {
 "id": 1,
 "contact": {
 "id": 1,
 "name": "Germán",
 "surname": "Palomares",
 "company": {
 "name": "Acme Corporation"
 }
 },
 "type": "meeting",
 "interaction_date": "2025-11-22T00:00:00",
 "notes": "..."
 },
 "transcript": "He quedado con Germán Palomares el próximo viernes",
 "extracted_entities": {
 "contact_name": "Germán Palomares",
 "action_type": "meeting",
 "date": "2025-11-22T00:00:00",
 "notes": "..."
 }
}
```

---

## Opción 2: Desarrollo local (Sin Docker)

### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos PostgreSQL
createdb voicecrm
psql voicecrm < ../database/init.sql
psql voicecrm < ../database/seed.sql

# Configurar variables de entorno
cp .env.example .env
nano .env # Añadir OPENAI_API_KEY y DATABASE_URL

# Ejecutar servidor
uvicorn app.main:app --reload
```

Ahora el backend estará en: http://localhost:8000

### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev
```

Ahora el frontend estará en: http://localhost:5173

---

## Desarrollo de la App Móvil (React Native)

La estructura base está creada en `/mobile`. Para desarrollarla:

```bash
cd mobile

# Instalar Expo CLI globalmente
npm install -g expo-cli

# Crear proyecto Expo
npx create-expo-app -t blank-typescript .

# Instalar dependencias adicionales
npm install expo-av axios @react-navigation/native

# Ejecutar
npm start
```

Luego escanea el QR con Expo Go en tu móvil.

---

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests (cuando estén implementados)

```bash
cd frontend
npm test
```

---

## Solución de problemas

### Error: "Database connection failed"

**Causa**: PostgreSQL no está corriendo o credenciales incorrectas

**Solución**:
```bash
# Verificar que PostgreSQL está corriendo
docker-compose ps

# Ver logs de la base de datos
docker-compose logs db

# Reiniciar servicios
docker-compose restart
```

### Error: "Invalid OpenAI API Key"

**Causa**: API Key no configurada o inválida

**Solución**:
1. Verifica que copiaste la clave correctamente en `.env`
2. Asegúrate de que la clave empieza con `sk-`
3. Verifica que tienes créditos en tu cuenta de OpenAI

### Error: "Contact not found"

**Causa**: El nombre mencionado en el audio no existe en la BD

**Solución**:
1. Verifica que el nombre está en la tabla `contacts`:
 ```bash
 docker-compose exec db psql -U voicecrm -d voicecrm -c "SELECT name, surname FROM contacts;"
 ```
2. Añade el contacto manualmente antes de procesar el audio
3. O modifica el código en `backend/app/api/interactions.py:46` para cambiar `auto_create=True`

### El audio no se transcribe correctamente

**Posibles causas**:
- Audio con mucho ruido de fondo
- Formato de audio incompatible
- Idioma incorrecto

**Soluciones**:
- Graba en ambiente silencioso
- Usa formatos: MP3, WAV, WEBM, OGG
- Verifica que el parámetro `language="es"` está configurado

---

## Acceso a la base de datos

### Vía Docker

```bash
# Conectar a PostgreSQL
docker-compose exec db psql -U voicecrm -d voicecrm

# Consultas útiles
SELECT * FROM users;
SELECT * FROM contacts;
SELECT * FROM interactions ORDER BY created_at DESC LIMIT 10;
```

### Vía cliente local

```bash
psql postgresql://voicecrm:voicecrm123@localhost:5432/voicecrm
```

---

## Despliegue en producción

### Recomendaciones

1. **Cambiar credenciales**:
 - `SECRET_KEY`: Generar clave aleatoria de 32+ caracteres
 - Contraseñas de base de datos
 - Desactivar `DEBUG=False`

2. **HTTPS**:
 - Usar reverse proxy (Nginx/Caddy)
 - Certificado SSL con Let's Encrypt

3. **Escalabilidad**:
 - Usar servicio de BD administrado (AWS RDS, GCP Cloud SQL)
 - Considerar CDN para frontend
 - Rate limiting en producción

4. **Monitoring**:
 - Logs centralizados (ELK Stack, CloudWatch)
 - Métricas (Prometheus + Grafana)
 - Alertas de errores (Sentry)

### Ejemplo con Docker en servidor

```bash
# En servidor (Ubuntu/Debian)
sudo apt update
sudo apt install docker.io docker-compose git

# Clonar repo
git clone <repo-url>
cd aud_text

# Configurar .env con credenciales de producción
nano .env

# Levantar en background
docker-compose up -d

# Configurar Nginx como reverse proxy
sudo nano /etc/nginx/sites-available/voicecrm
```

**Configuración Nginx**:
```nginx
server {
 listen 80;
 server_name voicecrm.tudominio.com;

 location / {
 proxy_pass http://localhost:8000;
 proxy_set_header Host $host;
 proxy_set_header X-Real-IP $remote_addr;
 }
}
```

```bash
# Activar sitio
sudo ln -s /etc/nginx/sites-available/voicecrm /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# SSL con Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d voicecrm.tudominio.com
```

---

## Recursos adicionales

- **Documentación API**: http://localhost:8000/docs (Swagger UI)
- **Arquitectura**: [docs/ARQUITECTURA.md](./ARQUITECTURA.md)
- **Memoria TFG**: [docs/TFG_MEMORIA.md](./TFG_MEMORIA.md)
- **OpenAI API Docs**: https://platform.openai.com/docs

---

## Soporte

Si encuentras problemas:

1. Revisa los logs: `docker-compose logs -f`
2. Verifica que todos los servicios están corriendo: `docker-compose ps`
3. Consulta la documentación técnica en `/docs`
4. Revisa issues en GitHub (si aplica)

---

## Checklist de despliegue

- [ ] Docker y Docker Compose instalados
- [ ] OpenAI API Key configurada en `.env`
- [ ] Servicios levantados: `docker-compose up -d`
- [ ] Backend respondiendo en http://localhost:8000/health
- [ ] Base de datos poblada con datos de ejemplo
- [ ] Usuario de prueba creado y login funcionando
- [ ] Audio de prueba procesado correctamente
- [ ] Frontend accesible (cuando esté implementado)

**¡Listo! Tu sistema VoiceCRM está funcionando.** 
