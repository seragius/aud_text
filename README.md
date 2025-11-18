# 🎙️ Voice CRM - Sistema de CRM con Reconocimiento de Voz y NLP

Sistema completo de gestión de relaciones con clientes (CRM) que permite registrar interacciones comerciales mediante voz, utilizando reconocimiento automático de voz (ASR) y procesamiento de lenguaje natural (NLP) para extraer información estructurada.

## 🎯 Características principales

- ✅ **Grabación de voz multiplataforma** (web y móvil)
- ✅ **Conversión automática de audio a texto** (Whisper API)
- ✅ **Extracción inteligente de entidades** mediante NLP (cliente, acción, fecha, notas)
- ✅ **Reconocimiento automático de contactos** desde base de datos pre-cargada
- ✅ **Gestión completa de CRM** (contactos, empresas, oportunidades, interacciones)
- ✅ **Interfaz web moderna** con React + TypeScript
- ✅ **App móvil nativa** con React Native
- ✅ **API REST segura** con autenticación JWT
- ✅ **Despliegue con Docker** Compose

## 🏗️ Arquitectura del sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENTE (Frontend)                        │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │   Web App        │         │   Mobile App     │         │
│  │   (React)        │         │ (React Native)   │         │
│  └────────┬─────────┘         └────────┬─────────┘         │
└───────────┼──────────────────────────────┼──────────────────┘
            │                              │
            │         HTTPS (JWT)          │
            └──────────────┬───────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                   BACKEND (FastAPI)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   API REST   │  │  Speech-to-  │  │  NLP Engine  │      │
│  │   Endpoints  │──│     Text     │──│  (Extracción)│      │
│  │              │  │   (Whisper)  │  │  Entidades   │      │
│  └──────┬───────┘  └──────────────┘  └──────────────┘      │
│         │                                                     │
│  ┌──────▼───────────────────────────────────────────┐       │
│  │         Lógica de Negocio & Servicios            │       │
│  │  • Autenticación  • CRM  • Matching de contactos │       │
│  └──────────────────────────┬───────────────────────┘       │
└─────────────────────────────┼───────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────┐
│                BASE DE DATOS (PostgreSQL)                    │
│  • Usuarios  • Contactos  • Empresas  • Interacciones       │
│  • Oportunidades  • Notas  • Historial                       │
└──────────────────────────────────────────────────────────────┘
```

## 📁 Estructura del proyecto

```
aud_text/
├── backend/                 # Backend FastAPI (Python)
│   ├── app/
│   │   ├── api/            # Endpoints REST
│   │   ├── core/           # Configuración y seguridad
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Lógica de negocio
│   │   │   ├── speech.py   # Speech-to-text
│   │   │   ├── nlp.py      # Extracción NLP
│   │   │   └── crm.py      # Lógica CRM
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/               # Frontend Web (React)
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── pages/          # Páginas
│   │   ├── services/       # Cliente API
│   │   ├── hooks/          # Hooks personalizados
│   │   └── App.tsx
│   ├── package.json
│   └── Dockerfile
│
├── mobile/                 # App Móvil (React Native)
│   ├── src/
│   │   ├── screens/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.tsx
│   └── package.json
│
├── database/
│   ├── init.sql            # Schema inicial
│   ├── seed.sql            # Datos de ejemplo
│   └── migrations/         # Migraciones
│
├── docs/                   # Documentación completa
│   ├── ARQUITECTURA.md     # Diseño técnico detallado
│   ├── API.md              # Documentación API REST
│   ├── TFG_MEMORIA.md      # Memoria del TFG
│   └── DEPLOYMENT.md       # Guía de despliegue
│
├── tests/                  # Tests funcionales
│   ├── backend/
│   └── frontend/
│
├── docker-compose.yml      # Orquestación completa
└── README.md
```

## 🚀 Stack tecnológico

### Backend
- **Python 3.11+** - Lenguaje principal
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para PostgreSQL
- **Pydantic** - Validación de datos
- **OpenAI Whisper API** - Speech-to-text
- **LangChain + GPT** - NLP y extracción de entidades
- **JWT** - Autenticación segura
- **Pytest** - Testing

### Frontend Web
- **React 18** - Framework UI
- **TypeScript** - Tipado estático
- **Vite** - Build tool rápido
- **TailwindCSS** - Estilos modernos
- **React Query** - Gestión de estado servidor
- **Axios** - Cliente HTTP

### Frontend Móvil
- **React Native** - Framework multiplataforma
- **TypeScript** - Tipado estático
- **React Navigation** - Navegación
- **Expo** - Tooling y desarrollo

### Base de datos
- **PostgreSQL 15** - Base de datos relacional

### DevOps
- **Docker** & **Docker Compose** - Contenedores
- **Git** - Control de versiones

## ⚙️ Instalación y despliegue

### Prerequisitos
- Docker y Docker Compose
- Node.js 18+ (para desarrollo frontend/mobile)
- Python 3.11+ (para desarrollo backend)

### Despliegue rápido con Docker

```bash
# Clonar repositorio
git clone <repo-url>
cd aud_text

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales (OpenAI API key, etc.)

# Levantar todos los servicios
docker-compose up -d

# Acceder a:
# - Web App: http://localhost:3000
# - API Backend: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### Desarrollo local

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend Web
```bash
cd frontend
npm install
npm run dev
```

#### Mobile
```bash
cd mobile
npm install
npm start
```

## 📊 Esquema de base de datos

```sql
-- Tablas principales del CRM
Users (id, email, password_hash, name, created_at)
Companies (id, name, sector, size, revenue, website)
Contacts (id, company_id, name, surname, position, email, phone, address)
Interactions (id, contact_id, user_id, type, date, audio_url, transcript, notes)
Opportunities (id, contact_id, value, close_date, probability, stage)
```

## 🎤 Flujo de uso

1. **Usuario graba nota de voz**: "He quedado con Germán Palomares el próximo viernes para revisar la propuesta"
2. **Sistema convierte audio a texto** (Whisper API)
3. **NLP extrae entidades**:
   - Cliente: "Germán Palomares" → Busca en BD → Encuentra contacto + empresa
   - Acción: "Reunión"
   - Fecha: "Próximo viernes" → Parsea a fecha concreta
   - Notas: "Revisar la propuesta"
4. **Sistema crea registro en CRM** con toda la información estructurada
5. **Usuario puede consultar, editar o eliminar** la interacción

## 🔐 Seguridad

- Autenticación mediante **JWT tokens**
- Contraseñas hasheadas con **bcrypt**
- Comunicación **HTTPS** en producción
- Validación de entrada con **Pydantic**
- CORS configurado correctamente
- Rate limiting en endpoints sensibles

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# Test de integración
docker-compose -f docker-compose.test.yml up
```

## 📚 Documentación adicional

- [Arquitectura detallada](docs/ARQUITECTURA.md)
- [Documentación API REST](docs/API.md)
- [Memoria del TFG](docs/TFG_MEMORIA.md)
- [Guía de despliegue](docs/DEPLOYMENT.md)

## 👨‍💻 Autor

Proyecto desarrollado como Trabajo Fin de Grado (TFG)

## 📄 Licencia

MIT License - Ver archivo LICENSE para más detalles

---

**Nota**: Este proyecto utiliza APIs de terceros (OpenAI Whisper) que requieren credenciales. Consulta la documentación de despliegue para configurarlas correctamente.
