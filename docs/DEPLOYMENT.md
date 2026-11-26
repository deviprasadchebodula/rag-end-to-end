# Deployment guide

## Actual demonstration architecture

Browser → HTTPS reverse proxy (Caddy) → Azure Linux VM / Docker → FastAPI → Pinecone and OpenRouter.

The project was demonstrated with a small Azure VM and disk-backed swap. Swap helped manage memory pressure but is slower than RAM. A provider access failure led to switching from Groq to OpenRouter. The active deployment was not Azure App Service: the attempted App Service creation was blocked by subscription quota.

## Container preparation

Build from the repository using the Dockerfile. Supply credentials at runtime, never through Docker build arguments or copied secret files.

```bash
docker build --platform linux/amd64 -t rag-assistant:demo .
docker run --rm --env-file .env -p 127.0.0.1:8000:8000 rag-assistant:demo
```

Verify the homepage, PDF upload, and an actual answer from a non-confidential sample document before pushing or exposing the service.

## Azure VM deployment checklist

- Use an authorized subscription and confirm budget, region and outbound provider availability.
- Install Docker and use an appropriate Linux image and architecture.
- Pull a verified container image; store runtime credentials securely.
- Bind the application to loopback behind the reverse proxy.
- Configure persistent storage and backups for uploaded files if needed.
- Configure a DNS hostname and HTTPS with a reverse proxy.
- Restrict SSH to trusted IPs and secure application access before public use.
- Enable an appropriate restart policy; monitor memory, disk and provider errors.

A VM can operate while the developer's laptop is off, but requires active cloud resources and a working external API.

## Azure Container Registry / App Service alternative

The demonstration image was successfully uploaded to ACR. The later Web App attempt was blocked by zero available App Service quota. To use this alternative, verify quota, plan support, cost and memory before provisioning. Configure managed identity with registry pull permission, internal container port 8000 and runtime environment variables. Do not assume a free plan is sufficient.

## Validation and shutdown

Confirm HTTPS and document question answering from an authorized external client. Inspect logs if requests fail. No production uptime or latency guarantee is claimed.

Before trial expiry, preserve the source code, required documents and configuration separately from credentials. With the subscription owner's permission, remove unused billable resources when no longer needed. Stopping a VM does not necessarily eliminate all disk, IP or registry costs.
