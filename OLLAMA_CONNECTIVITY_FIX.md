# Ollama Connectivity Fix

## Current Status

- **Knowledge Items Uploaded**: 176/177 files (99.4% success rate)
- **Knowledge Items Indexed**: Only 3 out of 176 (1.7%)
- **Root Cause**: Ollama connectivity issue preventing embedding generation
- **Remaining Documents**: 173 documents waiting for embeddings

## Problem

The uploaded documents cannot be fully indexed because:
1. Documents are uploaded and stored successfully
2. Backend attempts to generate embeddings using Ollama
3. Ollama connection fails (URL: `host.docker.internal:11434`)
4. Documents remain in pending state without embeddings

## Solution

### Step 1: Access Settings UI
1. Navigate to https://archon.nexorithm.io/settings
2. Scroll to "RAG Settings" section

### Step 2: Configure Ollama Instance
1. Find "Ollama Configuration" panel
2. Update the embedding provider base URL from:
   - **Current (incorrect)**: `http://host.docker.internal:11434`
   - **New (correct)**: `http://172.18.0.1:11434`

### Step 3: Verify Connection
1. Click "Test Connection" button
2. Ensure connection status shows "healthy"
3. Save the configuration

### Step 4: Trigger Re-processing
Once Ollama is connected:
1. The backend should automatically process pending documents
2. Embeddings will be generated for the 173 waiting documents
3. Documents will become fully searchable in the knowledge base

## Technical Details

### Docker Network Configuration
- **Issue**: `host.docker.internal` doesn't resolve correctly from within Docker container
- **Fix**: Use Docker bridge network IP `172.18.0.1` to access host services
- **Network**: `supabase_network_archon` (Docker bridge)

### Ollama Service
- **Host Location**: Running on host machine at port 11434
- **Container Access**: Must use host's Docker bridge IP (172.18.0.1)
- **Model Required**: `nomic-embed-text` for embeddings

### Alternative Solution (if 172.18.0.1 doesn't work)
Find the correct Docker bridge gateway IP:
```bash
docker network inspect supabase_network_archon | grep Gateway
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

---
*Last Updated: 2025-10-15*
*Issue Tracking: Backend endpoint fixed, Ollama configuration remains*
