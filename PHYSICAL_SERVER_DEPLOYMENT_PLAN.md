# Physical Server Deployment Plan for Iconic Design

Deploying a web application on a physical (bare-metal) server involves setting up the hardware, configuring the network, installing the operating system, and finally deploying the application stack. Here is a comprehensive step-by-step plan to achieve this.

## Phase 1: Hardware and Network Setup

### 1. Hardware Preparation
* **Server Assembly:** Ensure the physical server is assembled with all necessary components (CPU, RAM, Storage drives, NICs).
* **Power and Cooling:** Connect the server to a reliable power source (preferably with a UPS) and ensure adequate cooling in the server room/rack.
* **Network Connectivity:** Connect the server to the internet router or switch using an Ethernet cable.

### 2. Network Configuration (ISP level)
* **Static IP Address:** Request a **Static Public IP address** from the Internet Service Provider (ISP). This is crucial for hosting a website directly so the IP doesn't change.
* **Port Forwarding:** Configure the router to forward web traffic (Port 80 for HTTP, Port 443 for HTTPS) to the server's local IP address.
* **Firewall Configuration (Router):** Ensure the router's firewall allows incoming traffic on ports 80, 443, and 22 (SSH for remote management, consider restricting this to specific IPs).

### 2b. Alternative: What if the ISP doesn't provide a Static IP?
If a Static IP is not available, you have three great alternatives:
1. **Cloudflare Tunnels (Highly Recommended):** This is the most secure and modern method. You install a lightweight daemon (`cloudflared`) on the server that creates a secure outbound connection to Cloudflare. Cloudflare routes your domain's traffic through this tunnel to your server. 
   - **Pros:** **No port forwarding required**, hides your real home IP address from the internet, comes with free SSL, and bypasses ISP restrictions like CGNAT.
2. **Dynamic DNS (DDNS):** Services like No-IP or DuckDNS. You install a small script on your server that constantly checks your public IP. If the ISP changes your IP, the script automatically updates your domain's DNS records to point to the new IP.
   - **Cons:** You still need to port forward on your router. There can also be brief downtime (a few minutes) when your IP changes while the new DNS record propagates.
3. **VPS Reverse Proxy:** Rent a very cheap cloud VPS (e.g., $4/month on DigitalOcean or Linode) which *will* have a static IP. You connect your physical server to the VPS using a VPN (like WireGuard or Tailscale), and the VPS forwards all web traffic through the VPN to your physical server.

## Phase 2: Operating System Installation

### 1. Install Linux OS
* **Choose a Distribution:** Ubuntu Server LTS (Long Term Support) is highly recommended for its stability, extensive documentation, and community support.
* **Installation Media:** Create a bootable USB drive with the Ubuntu Server ISO.
* **Boot and Install:** Boot the server from the USB drive and follow the installation wizard.
    * Set up a strong administrator (root/sudo) password.
    * Configure the network interface to use a static internal IP address.
    * Install OpenSSH server during the setup for remote access.

### 2. Initial OS Security and Setup
* **Update System:** Run `sudo apt update && sudo apt upgrade -y` to get the latest security patches.
* **Set up a Firewall (UFW):**
  * `sudo ufw allow OpenSSH`
  * `sudo ufw allow 'Nginx Full'` (or Apache, allowing ports 80 and 443)
  * `sudo ufw enable`
* **Secure SSH:** Disable root login and password authentication; use SSH keys instead.

## Phase 3: Application Environment Setup

### 1. Install Dependencies
Install the required software stack. Assuming a Python-based stack (like Flask/Django) or Node.js based on previous files:
* **Python/Node.js:** Install the required runtime environment.
* **Database:** Install the database server (e.g., PostgreSQL, MySQL). Secure the database installation.
* **Web Server/Reverse Proxy:** Install Nginx or Apache.
* **Process Manager:** Install Gunicorn (for Python) or PM2 (for Node.js) to keep the application running continuously.

### 2. Clone and Configure the Application
* **Transfer Code:** Use `git` to clone the project repository onto the server (e.g., into `/var/www/iconic-design`).
* **Virtual Environment (if Python):** Set up a virtual environment and install dependencies from `requirements.txt`.
* **Environment Variables:** Create a `.env` file on the server with production credentials (database URLs, secret keys). **Never commit this file to Git.**

## Phase 4: Deployment and Service Configuration

### 1. Configure the Application Server
* Set up the process manager (like Gunicorn/Systemd or PM2) to run the application on a local port (e.g., `http://127.0.0.1:8000`).
* Ensure it is set to start automatically on system boot.

### 2. Configure the Reverse Proxy (Nginx)
* Create an Nginx server block configuration for the domain.
* Configure it to listen on port 80 and proxy incoming requests to the local application port (8000).
* Test the Nginx configuration (`sudo nginx -t`) and restart Nginx.

### 3. SSL/TLS Certificate (HTTPS)
* **Domain DNS:** Point your domain's A Record to the **Static Public IP address** obtained in Phase 1.
* **Install Certbot:** Use Let's Encrypt and Certbot to automatically fetch and configure free SSL certificates.
* Run `sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com`.

## Phase 5: Maintenance and Monitoring

* **Automated Backups:** Set up cron jobs to back up the database and application files regularly (ideally to an off-site location like AWS S3 or another server).
* **Log Rotation:** Ensure logs are rotated to prevent the disk from filling up.
* **Monitoring:** Install monitoring tools (like Prometheus, Grafana, or simple alerts like UptimeRobot) to track server health (CPU, RAM, Disk space) and website uptime.
* **UPS Monitoring:** If a UPS is used, configure tools (like `apcupsd`) to safely shut down the server in case of an extended power outage.

---
### Summary Checklist for the Client
- [ ] Buy physical server hardware.
- [ ] Contact ISP for a Static Public IP.
- [ ] Ensure router allows Port Forwarding.
- [ ] Provide an uninterrupted power supply (UPS).
