# Ollama Connectivity Fix

## Current Status

- **Knowledge Items Uploaded**: 176/177 files (99.4% success rate)
- **Knowledge Items Indexed**: Only 3 out of 176 (1.7%)
- **Root Cause**: Ollama connectivity issue preventing embedding generation
- **Remaining Documents**: 173 documents waiting for embeddings
- **Default URL Updated**: New installations will use correct URL automatically

## Problem

The uploaded documents cannot be fully indexed because:
1. Documents are uploaded and stored successfully
2. Backend attempts to generate embeddings using Ollama
3. Ollama connection fails (old default URL: `host.docker.internal:11434`)
4. Documents remain in pending state without embeddings

## Solution

### For Existing Installations

#### Step 1: Access Settings UI
1. Navigate to https://archon.nexorithm.io/settings
2. Scroll to "RAG Settings" section

#### Step 2: Configure Ollama Instance
1. Find "Ollama Configuration" panel
2. Update the embedding provider base URL from:
   - **Old default**: `http://host.docker.internal:11434`
   - **New default**: `http://172.18.0.1:11434`

#### Step 3: Verify Connection
1. Click "Test Connection" button
2. Ensure connection status shows "healthy"
3. Save the configuration

#### Step 4: Trigger Re-processing
Once Ollama is connected:
1. The backend should automatically process pending documents
2. Embeddings will be generated for the 173 waiting documents
3. Documents will become fully searchable in the knowledge base

### For New Installations

**No action required!** The default Ollama URL has been updated to `http://172.18.0.1:11434` in:
- `python/src/server/services/provider_discovery_service.py`
- `python/src/server/services/credential_service.py`
- `python/src/server/services/llm_provider_service.py`

## Technical Details

### Docker Network Configuration
- **Issue**: `host.docker.internal` doesn't resolve correctly from within Docker containers on all systems
- **Fix**: Use Docker bridge network IP `172.18.0.1` to access host services
- **Network**: `supabase_network_archon` (Docker bridge)
- **Applies to**: All Docker-based deployments

### Ollama Service
- **Host Location**: Running on host machine at port 11434
- **Container Access**: Must use host's Docker bridge IP (172.18.0.1)
- **Model Required**: `nomic-embed-text` for embeddings
- **Firewall**: Ensure port 11434 is accessible from Docker containers

### Firewall Configuration

#### UFW (Ubuntu/Debian)
```bash
# Allow Docker containers to access Ollama on host
sudo ufw allow in on docker0 to any port 11434
sudo ufw allow in on br-+ to any port 11434
```

#### Firewalld (RHEL/CentOS/Fedora)
```bash
# Add Docker bridge to trusted zone
sudo firewall-cmd --permanent --zone=trusted --add-interface=docker0
sudo firewall-cmd --permanent --zone=trusted --add-port=11434/tcp
sudo firewall-cmd --reload
```

#### iptables (Manual)
```bash
# Allow traffic from Docker bridge to host on port 11434
sudo iptables -I INPUT -i docker0 -p tcp --dport 11434 -j ACCEPT
sudo iptables -I INPUT -i br-+ -p tcp --dport 11434 -j ACCEPT
```

### Finding Your Docker Bridge IP

If `172.18.0.1` doesn't work, find your Docker bridge gateway IP:

```bash
# Find the Docker network name
docker network ls | grep supabase

# Inspect the network to find the gateway IP
docker network inspect supabase_network_archon | grep Gateway

# Alternative: Check Docker bridge IP
ip addr show docker0 | grep inet
```

Then use that IP address in the Ollama configuration.

## Expected Results After Fix

1. **Immediate**: Connection test shows "healthy"
2. **Within minutes**: Backend begins processing pending documents
3. **Within 10-30 minutes**: All 173 documents fully indexed with embeddings
4. **Knowledge base**: Full-text and semantic search enabled for all documents

## Verification

After configuration:
1. Check knowledge base UI - should see document count increase
2. Try searching for content from uploaded documents
3. Inspector modal should show document chunks when clicking cards

## Code Changes Made

### Backend Defaults Updated
The following files now use `http://172.18.0.1:11434` as the default Ollama URL:

1. **Provider Discovery Service** (`python/src/server/services/provider_discovery_service.py:27`)
   ```python
   DEFAULT_OLLAMA_URL = "http://172.18.0.1:11434"
   ```

2. **Credential Service** (`python/src/server/services/credential_service.py:523`)
   ```python
   return rag_settings.get("LLM_BASE_URL", "http://172.18.0.1:11434/v1")
   ```

3. **LLM Provider Service** (`python/src/server/services/llm_provider_service.py:586`)
   ```python
   fallback_url = rag_settings.get("LLM_BASE_URL", "http://172.18.0.1:11434")
   ```

---
*Last Updated: 2025-10-15*
*Status: Defaults updated, existing installations require manual configuration update*
