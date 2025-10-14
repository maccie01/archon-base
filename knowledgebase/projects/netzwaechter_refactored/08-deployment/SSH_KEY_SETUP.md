# SSH Key Setup for Netzwächter Deployment

Created: 2025-10-14

## SSH Key Generated Successfully ✅

### Key Information

**Key Type**: ED25519 (most secure, modern)
**Key Name**: `netzwaechter_deployment`
**Created**: 2025-10-14
**Purpose**: Production server deployment and management

### Key Locations

**Private Key** (KEEP SECRET - Never share):
```
/Users/janschubert/.ssh/netzwaechter_deployment
```
- Permissions: 600 (owner read/write only) ✅
- Status: Secured

**Public Key** (Safe to copy to server):
```
/Users/janschubert/.ssh/netzwaechter_deployment.pub
```
- Permissions: 644 (owner read/write, others read) ✅

---

## Your Public Key

Copy this ENTIRE line to your Hetzner server:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICdyyWO2xYQbC2Gn4efgFk8l60LACLpuY9Lg3Wpb3phJ netzwaechter-deployment-20251014
```

**Fingerprint**: `SHA256:7tVzuYLSTnjuQuxsNL2dw5QqNjBAsNMVaZJvPZmAm0w`

---

## Next Steps: Add Key to Server

### Option 1: Using ssh-copy-id (Easiest)

If you have password access to your server:

```bash
ssh-copy-id -i ~/.ssh/netzwaechter_deployment.pub root@YOUR_SERVER_IP
```

This will automatically:
- Create `~/.ssh/` directory on server if needed
- Add the public key to `~/.ssh/authorized_keys`
- Set correct permissions

### Option 2: Manual Copy (If password auth disabled)

1. **Login to Hetzner Cloud Console**
   - Go to https://console.hetzner.cloud/
   - Select your project
   - Click on your server
   - Click "Console" (browser-based terminal)

2. **Add the public key**:
```bash
# Login as root via Hetzner console, then:

# Create .ssh directory if it doesn't exist
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Add the public key
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICdyyWO2xYQbC2Gn4efgFk8l60LACLpuY9Lg3Wpb3phJ netzwaechter-deployment-20251014" >> ~/.ssh/authorized_keys

# Set correct permissions
chmod 600 ~/.ssh/authorized_keys

# Verify it was added
cat ~/.ssh/authorized_keys
```

### Option 3: During Server Creation

When creating a new Hetzner server:
1. Go to "Add SSH Key"
2. Paste the public key (the line above)
3. Name it: "netzwaechter-deployment"
4. Hetzner will automatically add it to the server

---

## Test SSH Connection

After adding the key to your server, test the connection:

```bash
# Replace YOUR_SERVER_IP with actual IP
ssh -i ~/.ssh/netzwaechter_deployment root@YOUR_SERVER_IP
```

**Expected output**:
- First time: "The authenticity of host... Are you sure?" → Type `yes`
- Should login without password
- You'll see the Ubuntu/server welcome message

**If it works**: ✅ You're connected!

**If it fails**: See troubleshooting below

---

## Configure SSH Config (Optional but Recommended)

Make connecting easier by adding to `~/.ssh/config`:

```bash
# Add this to ~/.ssh/config (create if doesn't exist)
cat >> ~/.ssh/config << 'EOF'

# Netzwächter Production Server
Host netzwaechter-prod
    HostName YOUR_SERVER_IP
    User root
    IdentityFile ~/.ssh/netzwaechter_deployment
    Port 22
    ServerAliveInterval 60
    ServerAliveCountMax 3
EOF

# Set proper permissions
chmod 600 ~/.ssh/config
```

**Then you can connect with**:
```bash
ssh netzwaechter-prod
```

Much easier than typing the full command!

---

## Security Best Practices ✅

### What We Did Right

1. ✅ **ED25519 Algorithm** - Most secure, modern algorithm
2. ✅ **Unique Key** - Dedicated key for this deployment only
3. ✅ **Proper Permissions** - Private key: 600, Public key: 644
4. ✅ **Descriptive Comment** - Key labeled with purpose and date

### Next: Server Hardening

Once connected, we'll:
1. **Disable password authentication** - SSH keys only
2. **Setup firewall** (ufw) - Only ports 22, 80, 443
3. **Install fail2ban** - Block brute force attempts
4. **Configure automatic updates** - Security patches

---

## Troubleshooting

### Problem: Permission denied (publickey)

**Possible causes**:
1. Public key not added to server
2. Wrong permissions on server's `~/.ssh/` or `authorized_keys`
3. SELinux blocking (rare on Ubuntu)

**Solution**:
```bash
# On server (via Hetzner console):
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
cat ~/.ssh/authorized_keys  # Verify key is there
```

### Problem: Connection timeout

**Possible causes**:
1. Wrong server IP
2. Firewall blocking port 22
3. Server is down

**Solution**:
```bash
# Check if server is reachable
ping YOUR_SERVER_IP

# Check if SSH port is open
nc -zv YOUR_SERVER_IP 22

# Or use telnet
telnet YOUR_SERVER_IP 22
```

### Problem: Host key verification failed

**Cause**: Server's SSH key changed (reinstall, snapshot restore)

**Solution**:
```bash
# Remove old host key
ssh-keygen -R YOUR_SERVER_IP

# Try connecting again
ssh -i ~/.ssh/netzwaechter_deployment root@YOUR_SERVER_IP
```

### Problem: Too many authentication failures

**Cause**: SSH trying all keys in ~/.ssh/ before yours

**Solution**:
```bash
# Use -o option to try only this key
ssh -o IdentitiesOnly=yes -i ~/.ssh/netzwaechter_deployment root@YOUR_SERVER_IP
```

---

## Key Management

### Backup Your Private Key

**Important**: This private key is the ONLY way to access the server with this key.

**Backup location suggestions**:
1. ✅ **Encrypted USB drive** - Physical backup
2. ✅ **Password manager** - 1Password, Bitwarden (secure notes)
3. ✅ **Encrypted cloud storage** - iCloud with FileVault, Dropbox (encrypted)
4. ❌ **Never** - Plain text in Dropbox/Google Drive
5. ❌ **Never** - Email to yourself
6. ❌ **Never** - Git repository

**How to backup**:
```bash
# Copy to encrypted USB (mounted at /Volumes/Backup)
cp ~/.ssh/netzwaechter_deployment /Volumes/Backup/ssh-keys/netzwaechter_deployment_$(date +%Y%m%d)

# Or create encrypted archive
tar -czf - ~/.ssh/netzwaechter_deployment | \
  openssl enc -aes-256-cbc -pbkdf2 -out ~/Documents/netzwaechter_key_backup.tar.gz.enc
```

### Revoke Key (If Compromised)

If you suspect the private key is compromised:

```bash
# 1. Login to server (via Hetzner console or different key)
ssh root@YOUR_SERVER_IP

# 2. Remove the compromised key from authorized_keys
nano ~/.ssh/authorized_keys
# Delete the line with: netzwaechter-deployment-20251014

# 3. Generate new key
ssh-keygen -t ed25519 -C "netzwaechter-deployment-new" -f ~/.ssh/netzwaechter_deployment_new

# 4. Add new key to server
ssh-copy-id -i ~/.ssh/netzwaechter_deployment_new.pub root@YOUR_SERVER_IP
```

### Multiple Team Members

If other people need access:

```bash
# Each person generates their OWN key:
ssh-keygen -t ed25519 -C "their-name-netzwaechter"

# They send you their PUBLIC key (.pub file)
# You add it to the server:
cat their_key.pub >> ~/.ssh/authorized_keys
```

**Never share private keys between people!**

---

## What Claude Needs

### For Initial Setup (Now)

Please provide:
1. ✅ Server IP address: `___________________`
2. ✅ Test SSH connection works (yes/no): `___________________`
3. ✅ Domain name (if you have one): `___________________`

### For Deployment (Once SSH Works)

I will need SSH access to:
1. Install dependencies (Node.js, PostgreSQL, Nginx)
2. Configure security (firewall, fail2ban)
3. Deploy application
4. Setup SSL/TLS certificates
5. Configure monitoring

**How to give me access**:

**Option A** - Let me SSH directly:
```bash
# You give me permission to use this command:
ssh -i ~/.ssh/netzwaechter_deployment root@YOUR_SERVER_IP
```

**Option B** - You execute commands I provide:
```bash
# I provide commands like this:
apt update && apt upgrade -y

# You SSH in and run them:
ssh netzwaechter-prod
root@server:~# apt update && apt upgrade -y
```

---

## SSH Key Details (Technical)

```
Algorithm: ED25519
Key Size: 256 bits
Security: Equivalent to 3072-bit RSA
Created: 2025-10-14
Comment: netzwaechter-deployment-20251014

Public Key Format: OpenSSH
Private Key Format: OpenSSH (RFC4716)

Fingerprint (SHA256):
7tVzuYLSTnjuQuxsNL2dw5QqNjBAsNMVaZJvPZmAm0w

Randomart:
+--[ED25519 256]--+
|  .. ooo         |
|   oE.+          |
|  o+.* o o       |
|   .= o =        |
|     o .So   .   |
|      o.=...o  . |
|       Boo+Bo.o  |
|       .X== *o . |
|       o.B+  o.  |
+----[SHA256]-----+
```

---

## Quick Reference

### Connect to Server
```bash
ssh -i ~/.ssh/netzwaechter_deployment root@YOUR_SERVER_IP
# Or (if SSH config setup):
ssh netzwaechter-prod
```

### Copy File to Server
```bash
scp -i ~/.ssh/netzwaechter_deployment local_file.txt root@YOUR_SERVER_IP:/remote/path/
```

### Copy File from Server
```bash
scp -i ~/.ssh/netzwaechter_deployment root@YOUR_SERVER_IP:/remote/file.txt ./local_path/
```

### Run Single Command
```bash
ssh -i ~/.ssh/netzwaechter_deployment root@YOUR_SERVER_IP "command_here"
```

### SSH with Verbose Output (Debugging)
```bash
ssh -vvv -i ~/.ssh/netzwaechter_deployment root@YOUR_SERVER_IP
```

---

## Status Checklist

- [x] SSH key pair generated
- [x] Private key secured (permissions: 600)
- [x] Public key readable (permissions: 644)
- [ ] Public key added to server
- [ ] SSH connection tested successfully
- [ ] SSH config file updated (optional)
- [ ] Private key backed up securely
- [ ] Ready for server setup

**Next Step**: Add public key to your Hetzner server and test connection!

---

**Created**: 2025-10-14
**Key Fingerprint**: SHA256:7tVzuYLSTnjuQuxsNL2dw5QqNjBAsNMVaZJvPZmAm0w
**Status**: Ready for server deployment
