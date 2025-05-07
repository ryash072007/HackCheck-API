# ...existing code...

## API Documentation

For a complete list of all API endpoints, request/response formats, and error codes, see the [API Documentation](./api_documentation.md).

# ...existing code...

## PART 1: Open the Firewall (Windows CMD)

1.  **Open Command Prompt as Administrator**
    
    -   Click **Start**, type `cmd`, right-click **Command Prompt**, choose **Run as administrator**.
        
2.  **Add Firewall Rule**  
    Copy-paste this exact line and press **Enter** (it opens port 8000 for HackCheck to wsl and local network):
    
    ```cmd
    netsh advfirewall firewall add rule name="HackCheck Inbound" dir=in action=allow protocol=TCP localport=8000
    
    ```
    
    -   ✅ You only need to do this **once**.
        

----------

## PART 2: Install WSL 2 & Ubuntu (Windows PowerShell or command prompt)

1.  **Open PowerShell as Administrator**
    
    -   Click **Start**, type `PowerShell`, right-click **Windows PowerShell**, choose **Run as administrator**.
        
2.  **Install Ubuntu 24.04**  
    Copy-paste and press **Enter**:
    
    ```powershell
    wsl --install "Ubuntu-24.04"
    
    ```
    
3.  **Launch Ubuntu** (still in PowerShell)
    
    ```powershell
    wsl -d Ubuntu-24.04
    
    ```
    
4.  **Set UNIX Username & Password**  
    When Ubuntu first starts, it asks for credentials. Type:
    
    -   **Username:** `postgres`
        
    -   **Password:** `12345678`
        
    
    > We pick `postgres` so PostgreSQL’s peer authentication just works without extra setup.
    

----------

> ✅ **All Windows bits are done.** Now stay in the **Ubuntu** window to finish.

----------

## PART 3: Ubuntu (Linux) Setup

> **Everything below happens inside the Ubuntu shell.** Do **not** switch back to PowerShell or CMD.

----------

### 1. Update & Install Core Software

Copy-paste each block one group at a time:

```bash
# 1A) Update package list
sudo apt update

# 1B) Upgrade installed packages
sudo apt upgrade -y

# 1C) Install PostgreSQL & Python venv support
sudo apt install -y postgresql postgresql-contrib python3-venv

```

----------

### 2. Create Python Virtual Environment & Database

```bash
# 2A) Go to your home folder
cd ~

# 2B) Make a Python “venv” (isolated environment)
python3 -m venv hackcheck-venv

# 2C) Activate it (you’ll see (hackcheck-venv) in your prompt)
source hackcheck-venv/bin/activate

# 2D) Create the HackCheck database as the postgres user
psql -c "CREATE DATABASE hackcheck;"

```
   

----------

### 3. Clone & Install HackCheck API

```bash
# 3A) Clone the repository’s WSL branch
git clone https://github.com/ryash072007/HackCheck-API.git -b wsl
cd HackCheck-API

# 3B) Install Python dependencies
pip install -r requirements.txt

# 3C) Apply database migrations (creates tables, etc.)
python manage.py migrate

```

----------

### 4. Create the Admin Account

You’ll run **two** commands. **Each** must be pasted **as one single line**.

1.  **Create superuser `admin`:**
    
    ```bash
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', '', '12345678')" | python manage.py shell
    
    ```
    
2.  **Grant extra admin flag**:
    
    ```bash
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); u = User.objects.get(username='admin'); u.is_admin = True; u.save()" | python manage.py shell
    
    ```
    

-   **Username:** `admin`
    
-   **Password:** `12345678`
    

> If you accidentally press Enter too early, press the **Up-arrow** key to recall the last command, then paste the full line again.

----------

Within `HackCheckAPI` folder, find the `settings.py` file and change `IP` to the windows host-machine IP found using the method given below in final check.

----------

### 5. Launch HackCheck

With your **venv still activated and in the HackCheck-API folder**, start the server:

```bash
gunicorn --bind 0.0.0.0:8000 --workers 4 --threads 2 HackCheckAPI.wsgi:application

```

-   `--workers 4`: number of parallel workers. If you have a good PC, use more workers.
    
-   `--threads 2`: number of threads per worker. If you have a faster cpu, you can increase it.
    

When you see lines like `Booting worker with pid…`, your API backend server is live.

#### Restarting the Server

If you need to restart the server later, follow these steps:

```bash
# 1) Go to your home folder
cd ~

# 2) Reactivate the virtual environment
source hackcheck-venv/bin/activate

# 3) Navigate to the HackCheck-API folder
cd HackCheck-API

# 4) Start the server | modify workers and threads as needed
gunicorn --bind 0.0.0.0:8000 --workers 8 --threads 3 HackCheckAPI.wsgi:application
```

----------

## ✅ Final Check

1.  **Find your PC’s local IP** (in PowerShell or CMD):
    
    ```powershell
    ipconfig
    
    ```
    
2.  **Open a browser** on **any** device (same network) and visit:
    
    ```
    http://<Your-PC-IP>:8000/
    
    ```

### Troubleshooting

If you cannot access the website from the host machine IP, follow these steps:

1. **Open WSL Settings**  
   - Click **Start**, type `WSL settings`, and open the **Windows Subsystem for Linux settings**.

2. **Change Networking Mode**  
   - Go to the **Networking** section.
   - Change the **Networking mode** to **Mirrored**.

3. **Enable Host Address Loopback**  
   - Ensure the **Enable host address loopback** option is checked.

4. **Restart WSL**  
   - Open PowerShell as Administrator and run:
     ```powershell
     wsl --shutdown
     ```
   - Then restart WSL by launching your Ubuntu instance again.

5. **Retry Accessing the Website**  
   - Open the browser and try visiting `http://<Your-PC-IP>:8000/` again.
