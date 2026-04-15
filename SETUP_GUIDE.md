# iAgri + AgroSense — Guía de Setup Completo
## Supabase · Twilio WhatsApp · Hostinger Subdominios

---

## PASO 1 — Supabase iAgri

### 1.1 Crear proyecto iAgri
1. Ir a https://supabase.com/dashboard → **New Project**
2. Nombre: `iagri-production`
3. Contraseña de BD: (guarda esta contraseña)
4. Región: `us-east-1` (o la más cercana a El Salvador)
5. Guardar:
   - `SUPABASE_URL` = https://xxxxx.supabase.co
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY` ← guardar muy seguro

### 1.2 Ejecutar migraciones iAgri (en orden)
En el **SQL Editor** de Supabase, ejecutar en este orden:

```
001_core_multitenant.sql
002_agro_production.sql  
003_kpis_alerts_agents.sql
004_whatsapp_twilio.sql
099_seed_project_one_sv.sql
```

**NOTA**: Si no tienes TimescaleDB en tu plan, omite las líneas
`SELECT create_hypertable(...)` y las políticas de retención en 003.
En planes gratuitos usar tablas normales con índice en `recorded_at`.

---

## PASO 2 — Supabase AgroSense

### 2.1 Crear proyecto AgroSense (separado)
1. Nuevo proyecto: `agrosense-production`
2. Guardar URL y keys por separado

### 2.2 Ejecutar migraciones AgroSense
```
agrosense/001_iot_sensors.sql
```

### 2.3 Vincular con iAgri
En la tabla `as_organizations`, insertar:
```sql
INSERT INTO as_organizations (slug, name, iagri_org_id) 
VALUES ('project-one-sv', 'Project One SV', 'a1b2c3d4-0000-0000-0000-000000000001');
```

---

## PASO 3 — Twilio WhatsApp

### 3.1 Registrarte en Twilio
1. https://www.twilio.com/try-twilio
2. Verificar tu número de teléfono real
3. En el dashboard, ir a **Messaging → Try it out → Send a WhatsApp message**

### 3.2 Sandbox de WhatsApp (para pruebas inmediatas)
1. Twilio Console → **Messaging → Try WhatsApp**
2. Tu número de sandbox será algo como: `+1 415 523 8886`
3. Para activar el sandbox: envía desde tu WhatsApp el código que aparece
   Ej: `join <palabra-clave>` al número de sandbox

### 3.3 Actualizar la tabla whatsapp_accounts
```sql
UPDATE whatsapp_accounts 
SET 
  account_sid = 'TU_ACCOUNT_SID',
  auth_token_enc = 'TU_AUTH_TOKEN',  -- en producción cifrar
  phone_number = '+14155238886',     -- tu número Twilio
  whatsapp_number = 'whatsapp:+14155238886'
WHERE organization_id = 'a1b2c3d4-0000-0000-0000-000000000001';
```

### 3.4 Deploy de la Edge Function WhatsApp
```bash
# Instalar Supabase CLI
npm install -g supabase

# Login
supabase login

# Vincular proyecto
supabase link --project-ref TU_PROJECT_REF

# Configurar secrets
supabase secrets set ANTHROPIC_API_KEY=sk-ant-xxxxx
supabase secrets set TWILIO_ACCOUNT_SID=ACxxxxx
supabase secrets set TWILIO_AUTH_TOKEN=xxxxx

# Deploy
supabase functions deploy whatsapp-webhook --no-verify-jwt
```

### 3.5 Configurar Webhook en Twilio
1. Twilio Console → **Messaging → Settings → WhatsApp Sandbox Settings**
2. En **"When a message comes in"**:
   ```
   https://TU_PROJECT.supabase.co/functions/v1/whatsapp-webhook
   ```
3. Método: **HTTP POST**

### 3.6 Probar
Desde tu WhatsApp personal (después de activar sandbox):
```
¡Hola! ¿Cómo están las zonas de cultivo hoy?
```
El agente responderá con el nombre del usuario y el estado del sistema.

---

## PASO 4 — Subdominios en Hostinger

### 4.1 Acceder al Panel de Control
1. Hostinger → **My Websites** → tu dominio `iagri.com`
2. Ir a **Domains → Manage** → **DNS / Nameservers**
3. O directo: **Hosting → Manage → DNS Zone**

### 4.2 Crear los subdominios (CNAME records)
Para cada subdominio, agrega un registro **CNAME**:

| Subdominio        | CNAME Target              | Descripción          |
|-------------------|---------------------------|----------------------|
| `app`             | `cname.vercel-dns.com`    | App principal        |
| `cultivos`        | `cname.vercel-dns.com`    | Módulo cultivos      |
| `comercial`       | `cname.vercel-dns.com`    | Módulo comercial     |
| `logistica`       | `cname.vercel-dns.com`    | Módulo logística     |
| `analytics`       | `cname.vercel-dns.com`    | KPIs y dashboards    |
| `sensores`        | `cname.vercel-dns.com`    | AgroSense IoT        |
| `finanzas`        | `cname.vercel-dns.com`    | Módulo financiero    |
| `fiaaa`           | `cname.vercel-dns.com`    | FIAAA inversores     |
| `api`             | Apunta a tu backend       | API Gateway          |
| `webhook`         | `TU_PROJECT.supabase.co`  | Webhooks Twilio/Meta |

### 4.3 Si usas Vercel para el frontend
```bash
# En cada proyecto Next.js, agregar dominio:
vercel domains add cultivos.iagri.com
vercel domains add comercial.iagri.com
# ... etc
```

### 4.4 SSL automático
Hostinger y Vercel generan SSL automáticamente para subdominios.
Para verificar: `https://cultivos.iagri.com` debe cargar con candado verde.

---

## PASO 5 — Variables de entorno por módulo

Crea un archivo `.env.local` en cada módulo Next.js:

```env
# Común a todos los módulos
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyxxxxxx
SUPABASE_SERVICE_ROLE_KEY=eyxxxxxx

# AgroSense (solo módulo sensores)
NEXT_PUBLIC_AGROSENSE_URL=https://yyyyy.supabase.co
NEXT_PUBLIC_AGROSENSE_ANON_KEY=eyxxxxxx

# Anthropic (solo en backend/edge functions)
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Twilio (solo en webhook)
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886

# ElevenLabs (para voz del agente)
ELEVENLABS_API_KEY=xxxxx
```

---

## PASO 6 — Registro del primer usuario

Después de registrarte en la app, ejecutar en Supabase SQL Editor:

```sql
-- Asignar organización y rol CEO al primer usuario
UPDATE profiles 
SET organization_id = 'a1b2c3d4-0000-0000-0000-000000000001'
WHERE id = 'TU_USER_ID_DE_AUTH';

-- Darle rol CEO
INSERT INTO user_roles (user_id, organization_id, role, is_primary)
VALUES ('TU_USER_ID', 'a1b2c3d4-0000-0000-0000-000000000001', 'ceo', TRUE);

-- Agregar número de WhatsApp
UPDATE profiles 
SET whatsapp_id = '+50312345678',  -- tu número real con código de país
    phone = '+50312345678'
WHERE id = 'TU_USER_ID';
```

---

## RESUMEN DE URLS FINALES

| URL                                    | Función                         |
|----------------------------------------|---------------------------------|
| `https://app.iagri.com`                | App principal / Login           |
| `https://cultivos.iagri.com`           | Gestión cultivos y zonas        |
| `https://sensores.iagri.com`           | Dashboard IoT AgroSense         |
| `https://comercial.iagri.com`          | CRM + Contratos B2I             |
| `https://analytics.iagri.com`          | KPIs y agentes gerenciales      |
| `https://finanzas.iagri.com`           | ERP Financiero (Dola)           |
| `https://fiaaa.iagri.com`              | Portal inversores FIAAA         |
| `https://PROJECT.supabase.co/functions/v1/whatsapp-webhook` | Webhook Twilio |

---

## PREGUNTAS FRECUENTES

**¿Puedo agregar nuevas organizaciones sin tocar el código?**
Sí. Solo INSERT en `organizations`, `org_modules`, y `user_roles`. 
Toda la RLS es automática por `organization_id`.

**¿Cómo paso del sandbox de Twilio a producción?**
1. En Twilio, solicitar un número WhatsApp Business (requiere aprobación Meta, 1-3 días)
2. Actualizar `whatsapp_accounts.is_sandbox = FALSE` y el número real
3. Cambiar `whatsapp_accounts.phone_number` al número aprobado

**¿Y si cae un módulo/subdominio?**
Cada módulo es independiente en Vercel. Si `comercial.iagri.com` falla,
`cultivos.iagri.com` y `sensores.iagri.com` siguen operando.
El único punto compartido es Supabase (base de datos).

**¿Cómo activo la voz del agente?**
Ver `profiles.voice_enabled = TRUE` + integrar ElevenLabs en el frontend.
La Edge Function ya soporta respuesta de audio.
