# Agent A: Docker & Container Security Remediation

Date: 2025-10-15 18:15 UTC
Agent: A (Container Security Specialist)
Server: 91.98.156.158 (netzwaechter)
Focus: Docker containers, compose files, container runtime security

---

## Agent A Responsibilities

**Primary Focus**: All tasks related to Docker containers, docker-compose.yml files, and container runtime configuration.

**Working Directory**: `/opt/archon/` and container configurations
**No Conflicts With Agent B**: Agent B handles Nginx configuration files only

---

## Task List for Agent A

### IMMEDIATE PRIORITY (Complete First)

#### Task A1: Audit and Remove Suspicious Docker Socket Access ⚠️ CRITICAL
**Status**: PENDING
**Priority**: IMMEDIATE
**Risk**: CRITICAL - Potential unauthorized Docker access

**Objective**: Remove Docker socket from `supabase_vector_archon` container

**Steps**:
1. SSH to server: `ssh root@91.98.156.158`
2. Backup current configuration:
   ```bash
   cd /opt/archon
   cp docker-compose.yml docker-compose.yml.backup.$(date +%Y%m%d_%H%M%S)
   ```
3. Inspect current socket access:
   ```bash
   docker inspect supabase_vector_archon | grep -A3 docker.sock
   ```
4. Edit docker-compose.yml to remove socket mount from `supabase_vector_archon`
5. Apply changes:
   ```bash
   docker compose up -d supabase_vector_archon
   ```
6. Verify container still works:
   ```bash
   docker logs supabase_vector_archon --tail 50
   docker ps | grep supabase_vector
   ```
7. Document why it was removed

**Expected Outcome**: `supabase_vector_archon` no longer has Docker socket access, continues functioning normally

**Rollback Plan**: `docker compose down supabase_vector_archon && cp docker-compose.yml.backup.YYYYMMDD_HHMMSS docker-compose.yml && docker compose up -d`

---

#### Task A2: Investigate archon-server Docker Socket Requirement ⚠️ CRITICAL
**Status**: PENDING
**Priority**: IMMEDIATE
**Risk**: CRITICAL - Potentially unnecessary privileged access

**Objective**: Determine if archon-server legitimately needs Docker socket access

**Steps**:
1. Search archon-server codebase for Docker API usage:
   ```bash
   # From local machine
   cd /Users/janschubert/code-projects/monitoring_firma/netzwaechter-refactored
   grep -r "docker" apps/backend/src --include="*.ts" --include="*.js"
   grep -r "dockerode" apps/backend/src
   grep -r "/var/run/docker.sock" apps/backend/
   ```

2. Check if Docker is imported in dependencies:
   ```bash
   cat apps/backend/package.json | grep -i docker
   ```

3. Review server logs for Docker API calls:
   ```bash
   ssh root@91.98.156.158 "docker logs archon-server --tail 500" | grep -i docker
   ```

4. **Decision Tree**:
   - **If Docker NOT used**: Remove socket mount (high priority)
   - **If Docker IS used**:
     - Document WHY it's needed
     - Implement read-only access if possible
     - Add audit logging
     - Consider alternative (Docker API proxy)

**Expected Outcome**: Clear documentation of whether Docker socket is needed, with justification or removal plan

---

#### Task A3: Add Restart Policies to Archon Services ⚠️ HIGH
**Status**: PENDING
**Priority**: IMMEDIATE
**Risk**: HIGH - Service unavailability if container crashes

**Objective**: Ensure Archon services automatically restart on failure

**Steps**:
1. Backup docker-compose.yml (if not already done in A1)
2. Edit `/opt/archon/docker-compose.yml`
3. Add `restart: unless-stopped` to:
   - `archon-server`
   - `archon-ui`
   - `archon-mcp`
4. Apply changes:
   ```bash
   cd /opt/archon
   docker compose up -d
   ```
5. Verify restart policies:
   ```bash
   docker inspect archon-server --format '{{.HostConfig.RestartPolicy.Name}}'
   docker inspect archon-ui --format '{{.HostConfig.RestartPolicy.Name}}'
   docker inspect archon-mcp --format '{{.HostConfig.RestartPolicy.Name}}'
   ```

**Expected Outcome**: All Archon services have `unless-stopped` restart policy

**Verification**:
```bash
# Test by stopping a container
docker stop archon-server
sleep 5
docker ps | grep archon-server  # Should be running again
```

---

### SHORT-TERM PRIORITY (Week 1)

#### Task A4: Bind Services to 127.0.0.1 Instead of 0.0.0.0 ⚠️ CRITICAL
**Status**: PENDING
**Priority**: SHORT-TERM
**Risk**: CRITICAL - Services exposed to external network

**Objective**: Change port bindings to localhost-only for internal services

**Services to Update**:
1. Supabase Kong (54321)
2. PostgreSQL (54322) - 30 blocked attacks detected
3. PostgREST (54323)
4. Realtime (54324)
5. Supabase Auth (54325, 9999)
6. Ollama (11434) - 3,160 blocked scanning attempts

**Steps**:

1. **Test Current Access** (ensure services work via localhost):
   ```bash
   ssh root@91.98.156.158
   curl -I http://127.0.0.1:54321
   curl -I http://127.0.0.1:3000  # archon-ui
   curl -I http://127.0.0.1:5001  # archon-server
   ```

2. **Backup Configuration**:
   ```bash
   cd /opt/archon
   cp docker-compose.yml docker-compose.yml.backup.localhost_binding.$(date +%Y%m%d_%H%M%S)
   ```

3. **Update Supabase Services**:
   Edit `/opt/archon/docker-compose.yml`:
   ```yaml
   services:
     supabase_kong_archon:
       ports:
         - "127.0.0.1:54321:8000"  # Change from "54321:8000"

     supabase_db_archon:
       ports:
         - "127.0.0.1:54322:5432"  # Change from "54322:5432"

     supabase_rest_archon:
       ports:
         - "127.0.0.1:54323:3000"  # Change from "54323:3000"

     supabase_realtime_archon:
       ports:
         - "127.0.0.1:54324:4000"  # Change from "54324:4000"

     supabase_auth_archon:
       ports:
         - "127.0.0.1:54325:9999"  # If exists
   ```

4. **Find and Update Ollama Configuration**:
   ```bash
   # Find Ollama docker-compose file
   find /opt -name "docker-compose.yml" -exec grep -l "ollama" {} \;

   # Update ollama service
   # Change: "11434:11434" to "127.0.0.1:11434:11434"
   ```

5. **Apply Changes**:
   ```bash
   cd /opt/archon
   docker compose up -d
   ```

6. **Verify Services Still Work**:
   ```bash
   # From server - should work
   curl -I http://127.0.0.1:54321
   curl -I http://127.0.0.1:54322

   # From local machine - should NOT work (should timeout)
   nc -zv -w 5 91.98.156.158 54321  # Should fail
   nc -zv -w 5 91.98.156.158 54322  # Should fail
   nc -zv -w 5 91.98.156.158 11434  # Should fail
   ```

7. **Verify Nginx Proxy Still Works**:
   ```bash
   # From local machine - should work
   curl -I https://archon.nexorithm.io
   curl -I https://arcane.nexorithm.io
   ```

**Expected Outcome**:
- Services bound to 127.0.0.1 only
- External port scans show no open ports except 22, 80, 443
- Nginx proxies still function correctly

**Impact**: LOW - Services accessed via Nginx proxy which uses localhost
**Benefit**: Eliminates single point of failure (firewall-only protection)

---

#### Task A5: Configure Resource Limits for All Containers ⚠️ MEDIUM
**Status**: PENDING
**Priority**: SHORT-TERM
**Risk**: MEDIUM - Resource exhaustion, DoS

**Objective**: Add CPU and memory limits to prevent resource exhaustion

**Recommended Limits**:
| Service | CPU Limit | Memory Limit | Justification |
|---------|-----------|--------------|---------------|
| archon-server | 2.0 | 2G | API backend with DB queries |
| archon-ui | 1.0 | 1G | Static frontend server |
| archon-mcp | 1.0 | 1G | MCP protocol server |
| supabase_db_archon | 4.0 | 4G | PostgreSQL database |
| supabase_kong_archon | 2.0 | 2G | API gateway |
| arcane | 1.0 | 1G | Management UI |
| ollama | 4.0 | 8G | AI model serving |

**Steps**:
1. Edit `/opt/archon/docker-compose.yml`
2. Add resource limits to each service:
   ```yaml
   services:
     archon-server:
       deploy:
         resources:
           limits:
             cpus: '2.0'
             memory: 2G
           reservations:
             cpus: '0.5'
             memory: 512M
   ```

3. Apply changes:
   ```bash
   cd /opt/archon
   docker compose up -d
   ```

4. Monitor for 24 hours to ensure limits aren't too restrictive:
   ```bash
   docker stats --no-stream
   ```

**Expected Outcome**: All containers have resource limits, no container can monopolize system resources

---

### MEDIUM-TERM PRIORITY (Weeks 2-4)

#### Task A6: Run Containers as Non-Root Users ⚠️ MEDIUM
**Status**: PENDING
**Priority**: MEDIUM-TERM
**Risk**: MEDIUM - Privilege escalation if container compromised

**Objective**: Convert containers to run as non-root users (UID 1000+)

**Approach**: Incremental migration (one service at a time)

**Services to Update** (in order):
1. `archon-ui` (stateless, easiest)
2. `archon-mcp` (stateless)
3. `arcane` (needs write access to /app/data volume)
4. `archon-server` (needs investigation)
5. Supabase services (complex, do last)

**Steps for Each Service**:

1. **Test Service Locally** (if possible):
   ```bash
   # From local dev environment
   docker run --user 1000:1000 <image> <command>
   # Check for permission errors
   ```

2. **Update docker-compose.yml**:
   ```yaml
   services:
     archon-ui:
       user: "1000:1000"
   ```

3. **Fix Volume Permissions** (if needed):
   ```bash
   ssh root@91.98.156.158
   docker volume inspect <volume_name>
   # Find Mountpoint
   chown -R 1000:1000 /var/lib/docker/volumes/<volume>/_data
   ```

4. **Apply and Test**:
   ```bash
   docker compose up -d <service>
   docker logs <service> --tail 50
   # Check for permission errors
   ```

5. **Rollback if Issues**:
   ```bash
   # Remove user: line from docker-compose.yml
   docker compose up -d <service>
   ```

**Expected Outcome**: Containers run as non-root, reducing privilege escalation risk

**Note**: Some containers (especially databases) may require root. Document exceptions with justification.

---

#### Task A7: Implement Read-Only Root Filesystems ⚠️ MEDIUM
**Status**: PENDING
**Priority**: MEDIUM-TERM
**Risk**: MEDIUM - Malware persistence, rootkit installation

**Objective**: Make container root filesystems read-only where possible

**Applicable Services** (stateless only):
- `archon-ui` (frontend)
- `archon-mcp` (protocol server)

**Not Applicable**:
- Databases (need writable data)
- `archon-server` (may need temp files)
- `arcane` (needs writable /app/data)

**Steps**:

1. **Test Locally**:
   ```bash
   docker run --read-only --tmpfs /tmp <image>
   # Check if application works
   ```

2. **Update docker-compose.yml**:
   ```yaml
   services:
     archon-ui:
       read_only: true
       tmpfs:
         - /tmp
         - /var/cache/nginx  # If using nginx
   ```

3. **Apply and Monitor**:
   ```bash
   docker compose up -d archon-ui
   docker logs archon-ui --tail 50
   # Watch for "read-only file system" errors
   ```

4. **Identify Required Writable Paths**:
   ```bash
   # Check logs for permission denied errors
   # Add tmpfs mounts as needed
   ```

**Expected Outcome**: Stateless containers have read-only root, reducing attack surface

---

#### Task A8: Drop Excessive Container Capabilities ⚠️ MEDIUM
**Status**: PENDING
**Priority**: MEDIUM-TERM
**Risk**: MEDIUM - Excessive privileges

**Objective**: Drop unnecessary Linux capabilities from containers

**Steps**:

1. **Check Current Capabilities**:
   ```bash
   docker inspect archon-server --format '{{.HostConfig.CapDrop}}'
   docker inspect archon-server --format '{{.HostConfig.CapAdd}}'
   ```

2. **Update docker-compose.yml** (start conservatively):
   ```yaml
   services:
     archon-server:
       cap_drop:
         - NET_RAW        # Can't create raw sockets
         - SYS_CHROOT     # Can't chroot
         - MKNOD          # Can't create device files
         - AUDIT_WRITE    # Can't write audit logs
         - SETFCAP        # Can't set file capabilities
   ```

3. **Test Application**:
   ```bash
   docker compose up -d archon-server
   docker logs archon-server --tail 100
   # Check for capability-related errors
   ```

4. **Gradually Drop More** (if no issues):
   ```yaml
   cap_drop:
     - ALL
   cap_add:
     - CHOWN           # Only if needed for file ownership
     - DAC_OVERRIDE    # Only if needed for permissions
   ```

**Expected Outcome**: Containers run with minimal capabilities required for operation

**Note**: Test thoroughly - dropping wrong capability can break application

---

#### Task A9: Implement Container Health Checks ⚠️ LOW
**Status**: PENDING
**Priority**: MEDIUM-TERM
**Risk**: LOW - Monitoring and availability

**Objective**: Add health checks for automatic failure detection and recovery

**Steps**:

1. **Add Health Checks to docker-compose.yml**:
   ```yaml
   services:
     archon-server:
       healthcheck:
         test: ["CMD", "curl", "-f", "http://localhost:5001/health"]
         interval: 30s
         timeout: 10s
         retries: 3
         start_period: 40s

     archon-ui:
       healthcheck:
         test: ["CMD", "curl", "-f", "http://localhost:3000"]
         interval: 30s
         timeout: 10s
         retries: 3
         start_period: 10s

     arcane:
       healthcheck:
         test: ["CMD", "curl", "-f", "http://localhost:3552/health"]
         interval: 30s
         timeout: 10s
         retries: 3
         start_period: 30s
   ```

2. **Install curl in Containers** (if not present):
   - May require updating Dockerfiles
   - Alternative: Use `wget`, `nc`, or native health check endpoints

3. **Apply Changes**:
   ```bash
   docker compose up -d
   ```

4. **Monitor Health Status**:
   ```bash
   docker ps  # Shows (healthy) or (unhealthy)
   docker inspect archon-server --format '{{.State.Health.Status}}'
   ```

**Expected Outcome**: Containers automatically marked unhealthy when non-responsive, enabling monitoring alerts

---

### LONG-TERM PRIORITY (Months 2-3)

#### Task A10: Implement Container Security Scanning ⚠️ LOW
**Status**: PENDING
**Priority**: LONG-TERM
**Risk**: LOW - Vulnerability detection

**Objective**: Scan container images for vulnerabilities

**Steps**:

1. **Install Trivy**:
   ```bash
   ssh root@91.98.156.158
   wget https://github.com/aquasecurity/trivy/releases/download/v0.44.0/trivy_0.44.0_Linux-64bit.tar.gz
   tar -xzf trivy_0.44.0_Linux-64bit.tar.gz
   mv trivy /usr/local/bin/
   ```

2. **Scan All Running Images**:
   ```bash
   docker ps --format '{{.Image}}' | sort -u | while read img; do
       echo "=== Scanning $img ==="
       trivy image --severity HIGH,CRITICAL "$img"
   done > /root/container-vulnerability-scan-$(date +%Y%m%d).txt
   ```

3. **Create Weekly Scan Script**:
   ```bash
   cat > /usr/local/bin/weekly-container-scan.sh << 'EOF'
   #!/bin/bash
   REPORT_FILE="/root/security-reports/container-scan-$(date +%Y%m%d).txt"
   mkdir -p /root/security-reports

   echo "Container Security Scan - $(date)" > "$REPORT_FILE"
   echo "======================================" >> "$REPORT_FILE"

   docker ps --format '{{.Image}}' | sort -u | while read img; do
       echo "" >> "$REPORT_FILE"
       echo "=== $img ===" >> "$REPORT_FILE"
       trivy image --severity HIGH,CRITICAL "$img" >> "$REPORT_FILE" 2>&1
   done

   # Email report (if mail configured)
   # mail -s "Weekly Container Security Scan" admin@nexorithm.io < "$REPORT_FILE"
   EOF
   chmod +x /usr/local/bin/weekly-container-scan.sh
   ```

4. **Schedule Weekly Scans**:
   ```bash
   crontab -e
   # Add: 0 2 * * 0 /usr/local/bin/weekly-container-scan.sh
   ```

**Expected Outcome**: Weekly vulnerability reports for all container images

---

#### Task A11: Implement Docker Bench Security Audit ⚠️ LOW
**Status**: PENDING
**Priority**: LONG-TERM
**Risk**: LOW - Compliance verification

**Objective**: Run automated CIS Docker Benchmark checks

**Steps**:

1. **Install Docker Bench**:
   ```bash
   ssh root@91.98.156.158
   git clone https://github.com/docker/docker-bench-security.git /opt/docker-bench-security
   cd /opt/docker-bench-security
   ```

2. **Run Initial Audit**:
   ```bash
   sh docker-bench-security.sh > /root/docker-bench-initial-$(date +%Y%m%d).txt
   ```

3. **Review Findings**:
   ```bash
   less /root/docker-bench-initial-$(date +%Y%m%d).txt
   # Focus on [WARN] items
   ```

4. **Create Monthly Audit Script**:
   ```bash
   cat > /usr/local/bin/monthly-docker-audit.sh << 'EOF'
   #!/bin/bash
   REPORT_FILE="/root/security-reports/docker-bench-$(date +%Y%m%d).txt"
   mkdir -p /root/security-reports

   cd /opt/docker-bench-security
   sh docker-bench-security.sh > "$REPORT_FILE"

   # Count warnings
   WARNS=$(grep -c "\[WARN\]" "$REPORT_FILE")
   echo "" >> "$REPORT_FILE"
   echo "Total Warnings: $WARNS" >> "$REPORT_FILE"
   EOF
   chmod +x /usr/local/bin/monthly-docker-audit.sh
   ```

5. **Schedule Monthly Audits**:
   ```bash
   crontab -e
   # Add: 0 3 1 * * /usr/local/bin/monthly-docker-audit.sh
   ```

**Expected Outcome**: Monthly CIS Docker Benchmark compliance reports

---

## Task Dependencies

```
A1 (Remove vector socket) ─── Can run immediately
A2 (Audit server socket) ───── Can run immediately
A3 (Restart policies) ──────── Can run immediately

A4 (Localhost binding) ──────── Requires A1, A2, A3 complete
A5 (Resource limits) ───────── Can run after A3

A6 (Non-root users) ────────── Requires A4, A5 complete
A7 (Read-only FS) ──────────── Requires A6 complete
A8 (Drop capabilities) ─────── Requires A6 complete
A9 (Health checks) ─────────── Can run anytime after A3

A10 (Security scanning) ────── Independent, can run anytime
A11 (Docker bench) ─────────── Independent, can run anytime
```

---

## Verification Checklist

After completing all tasks, verify:

- [ ] No containers have Docker socket except arcane (with documented justification)
- [ ] All services bound to 127.0.0.1 (not 0.0.0.0)
- [ ] All containers have restart policies
- [ ] All containers have resource limits
- [ ] Critical containers run as non-root users
- [ ] Stateless containers have read-only filesystems
- [ ] Unnecessary capabilities dropped
- [ ] Health checks configured
- [ ] Security scanning automated
- [ ] Docker bench audit scheduled

---

## Rollback Procedures

All configurations backed up with timestamps:
```bash
# List all backups
ls -lah /opt/archon/*.backup.*

# Rollback to specific backup
cd /opt/archon
docker compose down
cp docker-compose.yml.backup.YYYYMMDD_HHMMSS docker-compose.yml
docker compose up -d

# Verify services
docker ps
curl -I https://archon.nexorithm.io
```

---

## Communication with Agent B

**No Conflicts**: Agent B handles Nginx only
**Coordination Point**: After A4 (localhost binding), verify with Agent B that proxies still work

**Test After A4**:
```bash
# Agent B should verify:
curl -I https://archon.nexorithm.io      # Should work
curl -I https://arcane.nexorithm.io      # Should work
curl -I https://strawa.cockpit365.pro    # Should work
```

---

**Agent A Start Date**: 2025-10-15 18:15 UTC
**Expected Completion**: Week 1 for immediate/short-term tasks
**Progress Tracking**: Update this file with completion status
