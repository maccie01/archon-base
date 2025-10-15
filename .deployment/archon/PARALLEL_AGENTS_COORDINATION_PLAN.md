# Parallel Agents Coordination Plan

Date: 2025-10-15 18:15 UTC
Server: 91.98.156.158 (netzwaechter)
Objective: Execute security remediation with 2 agents working in parallel

---

## Overview

This plan coordinates 2 specialized agents to execute security remediation tasks in parallel without conflicts.

**Agent A**: Docker & Container Security Specialist
**Agent B**: Nginx & Network Security Specialist

**Key Principle**: No file overlap = No conflicts

---

## Agent Responsibilities

### Agent A: Docker & Container Security
**Working Directory**: `/opt/archon/` (server) and local codebase
**Files Modified**:
- `/opt/archon/docker-compose.yml`
- Docker container configurations
- Container volumes and permissions

**Tasks**: 11 tasks (A1-A11)
**Estimated Time**:
- Immediate: 2-3 hours
- Short-term: 1 week
- Medium-term: 3-4 weeks
- Long-term: 2-3 months

**Task File**: `AGENT_A_SECURITY_REMEDIATION.md`

---

### Agent B: Nginx & Network Security
**Working Directory**: `/etc/nginx/` (server)
**Files Modified**:
- `/etc/nginx/nginx.conf`
- `/etc/nginx/sites-available/*`
- `/etc/logrotate.d/nginx-custom`
- Security monitoring scripts

**Tasks**: 12 tasks (B1-B12)
**Estimated Time**:
- Immediate: 2-3 hours
- Short-term: 1 week
- Medium-term: 3-4 weeks
- Long-term: 2-3 months

**Task File**: `AGENT_B_SECURITY_REMEDIATION.md`

---

## File Ownership Matrix

| File/Directory | Agent A | Agent B | Conflict Risk |
|----------------|---------|---------|---------------|
| `/opt/archon/docker-compose.yml` | ✅ Owner | ❌ No access | **NONE** |
| `/etc/nginx/nginx.conf` | ❌ No access | ✅ Owner | **NONE** |
| `/etc/nginx/sites-available/*` | ❌ No access | ✅ Owner | **NONE** |
| Docker containers | ✅ Owner | ❌ No access | **NONE** |
| SSL/TLS configuration | ❌ No access | ✅ Owner | **NONE** |
| Rate limiting zones | ❌ No access | ✅ Owner | **NONE** |
| Security headers | ❌ No access | ✅ Owner | **NONE** |

**Conclusion**: ZERO file conflicts possible

---

## Coordination Points

### Coordination Point 1: Localhost Binding Change

**When**: After Agent A completes Task A4 (bind services to 127.0.0.1)

**What Happens**:
1. Agent A changes Docker port bindings from `0.0.0.0:PORT` to `127.0.0.1:PORT`
2. Services restart with new bindings
3. Agent A notifies Agent B: "Task A4 complete - localhost binding applied"

**Agent B Action**:
4. Agent B runs Task B2: Verify Nginx proxies still work
5. Tests:
   - `curl -I https://archon.nexorithm.io` (should work)
   - `curl -I https://arcane.nexorithm.io` (should work)
   - WebSocket connections (should work)
6. Agent B reports back: "Task B2 complete - proxies verified"

**Timeline**:
- Agent A completes A4: ~Day 2-3
- Agent B completes B2: ~30 minutes after A4
- Total delay: Minimal (30 minutes)

**If Issues Found**:
- Agent B documents specific proxy issues
- Agent A investigates Docker networking
- Rollback plan available in both task files

---

### Coordination Point 2: Final Integration Testing

**When**: After both agents complete all immediate + short-term tasks

**What Happens**:
1. Both agents complete their Week 1 tasks
2. Joint testing session:
   - External port scan: `nmap -sV -sC -p- archon.nexorithm.io`
   - SSL/TLS test: `nmap --script ssl-enum-ciphers -p 443 archon.nexorithm.io`
   - Security headers: `curl -I https://archon.nexorithm.io`
   - Container security: `docker ps --format '{{.Names}}' | xargs docker inspect`
   - Service functionality: Test all 3 sites work correctly

3. Generate joint completion report

**Timeline**:
- Week 1 completion: ~Day 7
- Joint testing: ~2-3 hours
- Report generation: ~1 hour

---

## Execution Timeline

### Phase 1: Immediate Priority (Days 1-2)

**Agent A Tasks** (can run immediately):
- A1: Remove Docker socket from supabase_vector ⏱️ 30 min
- A2: Audit archon-server Docker socket ⏱️ 1 hour
- A3: Add restart policies ⏱️ 30 min

**Agent B Tasks** (can run immediately):
- B1: Disable deprecated TLS protocols ⏱️ 30 min
- B3: Harden Netzwaechter site ⏱️ 1-2 hours
- B4: Strengthen SSL ciphers ⏱️ 30 min

**Parallel Execution**: YES - No conflicts
**Estimated Completion**: End of Day 1

---

### Phase 2: Short-Term Priority (Days 3-7)

**Agent A Tasks**:
- A4: Bind services to localhost ⏱️ 2-3 hours
  - **Coordination Trigger**: Notify Agent B when complete
- A5: Configure resource limits ⏱️ 2 hours

**Agent B Tasks**:
- B2: Verify WebSocket after A4 ⏱️ 30 min
  - **Coordination Wait**: Wait for Agent A Task A4
- B5: HTTP/2 optimization ⏱️ 1 hour
- B6: Advanced rate limiting ⏱️ 2 hours

**Parallel Execution**: Mostly YES (except B2 waits for A4)
**Estimated Completion**: End of Week 1

---

### Phase 3: Medium-Term Priority (Weeks 2-4)

**Agent A Tasks**:
- A6: Run containers as non-root ⏱️ 1-2 weeks
- A7: Read-only filesystems ⏱️ 3-4 days
- A8: Drop capabilities ⏱️ 3-4 days
- A9: Container health checks ⏱️ 2-3 days

**Agent B Tasks**:
- B7: Log rotation ⏱️ 2 hours
- B8: Log analysis ⏱️ 3-4 hours
- B9: GeoIP blocking (optional) ⏱️ 2-3 hours

**Parallel Execution**: YES - No conflicts
**Estimated Completion**: End of Week 4

---

### Phase 4: Long-Term Priority (Months 2-3)

**Agent A Tasks**:
- A10: Security scanning ⏱️ 1 week
- A11: Docker Bench audit ⏱️ 2-3 days

**Agent B Tasks**:
- B10: ModSecurity WAF ⏱️ 2-3 weeks
- B11: Certificate pinning ⏱️ 2-3 days
- B12: Security monitoring ⏱️ 1 week

**Parallel Execution**: YES - No conflicts
**Estimated Completion**: End of Month 3

---

## Risk Management

### Risk 1: Agent A Breaks Nginx Proxy

**Scenario**: Agent A changes port bindings, Nginx can't connect

**Mitigation**:
1. Agent A tests localhost connectivity before notifying Agent B
2. Agent B has comprehensive test suite (Task B2)
3. Rollback plan documented in Agent A task file
4. Nginx config unchanged by Agent A

**Likelihood**: LOW (Nginx config not touched by Agent A)
**Impact**: MEDIUM (services temporarily unavailable)
**Recovery Time**: 5-10 minutes (rollback docker-compose.yml)

---

### Risk 2: Agent B Breaks WebSocket

**Scenario**: Agent B modifies Nginx config, breaks WebSocket upgrade

**Mitigation**:
1. WebSocket map already configured and working
2. Agent B explicitly tests WebSocket in Task B2
3. Rollback plan documented in Agent B task file
4. Docker containers unchanged by Agent B

**Likelihood**: LOW (current config already works)
**Impact**: MEDIUM (real-time features broken)
**Recovery Time**: 5-10 minutes (restore nginx.conf backup)

---

### Risk 3: Both Agents Apply Conflicting Changes

**Scenario**: Both agents modify the same file simultaneously

**Mitigation**:
1. **File ownership clearly defined** (no overlap)
2. Agent A ONLY touches: `/opt/archon/docker-compose.yml`
3. Agent B ONLY touches: `/etc/nginx/` files
4. No shared files exist

**Likelihood**: IMPOSSIBLE (different file sets)
**Impact**: NONE
**Recovery Time**: N/A

---

### Risk 4: Service Downtime During Changes

**Scenario**: Applying changes causes brief service interruption

**Mitigation**:
1. All changes use `docker compose up -d` (rolling restart)
2. Nginx uses `reload` not `restart` (zero downtime)
3. Changes applied during low-traffic hours
4. Health checks verify service recovery
5. Rollback plan always available

**Likelihood**: LOW (graceful reload/restart)
**Impact**: LOW (< 5 seconds downtime)
**Recovery Time**: Automatic (health checks + restart policies)

---

## Communication Protocol

### Agent A → Agent B Messages

**Message Format**:
```
[AGENT A] Task A4 Complete
Status: ✅ SUCCESS / ⚠️ PARTIAL / ❌ FAILED
Action: Bound services to 127.0.0.1
Affected Services:
  - supabase_kong_archon: 127.0.0.1:54321
  - supabase_db_archon: 127.0.0.1:54322
  - supabase_rest_archon: 127.0.0.1:54323
  - supabase_realtime_archon: 127.0.0.1:54324
  - ollama: 127.0.0.1:11434
Local Test: ✅ Passed (curl http://127.0.0.1:54321 → 200 OK)
Next: Agent B Task B2 - Verify Nginx proxies
```

---

### Agent B → Agent A Messages

**Message Format**:
```
[AGENT B] Task B2 Complete
Status: ✅ SUCCESS / ⚠️ PARTIAL / ❌ FAILED
Action: Verified Nginx proxies after localhost binding
Tests Performed:
  - Archon site: ✅ PASS (https://archon.nexorithm.io → 200)
  - Arcane site: ✅ PASS (https://arcane.nexorithm.io → 200)
  - WebSocket: ✅ PASS (101 Switching Protocols)
  - Security headers: ✅ PASS (all present)
Issues: None
Next: Agent A can proceed with A5 (resource limits)
```

---

### Error Communication

**If Issues Found**:
```
[AGENT B] Task B2 ⚠️ PARTIAL SUCCESS
Status: ⚠️ PARTIAL - Arcane WebSocket not working
Action: Verified Nginx proxies after localhost binding
Tests Performed:
  - Archon site: ✅ PASS
  - Arcane site: ✅ PASS (but WebSocket fails)
  - WebSocket: ❌ FAIL (Connection refused)
Issues Found:
  - Arcane WebSocket connection: ERR_CONNECTION_REFUSED
  - Browser console: "WebSocket connection to 'wss://arcane.nexorithm.io/ws' failed"
  - Nginx logs: "upstream prematurely closed connection"
Suspected Cause: Port 3552 not listening on 127.0.0.1
Requested Action: Agent A verify arcane container bound to 127.0.0.1:3552
Rollback: Not performed (awaiting Agent A investigation)
```

---

## Success Metrics

### Phase 1 Success Criteria (End of Day 1)

**Agent A**:
- [ ] supabase_vector_archon has no Docker socket access
- [ ] archon-server Docker socket justified or removed
- [ ] All Archon containers have restart policies

**Agent B**:
- [ ] Only TLSv1.2 and TLSv1.3 enabled
- [ ] Netzwaechter site has rate limiting
- [ ] Strong cipher suites configured

**Joint**:
- [ ] All sites still accessible and functional
- [ ] SSL Labs grade A or higher on all sites

---

### Phase 2 Success Criteria (End of Week 1)

**Agent A**:
- [ ] All services bound to 127.0.0.1 (not 0.0.0.0)
- [ ] Resource limits configured on all containers

**Agent B**:
- [ ] Nginx proxies verified working with localhost binding
- [ ] Advanced rate limiting configured
- [ ] HTTP/2 optimizations applied

**Joint**:
- [ ] External port scan shows only 22, 80, 443 open
- [ ] No services exposed to external network (except via proxy)
- [ ] WebSocket connections working

---

### Phase 3 Success Criteria (End of Week 4)

**Agent A**:
- [ ] Critical containers run as non-root
- [ ] Read-only filesystems where applicable
- [ ] Unnecessary capabilities dropped
- [ ] Health checks configured

**Agent B**:
- [ ] Log rotation configured
- [ ] Automated log analysis running
- [ ] GeoIP blocking (if needed) configured

**Joint**:
- [ ] Docker security score improved from 4.5/10 to 7.0/10+
- [ ] Nginx security grade A+ on all sites
- [ ] CIS Docker Benchmark compliance > 80%

---

### Phase 4 Success Criteria (End of Month 3)

**Agent A**:
- [ ] Weekly container vulnerability scans automated
- [ ] Monthly Docker Bench audits scheduled

**Agent B**:
- [ ] ModSecurity WAF configured (detection mode minimum)
- [ ] Certificate pinning/Expect-CT enabled
- [ ] Prometheus/Grafana monitoring configured

**Joint**:
- [ ] Overall security score improved from 6.2/10 to 8.5/10+
- [ ] All critical and high priority issues resolved
- [ ] Automated security monitoring in place
- [ ] Incident response procedures documented

---

## Agent Launch Commands

### Launch Agent A (Docker Security)

```bash
# Use Claude Code task agent
claude task "Execute security remediation tasks from Agent A task file.
Your role is Docker & Container Security Specialist.
Read and follow /Users/janschubert/tools/archon/.deployment/archon/AGENT_A_SECURITY_REMEDIATION.md
Start with immediate priority tasks (A1, A2, A3).
Update the task file with completion status as you progress.
Notify when Task A4 is complete so Agent B can verify.
Do NOT modify any Nginx configuration files."
```

**Or manually with specialized agent**:
```bash
# In current session
/task Execute Agent A security remediation tasks as Docker specialist
```

---

### Launch Agent B (Nginx Security)

```bash
# Use Claude Code task agent
claude task "Execute security remediation tasks from Agent B task file.
Your role is Nginx & Network Security Specialist.
Read and follow /Users/janschubert/tools/archon/.deployment/archon/AGENT_B_SECURITY_REMEDIATION.md
Start with immediate priority tasks (B1, B3, B4).
Update the task file with completion status as you progress.
Wait for Agent A to notify completion of Task A4 before starting B2.
Do NOT modify any docker-compose.yml files."
```

**Or manually with specialized agent**:
```bash
# In current session
/task Execute Agent B security remediation tasks as Nginx specialist
```

---

## Monitoring Agent Progress

### Check Agent A Progress

```bash
# Read Agent A task file for status updates
cat /Users/janschubert/tools/archon/.deployment/archon/AGENT_A_SECURITY_REMEDIATION.md | grep "Status:"

# Check Docker changes on server
ssh root@91.98.156.158 "docker ps --format '{{.Names}}\t{{.Status}}'"
ssh root@91.98.156.158 "docker inspect supabase_vector_archon | grep docker.sock"
```

---

### Check Agent B Progress

```bash
# Read Agent B task file for status updates
cat /Users/janschubert/tools/archon/.deployment/archon/AGENT_B_SECURITY_REMEDIATION.md | grep "Status:"

# Check Nginx configuration changes
ssh root@91.98.156.158 "grep 'ssl_protocols' /etc/nginx/nginx.conf"
ssh root@91.98.156.158 "nginx -t"

# Test SSL/TLS
nmap --script ssl-enum-ciphers -p 443 archon.nexorithm.io | grep TLSv1
```

---

## Rollback Plan

### Agent A Rollback

```bash
ssh root@91.98.156.158
cd /opt/archon

# List available backups
ls -lah docker-compose.yml.backup.*

# Rollback to specific backup
docker compose down
cp docker-compose.yml.backup.YYYYMMDD_HHMMSS docker-compose.yml
docker compose up -d

# Verify services
docker ps
curl -I https://archon.nexorithm.io
```

---

### Agent B Rollback

```bash
ssh root@91.98.156.158

# List available backups
ls -lah /etc/nginx/nginx.conf.backup.*
ls -lah /etc/nginx/sites-available/*.backup.*

# Rollback Nginx config
cp /etc/nginx/nginx.conf.backup.YYYYMMDD_HHMMSS /etc/nginx/nginx.conf

# Test and reload
nginx -t && systemctl reload nginx

# Verify services
curl -I https://archon.nexorithm.io
curl -I https://arcane.nexorithm.io
```

---

### Full System Rollback

**If both agents need to rollback**:

```bash
ssh root@91.98.156.158

# 1. Rollback Docker (Agent A)
cd /opt/archon
docker compose down
cp docker-compose.yml.backup.YYYYMMDD_HHMMSS docker-compose.yml
docker compose up -d

# 2. Rollback Nginx (Agent B)
cp /etc/nginx/nginx.conf.backup.YYYYMMDD_HHMMSS /etc/nginx/nginx.conf
nginx -t && systemctl reload nginx

# 3. Verify all services
docker ps
systemctl status nginx
curl -I https://archon.nexorithm.io
curl -I https://arcane.nexorithm.io
curl -I https://strawa.cockpit365.pro
```

---

## Final Deliverables

### Agent A Deliverables

1. **Updated docker-compose.yml** with:
   - No Docker socket on supabase_vector_archon
   - Localhost bindings (127.0.0.1) on all internal services
   - Restart policies on all services
   - Resource limits configured
   - Non-root users where possible

2. **Security Scanning Automation**:
   - `/usr/local/bin/weekly-container-scan.sh`
   - `/usr/local/bin/monthly-docker-audit.sh`
   - Cron jobs configured

3. **Documentation**:
   - Agent A task file with completion status
   - Docker socket access justifications
   - Container security improvements summary

---

### Agent B Deliverables

1. **Updated Nginx Configuration** with:
   - Only TLSv1.2 and TLSv1.3 enabled
   - Strong cipher suites
   - Security headers on all sites
   - Rate limiting on all endpoints
   - Log rotation configured

2. **Security Monitoring Scripts**:
   - `/usr/local/bin/daily-nginx-analysis.sh`
   - Automated log analysis
   - Security metrics collection

3. **Documentation**:
   - Agent B task file with completion status
   - Nginx security configuration summary
   - SSL/TLS test results

---

### Joint Deliverables

1. **Comprehensive Security Report**:
   - Before/after comparison
   - Security score improvement (6.2/10 → 8.5/10)
   - CIS Docker Benchmark compliance improvement
   - OWASP compliance improvement

2. **Incident Response Runbook**:
   - Common issues and solutions
   - Emergency rollback procedures
   - Contact information

3. **Maintenance Schedule**:
   - Daily: Automated log analysis
   - Weekly: Container vulnerability scans
   - Monthly: Docker Bench security audit
   - Quarterly: Full security review

---

## Conclusion

This plan enables two agents to work in parallel on security remediation with:

✅ **Zero File Conflicts**: Different file ownership
✅ **Clear Coordination**: Single coordination point (A4 → B2)
✅ **Independent Tasks**: Most tasks can run in parallel
✅ **Risk Mitigation**: Comprehensive rollback plans
✅ **Progress Tracking**: Status updates in task files
✅ **Success Metrics**: Clear completion criteria

**Estimated Timeline**:
- Phase 1 (Critical): 1 day
- Phase 2 (High): 1 week
- Phase 3 (Medium): 1 month
- Phase 4 (Long-term): 3 months

**Expected Outcome**: Security posture improved from 6.2/10 to 8.5/10+

---

**Plan Created**: 2025-10-15 18:15 UTC
**Ready to Execute**: YES
**Agents Ready**: Agent A & Agent B task files complete
