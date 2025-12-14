# ReplyHQ.ai Production Deployment Guide

This guide provides step-by-step instructions for deploying the ReplyHQ.ai application to production using Railway (backend) and Vercel (frontend).

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Prerequisites](#prerequisites)
3. [Railway Deployment (Backend)](#railway-deployment-backend)
4. [Vercel Deployment (Frontend)](#vercel-deployment-frontend)
5. [Domain Configuration](#domain-configuration)
6. [Environment Variables Reference](#environment-variables-reference)
7. [Post-Deployment Verification](#post-deployment-verification)
8. [Troubleshooting](#troubleshooting)
9. [Maintenance & Operations](#maintenance--operations)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                          replyhq.ai                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│    ┌────────────────────┐              ┌────────────────────┐       │
│    │      Vercel        │    HTTPS     │      Railway       │       │
│    │    (Frontend)      │ ──────────── │     (Backend)      │       │
│    │                    │              │                    │       │
│    │   replyhq.ai       │              │  api.replyhq.ai    │       │
│    │   Next.js 15       │              │  FastAPI + Python  │       │
│    │   React 19         │              │  LangGraph AI      │       │
│    └────────────────────┘              └─────────┬──────────┘       │
│                                                  │                   │
│                                    ┌─────────────┴─────────────┐    │
│                                    │                           │    │
│                           ┌────────┴────────┐    ┌─────────────┴──┐ │
│                           │   PostgreSQL    │    │     Redis      │ │
│                           │   (Railway)     │    │   (Railway)    │ │
│                           └─────────────────┘    └────────────────┘ │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

**External Integrations:**
- Instagram Graph API (Meta)
- OpenAI API (GPT models)
- Shopify Admin API

---

## Prerequisites

Before starting deployment, ensure you have:

### Accounts Required
- [ ] [Railway Account](https://railway.app/) (Pro plan recommended for production)
- [ ] [Vercel Account](https://vercel.com/) (Pro plan recommended for custom domains)
- [ ] [GitHub Account](https://github.com/) (repository connected to both platforms)
- [ ] Domain registrar access for `replyhq.ai`

### API Keys & Credentials
- [ ] **OpenAI API Key** - [Get from OpenAI Platform](https://platform.openai.com/api-keys)
- [ ] **Meta/Instagram App** - [Meta Developer Console](https://developers.facebook.com/)
  - App ID and App Secret
  - Instagram Business Account connected
  - Webhook configured
- [ ] **Shopify Admin API** - [Shopify Partners](https://partners.shopify.com/)
  - Store URL
  - API Key
  - Admin Access Token

### Tools
- [ ] Git installed locally
- [ ] Node.js 20.x (for local testing)
- [ ] Python 3.11 (for local testing)
- [ ] Railway CLI (optional): `npm install -g @railway/cli`
- [ ] Vercel CLI (optional): `npm install -g vercel`

---

## Railway Deployment (Backend)

### Step 1: Create a New Railway Project

1. Go to [railway.app](https://railway.app/) and log in
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Connect your GitHub account if not already connected
5. Select the `saas-dm` repository
6. Railway will detect the monorepo structure

### Step 2: Configure the Backend Service

1. In your Railway project, click **"New Service"** → **"GitHub Repo"**
2. Select the same repository
3. Configure the service:
   - **Root Directory**: `backend`
   - **Builder**: Dockerfile (auto-detected from `railway.json`)

4. The service will start building. It will fail initially because environment variables aren't set yet.

### Step 3: Add PostgreSQL Database

1. In the Railway project dashboard, click **"New Service"**
2. Select **"Database"** → **"PostgreSQL"**
3. Railway will provision a PostgreSQL instance
4. Click on the PostgreSQL service → **"Variables"** tab
5. Copy the `DATABASE_URL` - you'll need this for the backend

**Important**: The `DATABASE_URL` format from Railway is:
```
postgresql://user:password@host:port/database
```

You need to modify it for async support:
```
postgresql+asyncpg://user:password@host:port/database
```

### Step 4: Add Redis Cache

1. Click **"New Service"** → **"Database"** → **"Redis"**
2. Railway will provision a Redis instance
3. Copy the `REDIS_URL` from the Redis service variables

### Step 5: Configure Backend Environment Variables

1. Click on your backend service
2. Go to the **"Variables"** tab
3. Add the following environment variables:

```bash
# Database (modify the Railway-provided URL)
DATABASE_URL=postgresql+asyncpg://[copy-from-postgresql-service]

# Redis (copy from Redis service)
REDIS_URL=[copy-from-redis-service]

# Security - GENERATE A NEW SECRET KEY!
# Run: openssl rand -hex 32
SECRET_KEY=your-generated-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS - Your production domains
CORS_ORIGINS=["https://replyhq.ai", "https://www.replyhq.ai"]

# Instagram/Meta
INSTAGRAM_VERIFY_TOKEN=your-webhook-verify-token
INSTAGRAM_APP_SECRET=your-instagram-app-secret
INSTAGRAM_ACCESS_TOKEN=your-instagram-page-access-token
INSTAGRAM_PAGE_ID=your-instagram-page-id

# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-4.1-mini
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=500

# Shopify
SHOPIFY_STORE_URL=your-store.myshopify.com
SHOPIFY_API_KEY=your-shopify-api-key
SHOPIFY_ACCESS_TOKEN=shpat_your-access-token
```

### Step 6: Deploy and Verify

1. After adding variables, Railway will automatically redeploy
2. Watch the deployment logs for any errors
3. Once deployed, click **"Settings"** → **"Networking"**
4. Generate a public domain or add your custom domain (`api.replyhq.ai`)

### Step 7: Run Database Migrations

Migrations run automatically on deployment (configured in `railway.json`). Verify by checking the deployment logs for:
```
INFO  [alembic.runtime.migration] Running upgrade -> 001_create_users_table
INFO  [alembic.runtime.migration] Running upgrade 001 -> 002_create_conversation_tables
```

---

## Vercel Deployment (Frontend)

### Step 1: Import Project to Vercel

1. Go to [vercel.com](https://vercel.com/) and log in
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository
4. Configure the project:
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### Step 2: Configure Environment Variables

In Vercel project settings → **Environment Variables**, add:

```bash
NEXT_PUBLIC_API_URL=https://api.replyhq.ai
```

**Note**: Only `NEXT_PUBLIC_` prefixed variables are exposed to the browser.

### Step 3: Deploy

1. Click **"Deploy"**
2. Vercel will build and deploy your frontend
3. You'll get a `.vercel.app` preview URL immediately

### Step 4: Configure Production Domain

1. Go to **Settings** → **Domains**
2. Add `replyhq.ai` and `www.replyhq.ai`
3. Vercel will provide DNS configuration instructions

---

## Domain Configuration

### DNS Records for replyhq.ai

Configure these DNS records at your domain registrar:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | `76.76.21.21` | 3600 |
| CNAME | www | `cname.vercel-dns.com` | 3600 |
| CNAME | api | `[your-railway-domain].railway.app` | 3600 |

### SSL/HTTPS Configuration

**Vercel (Frontend):**
- SSL is automatically provisioned via Let's Encrypt
- No configuration needed
- Automatic HTTPS redirect enabled by default

**Railway (Backend):**
- SSL is automatically provisioned for all domains
- Custom domains get automatic SSL certificates
- HTTPS is enforced by default

### Verify Domain Configuration

After DNS propagation (can take up to 48 hours):

```bash
# Check frontend
curl -I https://replyhq.ai

# Check backend
curl -I https://api.replyhq.ai/health
```

---

## Environment Variables Reference

### Backend (Railway)

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | ✅ | PostgreSQL connection string with `+asyncpg` |
| `REDIS_URL` | ✅ | Redis connection string |
| `SECRET_KEY` | ✅ | JWT signing key (32+ chars) |
| `ALGORITHM` | ❌ | JWT algorithm (default: HS256) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | ❌ | Token expiry (default: 30) |
| `CORS_ORIGINS` | ✅ | JSON array of allowed origins |
| `INSTAGRAM_VERIFY_TOKEN` | ✅ | Meta webhook verification token |
| `INSTAGRAM_APP_SECRET` | ✅ | Instagram app secret |
| `INSTAGRAM_ACCESS_TOKEN` | ✅ | Page access token |
| `INSTAGRAM_PAGE_ID` | ✅ | Instagram business page ID |
| `OPENAI_API_KEY` | ✅ | OpenAI API key |
| `OPENAI_API_BASE` | ❌ | OpenAI API URL (default: official) |
| `OPENAI_MODEL` | ❌ | Model name (default: gpt-4.1-mini) |
| `OPENAI_TEMPERATURE` | ❌ | Response creativity (default: 0.7) |
| `OPENAI_MAX_TOKENS` | ❌ | Max response tokens (default: 500) |
| `SHOPIFY_STORE_URL` | ✅ | Shopify store URL |
| `SHOPIFY_API_KEY` | ✅ | Shopify API key |
| `SHOPIFY_ACCESS_TOKEN` | ✅ | Shopify admin token |

### Frontend (Vercel)

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_API_URL` | ✅ | Backend API URL (e.g., https://api.replyhq.ai) |

---

## Post-Deployment Verification

### 1. Backend Health Check

```bash
curl https://api.replyhq.ai/health
```

Expected response:
```json
{"status": "healthy"}
```

### 2. Frontend Accessibility

```bash
curl -I https://replyhq.ai
```

Expected: `HTTP/2 200` status

### 3. API Connectivity Test

```bash
# Test authentication endpoint
curl -X POST https://api.replyhq.ai/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpassword123"}'
```

### 4. CORS Verification

Open browser developer tools on `https://replyhq.ai` and check:
- Network tab shows successful API calls
- No CORS errors in console

### 5. Instagram Webhook Verification

1. Go to [Meta Developer Console](https://developers.facebook.com/)
2. Navigate to your app → Webhooks
3. Add webhook URL: `https://api.replyhq.ai/webhooks/instagram`
4. Verify token should match `INSTAGRAM_VERIFY_TOKEN`
5. Subscribe to `messages` and `messaging_postbacks` events

### 6. Database Verification

Check Railway logs for successful migration:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
```

---

## Troubleshooting

### Common Issues

#### 1. "Application failed to start" on Railway

**Cause**: Missing environment variables or database connection issues.

**Solution**:
1. Check all required environment variables are set
2. Verify `DATABASE_URL` has `+asyncpg` prefix
3. Check Railway logs for specific error messages

#### 2. CORS Errors in Browser

**Cause**: `CORS_ORIGINS` not properly configured.

**Solution**:
1. Ensure `CORS_ORIGINS` is a valid JSON array
2. Include both `https://replyhq.ai` AND `https://www.replyhq.ai`
3. Redeploy after changing

#### 3. Database Migrations Failed

**Cause**: Database not ready or connection string incorrect.

**Solution**:
1. Verify PostgreSQL service is running on Railway
2. Check `DATABASE_URL` format includes `+asyncpg`
3. Manually run migrations:
   ```bash
   railway run alembic upgrade head
   ```

#### 4. 502 Bad Gateway on Vercel

**Cause**: Backend API not responding.

**Solution**:
1. Check Railway backend is running
2. Verify `NEXT_PUBLIC_API_URL` is correct
3. Test backend health endpoint directly

#### 5. "Invalid token" Errors

**Cause**: `SECRET_KEY` mismatch or token expired.

**Solution**:
1. Ensure `SECRET_KEY` is consistent across deployments
2. Check `ACCESS_TOKEN_EXPIRE_MINUTES` setting
3. Clear browser localStorage and re-authenticate

### Viewing Logs

**Railway:**
1. Go to your service → **Deployments** tab
2. Click on a deployment → **View Logs**

**Vercel:**
1. Go to your project → **Deployments** tab
2. Click on a deployment → **Functions** or **Runtime Logs**

---

## Maintenance & Operations

### Updating the Application

1. Push changes to the `main` branch
2. Both Railway and Vercel will auto-deploy

### Manual Deployment

**Railway:**
```bash
railway up
```

**Vercel:**
```bash
vercel --prod
```

### Database Backups

Railway PostgreSQL provides automatic daily backups. To create a manual backup:

1. Go to PostgreSQL service on Railway
2. Click **"Backups"** tab
3. Click **"Create Backup"**

### Scaling

**Railway:**
- Adjust instance count in service settings
- Enable horizontal scaling on Pro plan

**Vercel:**
- Serverless functions scale automatically
- Configure function memory/timeout in `vercel.json` if needed

### Monitoring

Recommended monitoring tools:
- **Uptime**: [UptimeRobot](https://uptimerobot.com/) or [Better Uptime](https://betteruptime.com/)
- **Error Tracking**: [Sentry](https://sentry.io/)
- **Analytics**: [Vercel Analytics](https://vercel.com/analytics) or Google Analytics

### Rollback

**Railway:**
1. Go to **Deployments** tab
2. Find the previous working deployment
3. Click **"Redeploy"**

**Vercel:**
1. Go to **Deployments** tab
2. Find the previous working deployment
3. Click **"..."** → **"Promote to Production"**

---

## Quick Reference

### Deployment URLs

| Service | URL |
|---------|-----|
| Frontend (Production) | https://replyhq.ai |
| Backend API | https://api.replyhq.ai |
| Health Check | https://api.replyhq.ai/health |
| API Docs | https://api.replyhq.ai/docs |

### Key Commands

```bash
# Generate secret key
openssl rand -hex 32

# Test API health
curl https://api.replyhq.ai/health

# Railway CLI login
railway login

# Vercel CLI login
vercel login

# View Railway logs
railway logs

# View Vercel logs
vercel logs
```

### Support Resources

- [Railway Documentation](https://docs.railway.app/)
- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

## Security Checklist

Before going live, ensure:

- [ ] `SECRET_KEY` is a strong, unique value (not the default)
- [ ] `CORS_ORIGINS` only includes production domains (no wildcards)
- [ ] All API keys are production keys (not test/development)
- [ ] HTTPS is enforced on all endpoints
- [ ] Database is not publicly accessible (Railway handles this)
- [ ] `.env` files are not committed to Git
- [ ] Error messages don't expose sensitive information
- [ ] Rate limiting is configured for public endpoints

---

*Last updated: December 2024*
