# WebServer
Home hosted web server to play around with web development (html, css, REST, home automation)

Setting up your Raspberry Pi 4 as a web server on your local network is a great project. Below are detailed instructions to get you started.

### **Step 1: Prepare Your Raspberry Pi**

1. **Install the Operating System:**
   - Download and install [Raspberry Pi OS](https://www.raspberrypi.com/software/) (Lite version recommended for a server) on your Raspberry Pi.
   - Use [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to flash the OS onto your microSD card.
   - Enable SSH for remote access by adding an empty file named `ssh` (no extension) in the boot partition of the microSD card.

2. **Boot Your Raspberry Pi:**
   - Insert the microSD card into your Raspberry Pi.
   - Connect the Raspberry Pi to your network using an Ethernet cable or Wi-Fi.
   - Power on the Raspberry Pi.

3. **Access Your Raspberry Pi via SSH:**
   - From a terminal on your PC, connect to your Raspberry Pi using SSH:
     ```bash
     ssh pi@raspberrypi.local
     ```
     - If that doesn't work, find the IP address of your Raspberry Pi using your router's admin interface or a network scanning tool like `nmap` and connect using:
     ```bash
     ssh pi@<Raspberry_Pi_IP_Address>
     ```

4. **Update and Upgrade the System:**
   - Once logged in, update your Raspberry Pi:
     ```bash
     sudo apt update
     sudo apt upgrade -y
     ```

### **Step 2: Install Web Server Software**

1. **Install Apache (Web Server):**
   - Apache is a popular web server software that you'll install on your Raspberry Pi.
   - Install Apache using the following command:
     ```bash
     sudo apt install apache2 -y
     ```
   - After installation, check if Apache is running:
     ```bash
     sudo systemctl status apache2
     ```
     - You should see something like `Active: active (running)`.

2. **Test Apache Installation:**
   - Open a web browser on your computer and enter the IP address of your Raspberry Pi.
   - You should see the Apache default page saying "Apache2 Debian Default Page."

3. **Install PHP (Optional - for dynamic content):**
   - If you plan to serve dynamic content (e.g., PHP scripts), install PHP:
     ```bash
     sudo apt install php libapache2-mod-php -y
     ```
   - Test PHP by creating a file called `info.php` in the web directory:
     ```bash
     sudo nano /var/www/html/info.php
     ```
   - Add the following content:
     ```php
     <?php
     phpinfo();
     ?>
     ```
   - Save and exit (`CTRL + X`, then `Y`, and `Enter`).
   - In your web browser, go to `http://<Raspberry_Pi_IP_Address>/info.php` to see the PHP info page.

4. **Install MySQL (Optional - for databases):**
   - If your web application requires a database, install MySQL:
     ```bash
     sudo apt install mysql-server -y
     ```
   - Secure your MySQL installation:
     ```bash
     sudo mysql_secure_installation
     ```
   - Follow the prompts to set a root password and remove insecure defaults.

5. **Install phpMyAdmin (Optional - for database management):**
   - Install phpMyAdmin to manage MySQL databases via a web interface:
     ```bash
     sudo apt install phpmyadmin -y
     ```
   - During installation, select Apache2 and choose "Yes" to configure the database.
   - Enable the phpMyAdmin configuration:
     ```bash
     sudo phpenmod mbstring
     sudo systemctl restart apache2
     ```
   - Access phpMyAdmin by navigating to `http://<Raspberry_Pi_IP_Address>/phpmyadmin` in your browser.

### **Step 3: Configure Your Web Server**

1. **Set Up a Static IP Address (Optional):**
   - To ensure your Raspberry Pi always has the same IP address on your network, set up a static IP.
   - Edit the `dhcpcd.conf` file:
     ```bash
     sudo nano /etc/dhcpcd.conf
     ```
   - Add the following lines at the end (adjust for your network):
     ```bash
     interface eth0
     static ip_address=192.168.1.100/24
     static routers=192.168.1.1
     static domain_name_servers=192.168.1.1
     ```
   - Save and exit, then reboot the Raspberry Pi:
     ```bash
     sudo reboot
     ```

2. **Set Up a Virtual Host (Optional - for multiple sites):**
   - If you want to host multiple websites on your Raspberry Pi, set up virtual hosts.
   - Create a directory for your new site:
     ```bash
     sudo mkdir /var/www/your_site
     sudo chown -R pi:pi /var/www/your_site
     ```
   - Copy the default Apache configuration file:
     ```bash
     sudo cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/your_site.conf
     ```
   - Edit the new configuration file:
     ```bash
     sudo nano /etc/apache2/sites-available/your_site.conf
     ```
   - Modify the `DocumentRoot` and `ServerName` to match your site:
     ```apache
     <VirtualHost *:80>
         ServerAdmin webmaster@localhost
         DocumentRoot /var/www/your_site
         ServerName your_site.local

         ErrorLog ${APACHE_LOG_DIR}/error.log
         CustomLog ${APACHE_LOG_DIR}/access.log combined
     </VirtualHost>
     ```
   - Enable the site and reload Apache:
     ```bash
     sudo a2ensite your_site.conf
     sudo systemctl reload apache2
     ```

3. **Enable HTTPS (Optional - for secure connections):**
   - Install `certbot` to enable HTTPS with a free SSL certificate from Let’s Encrypt:
     ```bash
     sudo apt install certbot python3-certbot-apache -y
     ```
   - Obtain and install the SSL certificate:
     ```bash
     sudo certbot --apache
     ```
   - Follow the prompts to set up HTTPS.

### **Step 4: Deploy Your Website**

1. **Upload Your Website Files:**
   - You can upload your website files to the `/var/www/html/` directory or to the custom directory you set up in the virtual host.
   - Use SCP (Secure Copy) from your computer to transfer files:
     ```bash
     scp -r /path/to/your/website/files pi@<Raspberry_Pi_IP_Address>:/var/www/html/
     ```

2. **Set Correct Permissions:**
   - Ensure the web server can access your files:
     ```bash
     sudo chown -R www-data:www-data /var/www/html/
     sudo chmod -R 755 /var/www/html/
     ```

3. **Access Your Website:**
   - Open a web browser and enter your Raspberry Pi's IP address (or domain name if you’ve set one up). You should see your website live!

### **Step 5: Maintain Your Web Server**

1. **Update Your System Regularly:**
   - Keep your Raspberry Pi secure and up-to-date:
     ```bash
     sudo apt update
     sudo apt upgrade -y
     ```

2. **Monitor Logs:**
   - Regularly check Apache logs for any issues:
     ```bash
     sudo tail -f /var/log/apache2/error.log
     ```

3. **Backup Your Website:**
   - Regularly back up your website files and database to avoid data loss.

---

By following these steps, you'll have a fully functional web server running on your Raspberry Pi 4. This setup is perfect for hosting personal projects, testing environments, or even a small home automation dashboard.
