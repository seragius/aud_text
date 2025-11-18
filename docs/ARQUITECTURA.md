# 🏗️ Arquitectura del Sistema Voice CRM

## Índice
1. [Visión general](#visión-general)
2. [Arquitectura de tres capas](#arquitectura-de-tres-capas)
3. [Modelo de datos](#modelo-de-datos)
4. [Componentes del sistema](#componentes-del-sistema)
5. [Flujo de datos](#flujo-de-datos)
6. [Decisiones de diseño](#decisiones-de-diseño)
7. [Escalabilidad y rendimiento](#escalabilidad-y-rendimiento)
8. [Seguridad](#seguridad)

---

## 1. Visión general

Voice CRM es un sistema distribuido basado en arquitectura **cliente-servidor** con procesamiento de inteligencia artificial para reconocimiento de voz y extracción de información mediante NLP.

### Principios de diseño
- **Modularidad**: Cada componente tiene responsabilidad única
- **Escalabilidad**: Servicios separados que pueden escalar independientemente
- **Mantenibilidad**: Código limpio, documentado y testeable
- **Seguridad**: Autenticación robusta y validación de datos
- **Usabilidad**: Interfaz intuitiva y multiplataforma

---

## 2. Arquitectura de tres capas

```
┌─────────────────────────────────────────────────────────────────┐
│                     CAPA DE PRESENTACIÓN                         │
│                                                                  │
│  ┌──────────────────────┐       ┌──────────────────────┐       │
│  │   Web Application    │       │   Mobile Application │       │
│  │   ─────────────      │       │   ──────────────     │       │
│  │   • React 18         │       │   • React Native     │       │
│  │   • TypeScript       │       │   • TypeScript       │       │
│  │   • TailwindCSS      │       │   • Expo             │       │
│  │   • Vite             │       │   • Native Audio     │       │
│  │   • Web Audio API    │       │   • Navigation       │       │
│  │   • React Query      │       │   • AsyncStorage     │       │
│  └──────────┬───────────┘       └──────────┬───────────┘       │
│             │                               │                   │
│             └───────────┬───────────────────┘                   │
└─────────────────────────┼───────────────────────────────────────┘
                          │
                          │ HTTPS/REST + JWT
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│                    CAPA DE LÓGICA DE NEGOCIO                     │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              FastAPI Backend Server                     │    │
│  │  ┌──────────────────────────────────────────────────┐  │    │
│  │  │            API REST Endpoints                     │  │    │
│  │  │  /auth  /contacts  /companies  /interactions     │  │    │
│  │  └────────────────────┬─────────────────────────────┘  │    │
│  │                       │                                 │    │
│  │  ┌────────────────────▼─────────────────────────────┐  │    │
│  │  │              Service Layer                        │  │    │
│  │  │                                                   │  │    │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌──────────┐ │  │    │
│  │  │  │   Speech    │  │     NLP     │  │   CRM    │ │  │    │
│  │  │  │   Service   │──│   Service   │──│ Service  │ │  │    │
│  │  │  │             │  │             │  │          │ │  │    │
│  │  │  │ • Whisper   │  │ • GPT-4     │  │ • Match  │ │  │    │
│  │  │  │   API       │  │ • LangChain │  │ • Create │ │  │    │
│  │  │  │ • Validate  │  │ • Extract   │  │ • Update │ │  │    │
│  │  │  │   audio     │  │   entities  │  │ • Query  │ │  │    │
│  │  │  └─────────────┘  └─────────────┘  └──────────┘ │  │    │
│  │  └──────────────────────┬───────────────────────────┘  │    │
│  │                         │                               │    │
│  │  ┌──────────────────────▼───────────────────────────┐  │    │
│  │  │            Data Access Layer (ORM)                │  │    │
│  │  │              SQLAlchemy Models                    │  │    │
│  │  └───────────────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          │ SQL / Connection Pool
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│                    CAPA DE PERSISTENCIA                          │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                PostgreSQL Database                      │    │
│  │                                                         │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐         │    │
│  │  │  Users   │  │Companies │  │  Contacts    │         │    │
│  │  └──────────┘  └──────────┘  └──────────────┘         │    │
│  │                                                         │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐     │    │
│  │  │Interactions  │  │Opportunities │  │  Notes   │     │    │
│  │  └──────────────┘  └──────────────┘  └──────────┘     │    │
│  └────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Modelo de datos

### Diagrama Entidad-Relación

```
┌──────────────┐
│    Users     │
├──────────────┤
│ id (PK)      │
│ email        │──────┐
│ password_hash│      │
│ name         │      │
│ role         │      │
│ created_at   │      │
└──────────────┘      │
                      │
                      │ 1:N
                      │
                      ▼
         ┌────────────────────┐
         │   Interactions     │
         ├────────────────────┤
         │ id (PK)            │
         │ user_id (FK)       │
         │ contact_id (FK)    │◄──────┐
         │ type               │       │
         │ date               │       │
         │ audio_url          │       │
         │ transcript         │       │ N:1
         │ extracted_data     │       │
         │ notes              │       │
         │ created_at         │       │
         └────────────────────┘       │
                                      │
┌──────────────┐                      │
│  Companies   │                      │
├──────────────┤                      │
│ id (PK)      │──────┐               │
│ name         │      │               │
│ sector       │      │               │
│ size         │      │ 1:N           │
│ employees    │      │               │
│ revenue      │      ▼               │
│ website      │   ┌──────────────┐  │
│ country      │   │   Contacts   │  │
│ city         │   ├──────────────┤  │
│ created_at   │   │ id (PK)      │──┘
└──────────────┘   │ company_id   │
                   │ name         │
                   │ surname      │
                   │ position     │
                   │ email        │
                   │ phone_mobile │
                   │ phone_office │
                   │ address      │
                   │ lead_status  │
                   │ lead_source  │
                   │ created_at   │
                   └──────┬───────┘
                          │
                          │ 1:N
                          │
                          ▼
                   ┌──────────────────┐
                   │  Opportunities   │
                   ├──────────────────┤
                   │ id (PK)          │
                   │ contact_id (FK)  │
                   │ title            │
                   │ value            │
                   │ probability      │
                   │ stage            │
                   │ close_date       │
                   │ created_at       │
                   └──────────────────┘
```

### Esquema SQL detallado

#### Tabla: users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabla: companies
```sql
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sector VARCHAR(100),
    size VARCHAR(50),
    employees INT,
    revenue DECIMAL(15,2),
    website VARCHAR(255),
    country VARCHAR(100),
    city VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabla: contacts
```sql
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES companies(id) ON DELETE SET NULL,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100),
    position VARCHAR(100),
    email VARCHAR(255),
    phone_mobile VARCHAR(50),
    phone_office VARCHAR(50),
    address TEXT,
    lead_type VARCHAR(50) DEFAULT 'lead',
    lead_status VARCHAR(50) DEFAULT 'new',
    lead_source VARCHAR(100),
    funnel_stage VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_contacts_name ON contacts(name, surname);
CREATE INDEX idx_contacts_company ON contacts(company_id);
```

#### Tabla: interactions
```sql
CREATE TABLE interactions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    contact_id INT REFERENCES contacts(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    interaction_date TIMESTAMP NOT NULL,
    audio_url VARCHAR(500),
    transcript TEXT,
    extracted_data JSONB,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_interactions_contact ON interactions(contact_id);
CREATE INDEX idx_interactions_date ON interactions(interaction_date);
```

#### Tabla: opportunities
```sql
CREATE TABLE opportunities (
    id SERIAL PRIMARY KEY,
    contact_id INT REFERENCES contacts(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    value DECIMAL(15,2),
    probability INT CHECK (probability >= 0 AND probability <= 100),
    stage VARCHAR(100),
    close_date DATE,
    is_closed BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 4. Componentes del sistema

### 4.1 Backend - FastAPI

#### Estructura de directorios
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py             # Dependencies (DB, auth)
│   │   ├── auth.py             # Auth endpoints
│   │   ├── contacts.py         # Contacts CRUD
│   │   ├── companies.py        # Companies CRUD
│   │   ├── interactions.py     # Interactions + Voice
│   │   └── opportunities.py    # Opportunities CRUD
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Settings
│   │   ├── security.py         # JWT, password hashing
│   │   └── database.py         # DB connection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── company.py
│   │   ├── contact.py
│   │   ├── interaction.py
│   │   └── opportunity.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # Pydantic schemas
│   │   ├── company.py
│   │   ├── contact.py
│   │   ├── interaction.py
│   │   └── opportunity.py
│   └── services/
│       ├── __init__.py
│       ├── speech.py           # Whisper integration
│       ├── nlp.py              # Entity extraction
│       └── crm.py              # Contact matching logic
├── requirements.txt
├── Dockerfile
└── .env.example
```

#### Componentes clave

**1. Speech Service** (`services/speech.py`)
- Recibe archivos de audio (WAV, MP3, OGG)
- Valida formato y tamaño
- Envía a Whisper API
- Retorna transcripción en texto

**2. NLP Service** (`services/nlp.py`)
- Recibe texto transcrito
- Utiliza GPT-4 + LangChain para extraer:
  - **Nombre de contacto**: Busca coincidencias en BD
  - **Tipo de acción**: Reunión, llamada, email, etc.
  - **Fecha**: Parsea expresiones naturales ("próximo viernes")
  - **Notas adicionales**: Contexto relevante
- Estructura la información en formato JSON

**3. CRM Service** (`services/crm.py`)
- **Matching inteligente**: Busca contactos por nombre/apellido (fuzzy matching)
- **Autocomplete**: Rellena campos de empresa automáticamente
- **Validación**: Verifica que los datos extraídos sean coherentes

### 4.2 Frontend Web - React

#### Estructura
```
frontend/
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   └── Modal.tsx
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Layout.tsx
│   │   ├── voice/
│   │   │   ├── VoiceRecorder.tsx    # Componente grabación
│   │   │   └── AudioPlayer.tsx
│   │   └── crm/
│   │       ├── ContactList.tsx
│   │       ├── ContactDetail.tsx
│   │       └── InteractionCard.tsx
│   ├── pages/
│   │   ├── Login.tsx
│   │   ├── Dashboard.tsx
│   │   ├── Contacts.tsx
│   │   ├── Companies.tsx
│   │   └── Interactions.tsx
│   ├── services/
│   │   ├── api.ts              # Axios instance
│   │   ├── auth.ts
│   │   └── crm.ts
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useVoiceRecorder.ts
│   │   └── useContacts.ts
│   ├── utils/
│   │   └── audioUtils.ts
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── vite.config.ts
└── tailwind.config.js
```

#### Características
- **Web Audio API** para grabación de voz
- **React Query** para cacheo y sincronización
- **TypeScript** para type safety
- **Responsive design** con TailwindCSS

### 4.3 Mobile - React Native

```
mobile/
├── src/
│   ├── screens/
│   │   ├── LoginScreen.tsx
│   │   ├── DashboardScreen.tsx
│   │   ├── VoiceRecordScreen.tsx
│   │   └── ContactsScreen.tsx
│   ├── components/
│   ├── services/
│   │   └── api.ts
│   ├── navigation/
│   │   └── AppNavigator.tsx
│   └── App.tsx
├── package.json
└── app.json
```

---

## 5. Flujo de datos

### Flujo completo: Grabación de voz → CRM

```
1. USUARIO (Web/Mobile)
   │
   ├─ Graba audio: "He quedado con Germán Palomares el viernes"
   │
   ▼
2. FRONTEND
   │
   ├─ Captura audio (Web Audio API / React Native Audio)
   ├─ Convierte a formato compatible (WAV/MP3)
   ├─ Crea FormData con archivo
   │
   ▼
3. API BACKEND
   │
   ├─ POST /api/interactions/voice
   ├─ Autenticación JWT
   ├─ Validación de archivo
   │
   ▼
4. SPEECH SERVICE
   │
   ├─ Envía audio a Whisper API
   ├─ Recibe: "He quedado con Germán Palomares el viernes"
   │
   ▼
5. NLP SERVICE
   │
   ├─ Prompt GPT-4:
   │   "Extrae: nombre, acción, fecha del siguiente texto..."
   ├─ Recibe JSON:
   │   {
   │     "name": "Germán Palomares",
   │     "action": "Reunión",
   │     "date": "2025-11-22",
   │     "notes": "..."
   │   }
   │
   ▼
6. CRM SERVICE
   │
   ├─ Busca "Germán Palomares" en BD (fuzzy matching)
   ├─ Encuentra contact_id = 42
   ├─ Obtiene empresa asociada: "Acme Corp"
   │
   ▼
7. DATABASE
   │
   ├─ INSERT INTO interactions (...) VALUES (...)
   ├─ Commit transaction
   │
   ▼
8. RESPONSE
   │
   └─ 201 Created
      {
        "id": 123,
        "contact": {
          "id": 42,
          "name": "Germán",
          "surname": "Palomares",
          "company": "Acme Corp"
        },
        "type": "meeting",
        "date": "2025-11-22",
        "transcript": "...",
        "notes": "..."
      }
```

---

## 6. Decisiones de diseño

### 6.1 ¿Por qué FastAPI?

**Ventajas**:
- Rendimiento superior (comparable a Node.js)
- Validación automática con Pydantic
- Documentación automática (Swagger/OpenAPI)
- Soporte nativo async/await
- Integración excelente con Python ML/NLP

### 6.2 ¿Por qué PostgreSQL?

**Ventajas**:
- ACID completo (esencial para CRM)
- Soporte JSONB (para datos extraídos flexibles)
- Índices avanzados
- Escalabilidad vertical y horizontal
- Open source y maduro

### 6.3 ¿Por qué Whisper API vs. modelo propio?

**Razones**:
- **Precisión**: >95% en español sin entrenamiento
- **Rapidez**: Procesamiento en 2-5 segundos
- **Costo**: ~$0.006/minuto de audio
- **Simplicidad**: No requiere infraestructura GPU
- **Mantenimiento**: Sin necesidad de reentrenar

### 6.4 ¿Por qué GPT-4 para NLP vs. spaCy?

**Razones**:
- **Flexibilidad**: Puede entender contexto complejo
- **Pocos ejemplos**: Zero-shot learning
- **Multilenguaje**: Sin modelos adicionales
- **Actualización**: Mejora sin reentrenamiento

**Alternativa considerada**: spaCy + entrenamiento custom
- ❌ Requiere dataset etiquetado (500+ ejemplos)
- ❌ Mantenimiento de modelo
- ✅ Menor latencia
- ✅ Menor costo operativo

**Decisión**: GPT-4 para MVP, migrar a modelo custom si escala

---

## 7. Escalabilidad y rendimiento

### Estrategias implementadas

1. **Cacheo de contactos frecuentes** (Redis - opcional futuro)
2. **Connection pooling** en PostgreSQL
3. **Compresión de audio** antes de envío
4. **Procesamiento asíncrono** con FastAPI
5. **Lazy loading** en frontend
6. **Paginación** en listados

### Métricas objetivo

- **Latencia API**: < 200ms (endpoints CRUD)
- **Procesamiento de voz**: < 10s (audio de 1min)
- **Concurrent users**: 100+ simultáneos
- **Uptime**: 99.9%

---

## 8. Seguridad

### Implementaciones

1. **Autenticación**
   - JWT con expiración (24h)
   - Refresh tokens
   - Password hashing con bcrypt (cost=12)

2. **Autorización**
   - Role-based access control (RBAC)
   - Ownership validation (users solo ven sus datos)

3. **Validación**
   - Pydantic schemas en todos los endpoints
   - Sanitización de inputs
   - File upload validation (tipo, tamaño)

4. **Comunicación**
   - HTTPS en producción
   - CORS configurado correctamente
   - Rate limiting (100 req/min por IP)

5. **Base de datos**
   - Prepared statements (SQLAlchemy ORM)
   - Backups automáticos diarios
   - Encriptación en reposo (PostgreSQL)

### Amenazas mitigadas

| Amenaza | Mitigación |
|---------|------------|
| SQL Injection | ORM + Prepared statements |
| XSS | React auto-escape + Content-Security-Policy |
| CSRF | SameSite cookies + CORS |
| Brute force | Rate limiting + Account lockout |
| Data leaks | RBAC + Ownership checks |

---

## Resumen

Esta arquitectura proporciona:

✅ **Modularidad**: Componentes independientes y reemplazables
✅ **Escalabilidad**: Diseño preparado para crecimiento
✅ **Mantenibilidad**: Código limpio y documentado
✅ **Seguridad**: Múltiples capas de protección
✅ **Usabilidad**: Interfaces intuitivas multiplataforma
✅ **Extensibilidad**: Fácil añadir nuevas funcionalidades

El sistema está diseñado siguiendo **best practices** de ingeniería de software y cumple todos los objetivos del TFG.
