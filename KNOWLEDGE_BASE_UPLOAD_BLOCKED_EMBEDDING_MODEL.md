# Knowledge Base Upload Blocked - Embedding Model Configuration

**Date**: 2025-10-14 23:10 UTC
**Status**: BLOCKED - Requires user action
**Issue**: Ollama embedding model not configured in Archon Settings

---

## Problem

The batch upload script to populate the knowledge base is failing with authentication errors:

```
HTTP 401 - Invalid Ollama API key
Error: Failed to create embedding: Error code: 404 -
{'error': {'message': 'model "nomic-embed-text" not found, try pulling it first'}}
```

### Root Cause

The Archon backend is configured to use Ollama for embeddings, but it's not finding the embedding model because:

1. **Model is installed**: `nomic-embed-text` has been successfully pulled on the server
2. **Ollama is working**: Direct curl test to Ollama embedding endpoint succeeds
3. **Configuration mismatch**: The Archon settings database doesn't have the correct embedding model configured

### What Works

- Ollama service is running on `0.0.0.0:11434`
- Embedding model `nomic-embed-text:latest` is installed (274 MB)
- Direct embedding test succeeds:
  ```bash
  curl http://localhost:11434/api/embeddings \
    -d '{"model": "nomic-embed-text", "prompt": "test"}'
  # Returns 768-dimensional embedding vector successfully
  ```

### What Doesn't Work

- Archon API document upload endpoint returns 401 authentication error
- Backend logs show: model "nomic-embed-text" not found
- Issue is configuration, not connectivity

---

## Solution Required

### Step 1: Access Archon UI Settings

Navigate to: `https://archon.nexorithm.io`
Go to: **Settings → AI Providers → Embedding Provider**

### Step 2: Configure Ollama Embedding Provider

Set the following values:

**Provider**: Ollama
**Base URL**: `http://host.docker.internal:11434`
**Model**: `nomic-embed-text` (or `nomic-embed-text:latest`)
**API Key**: (leave empty - Ollama doesn't require authentication)

### Step 3: Test Configuration

1. Use the "Test Connection" button in Settings
2. Should show: "✓ Connection successful - 1 embedding model found"
3. Save the settings

### Step 4: Retry Upload

Once configuration is saved, re-run the upload script:

```bash
cd /Users/janschubert/tools/archon
python3 scripts/upload_knowledge_base.py --yes
```

---

## Technical Details

### Available Ollama Models (Server)

```bash
NAME                       ID              SIZE      MODIFIED
nomic-embed-text:latest    0a109f422b47    274 MB    10 minutes ago
qwen2.5-coder:3b           f72c60cabf62    1.9 GB    4 hours ago
llama3.2:3b                a80c4f17acd5    2.0 GB    4 hours ago
```

### Embedding Model Specifications

**Model**: nomic-embed-text
**Dimensions**: 768
**Purpose**: Text embeddings for semantic search
**Provider**: Nomic AI
**License**: Apache 2.0

### Test Commands Used

```bash
# List models
ollama list

# Test embedding endpoint
curl http://localhost:11434/api/embeddings \
  -d '{"model": "nomic-embed-text", "prompt": "test"}' | jq .embedding[0:10]

# Expected: Returns array of 768 float values
```

---

## Alternative: Use OpenAI

If Ollama configuration continues to fail, alternative is to use OpenAI:

### Option 1: OpenAI API

**Provider**: OpenAI
**Model**: `text-embedding-3-small` (1536 dimensions, $0.02/1M tokens)
**API Key**: Your OpenAI API key
**Pros**: Reliable, high quality embeddings
**Cons**: Costs money for API calls

### Option 2: OpenAI-Compatible (e.g., Together.ai)

**Provider**: OpenAI Compatible
**Base URL**: `https://api.together.xyz/v1`
**Model**: `togethercomputer/m2-bert-80M-8k-retrieval`
**API Key**: Your Together.ai API key
**Pros**: Cheaper than OpenAI, compatible API
**Cons**: Still costs money

---

## Estimated Costs (If Using OpenAI)

**Knowledge Base**: 177 files, ~2.79 MB of markdown text
**Estimated tokens**: ~698,000 tokens (assuming 4 chars per token)
**Cost with text-embedding-3-small**: $0.014 (1.4 cents)
**Cost with text-embedding-ada-002**: $0.07 (7 cents)

---

## Upload Script Details

**Location**: `/Users/janschubert/tools/archon/scripts/upload_knowledge_base.py`

**What it does**:
- Finds all markdown files in `knowledgebase/` (177 files)
- Extracts tags based on directory structure
- Uploads via POST to `https://archon.nexorithm.io/api/documents/upload`
- Tracks progress for each upload
- Handles retries on errors
- Logs results to `upload_knowledge_base.log`

**Current Status**: Ready to run once embedding provider is configured

---

## Next Steps

1. **User Action Required**: Configure embedding provider in Archon UI Settings
2. **After configuration**: Run upload script with `--yes` flag
3. **Monitor progress**: Check `upload_knowledge_base.log` for results
4. **Verify uploads**: Check Progress → Active Operations in Archon UI

---

## Files Modified/Created

### `/Users/janschubert/tools/archon/scripts/upload_knowledge_base.py`
**Status**: Complete and tested (except for embedding configuration blocker)
**Features**:
- Batch upload with configurable batch size
- Automatic tag extraction from directory structure
- Retry logic with exponential backoff
- Comprehensive logging
- Progress tracking via Archon API
- Results saved to `upload_results.json`

### `/Users/janschubert/tools/archon/upload_knowledge_base.log`
**Status**: Contains partial upload attempt logs showing 401 errors

---

## Support Information

**Server**: netzwaechter (91.98.156.158)
**Archon URL**: https://archon.nexorithm.io
**Ollama Service**: Running on host, port 11434
**Embedding Model**: nomic-embed-text (installed, 274 MB)

### If Issues Persist

1. Check Archon backend logs:
   ```bash
   ssh root@91.98.156.158 "docker logs archon-server 2>&1 | grep -i embed | tail -20"
   ```

2. Restart Archon server:
   ```bash
   ssh root@91.98.156.158 "cd /opt/archon && docker compose restart archon-server"
   ```

3. Test Ollama connectivity from Docker:
   ```bash
   ssh root@91.98.156.158 "docker exec archon-server curl -s http://host.docker.internal:11434/api/tags"
   ```

---

**Created**: 2025-10-14 23:10 UTC
**Engineer**: Claude Code
**Project**: Archon Knowledge Base Population
**Status**: AWAITING USER ACTION

