"""
  ('-.      .-')    ('-. .-.             
  ( OO ).-. ( OO ). ( OO )  /             
  / . --. /(_)---\_),--. ,--. ,--. ,--.   
  | \-.  \ /    _ | |  | |  | |  | |  |   
.-'-'  |  |\  :` `. |   .|  | |  | | .-') 
 \| |_.'  | '..`''.)|       | |  |_|( OO )
  |  .-.  |.-._)   \|  .-.  | |  | | `-' /
  |  | |  |\       /|  | |  |('  '-'(_.-' 
  `--' `--' `-----' `--' `--'  `-----'    
                                                                                                  
    Auto Task Tool For Paws -Asʜᴜ || ☠️ xᴅ
    Author  : Asʜᴜ || ☠️ xᴅ
    Get Updates: https://telegram.dog/lootersera_th    
"""

import os
import requests
import time
import json
import re
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from colorama import init, Fore, Back, Style
import logging
from logging.handlers import RotatingFileHandler
from eth_account import Account
from eth_keys import keys
from fake_useragent import UserAgent
from requests.exceptions import RequestException, ProxyError, Timeout
from urllib3.exceptions import InsecureRequestWarning
import socks
import socket
from typing import Dict, List, Optional, Tuple
import backoff
import concurrent.futures
from threading import Lock

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Initialize colorama for Windows support
init()

# Load environment variables
load_dotenv()

# AntiCaptcha API Key and Faucet URL
ANTICAPTCHA_API_KEY = os.getenv("ANTICAPTCHA_API_KEY")
FAUCET_URL = os.getenv("FAUCET_URL")
HCAPTCHA_SITE_KEY = "914e63b4-ac20-4c24-bc92-cdb6950ccfde"

# File to store claim history
CLAIM_HISTORY_FILE = "data/claim_history.json"
LOG_FILE = "logs/faucet.log"
WALLETS_FILE = "data/wallets.json"
PROXY_FILE = "data/proxies.txt"

# Add new constants at the top with other constants
SUCCESSFUL_CLAIMS_FILE = "data/successful_claims.json"
UNSUCCESSFUL_CLAIMS_FILE = "data/unsuccessful_claims.json"

# Setup logging
def setup_logging():
    logger = logging.getLogger('faucet')
    logger.setLevel(logging.INFO)
    
    # Create formatters
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logging()

def print_status(message, status="info"):
    """Print colored status messages to console"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    if status == "success":
        print(f"{Fore.GREEN}[{timestamp}] ✓ {message}{Style.RESET_ALL}")
    elif status == "error":
        print(f"{Fore.RED}[{timestamp}] ✗ {message}{Style.RESET_ALL}")
    elif status == "warning":
        print(f"{Fore.YELLOW}[{timestamp}] ⚠ {message}{Style.RESET_ALL}")
    elif status == "info":
        print(f"{Fore.CYAN}[{timestamp}] ℹ {message}{Style.RESET_ALL}")
    elif status == "progress":
        print(f"{Fore.BLUE}[{timestamp}] ⟳ {message}{Style.RESET_ALL}")

# Anti-bot settings
MIN_DELAY = 5  # Minimum delay between requests
MAX_DELAY = 15  # Maximum delay between requests
MAX_RETRIES = 3  # Maximum number of retries for failed requests
PROXY_TIMEOUT = 10  # Proxy timeout in seconds
MAX_CONCURRENT_REQUESTS = 1  # Maximum number of concurrent requests
REQUEST_TIMEOUT = 30  # Request timeout in seconds

# User agent rotation
ua = UserAgent()

class ProxyManager:
    def __init__(self):
        self.proxies: List[Dict] = []
        self.current_index = 0
        self.failed_proxies: Dict[str, int] = {}  # Track failed attempts per proxy
        self.proxy_health: Dict[str, float] = {}  # Track proxy health scores
        self.last_used: Dict[str, datetime] = {}  # Track last used time per proxy

    def load_proxies(self, file_path: str = PROXY_FILE) -> bool:
        """Load and validate proxies from file"""
        try:
            with open(file_path, "r") as file:
                proxy_lines = file.read().splitlines()
            
            valid_proxies = []
            for line in proxy_lines:
                if line.strip() and not line.startswith('#'):
                    proxy = self.parse_proxy(line.strip())
                    if proxy:
                        valid_proxies.append(proxy)
                        self.proxy_health[proxy['url']] = 1.0  # Initialize health score
            
            self.proxies = valid_proxies
            print_status(f"Loaded {len(valid_proxies)} valid proxies", "success")
            return True
        except Exception as e:
            print_status(f"Error loading proxies: {e}", "error")
            return False

    def parse_proxy(self, proxy_str: str) -> Optional[Dict]:
        """Parse proxy string into structured format"""
        try:
            if proxy_str.startswith(('http://', 'https://', 'socks5://')):
                # Handle URL format: http://username:password@host:port
                protocol = proxy_str.split('://')[0]
                rest = proxy_str.split('://')[1]
                if '@' in rest:
                    auth, host_port = rest.split('@')
                    username, password = auth.split(':')
                    host, port = host_port.split(':')
                else:
                    host, port = rest.split(':')
                    username = password = None
            else:
                # Handle simple format: host:port or host:port:username:password
                parts = proxy_str.split(':')
                if len(parts) == 2:
                    host, port = parts
                    protocol = 'http'
                    username = password = None
                elif len(parts) == 4:
                    host, port, username, password = parts
                    protocol = 'http'
                else:
                    return None

            proxy_dict = {
                'protocol': protocol,
                'host': host,
                'port': port,
                'username': username,
                'password': password,
                'url': f"{protocol}://{username}:{password}@{host}:{port}" if username and password else f"{protocol}://{host}:{port}"
            }
            return proxy_dict
        except Exception as e:
            print_status(f"Error parsing proxy {proxy_str}: {e}", "error")
            return None

    def get_next_proxy(self) -> Optional[Dict]:
        """Get next available proxy with health check"""
        if not self.proxies:
            return None

        # Sort proxies by health score and last used time
        available_proxies = [
            p for p in self.proxies 
            if self.proxy_health.get(p['url'], 1.0) > 0.5  # Only use healthy proxies
            and (p['url'] not in self.last_used or 
                 datetime.now() - self.last_used[p['url']] > timedelta(minutes=5))
        ]

        if not available_proxies:
            # Reset health scores if all proxies are unhealthy
            self.proxy_health = {p['url']: 1.0 for p in self.proxies}
            available_proxies = self.proxies

        # Select proxy with highest health score
        proxy = max(available_proxies, key=lambda p: self.proxy_health.get(p['url'], 1.0))
        self.last_used[proxy['url']] = datetime.now()
        return proxy

    def mark_proxy_failed(self, proxy_url: str):
        """Mark proxy as failed and adjust health score"""
        self.failed_proxies[proxy_url] = self.failed_proxies.get(proxy_url, 0) + 1
        self.proxy_health[proxy_url] = max(0.0, self.proxy_health.get(proxy_url, 1.0) - 0.2)

    def mark_proxy_success(self, proxy_url: str):
        """Mark proxy as successful and improve health score"""
        self.proxy_health[proxy_url] = min(1.0, self.proxy_health.get(proxy_url, 1.0) + 0.1)

    def validate_proxy(self, proxy: Dict) -> bool:
        """Validate proxy is working"""
        try:
            proxies = {
                'http': proxy['url'],
                'https': proxy['url']
            }
            response = requests.get(
                'https://api.ipify.org?format=json',
                proxies=proxies,
                timeout=PROXY_TIMEOUT,
                verify=False
            )
            return response.status_code == 200
        except Exception as e:
            print_status(f"Proxy validation failed for {proxy['url']}: {e}", "error")
            return False

class AntiBotProtection:
    def __init__(self):
        self.last_request_time = datetime.now()
        self.request_count = 0
        self.ua = UserAgent()

    def get_random_delay(self) -> float:
        """Get random delay between requests"""
        return random.uniform(MIN_DELAY, MAX_DELAY)

    def get_random_user_agent(self) -> str:
        """Get random user agent"""
        return self.ua.random

    def wait_if_needed(self):
        """Wait if too many requests in short time"""
        now = datetime.now()
        if (now - self.last_request_time).total_seconds() < MIN_DELAY:
            time.sleep(self.get_random_delay())
        self.last_request_time = now

    def should_continue(self) -> bool:
        """Check if we should continue making requests"""
        return self.request_count < MAX_CONCURRENT_REQUESTS

# Initialize managers
proxy_manager = ProxyManager()
anti_bot = AntiBotProtection()

@backoff.on_exception(
    backoff.expo,
    (RequestException, ProxyError, Timeout),
    max_tries=MAX_RETRIES
)
def make_request(method: str, url: str, **kwargs) -> requests.Response:
    """Make HTTP request with anti-bot protection and proxy support"""
    anti_bot.wait_if_needed()
    
    proxy = proxy_manager.get_next_proxy()
    if proxy:
        kwargs['proxies'] = {
            'http': proxy['url'],
            'https': proxy['url']
        }
    
    kwargs['headers'] = kwargs.get('headers', {})
    kwargs['headers']['User-Agent'] = anti_bot.get_random_user_agent()
    kwargs['timeout'] = REQUEST_TIMEOUT
    kwargs['verify'] = False  # Disable SSL verification for proxies
    
    try:
        response = requests.request(method, url, **kwargs)
        if proxy:
            proxy_manager.mark_proxy_success(proxy['url'])
        return response
    except Exception as e:
        if proxy:
            proxy_manager.mark_proxy_failed(proxy['url'])
        raise

def solve_captcha(site_key: str, page_url: str) -> Optional[str]:
    """Solve CAPTCHA with improved error handling and proxy support"""
    print_status("Solving CAPTCHA...", "progress")
    
    # Step 1: Create task
    task_data = {
        "clientKey": ANTICAPTCHA_API_KEY,
        "task": {
            "type": "HCaptchaTaskProxyless",
            "websiteURL": page_url,
            "websiteKey": site_key,
            "userAgent": anti_bot.get_random_user_agent()
        }
    }
    
    try:
        response = make_request(
            "POST",
            "http://api.anti-captcha.com/createTask",
            json=task_data,
            headers={"Content-Type": "application/json"}
        )
        response_data = response.json()
        
        if response_data.get("errorId") == 0:
            task_id = response_data["taskId"]
            print_status(f"Created AntiCaptcha task with ID: {task_id}", "success")
        else:
            print_status(f"Error creating AntiCaptcha task: {response_data}", "error")
            return None

        # Step 2: Get solution
        max_attempts = 30
        attempts = 0
        
        while attempts < max_attempts:
            result_data = make_request(
                "POST",
                "http://api.anti-captcha.com/getTaskResult",
                json={
                    "clientKey": ANTICAPTCHA_API_KEY,
                    "taskId": task_id
                },
                headers={"Content-Type": "application/json"}
            ).json()
            
            if result_data.get("errorId") == 0:
                if result_data["status"] == "ready":
                    print_status("Successfully solved CAPTCHA", "success")
                    return result_data["solution"]["gRecaptchaResponse"]
                elif result_data["status"] == "processing":
                    print_status(f"CAPTCHA still processing... (attempt {attempts + 1}/{max_attempts})", "progress")
            
            attempts += 1
            time.sleep(5)
        
        print_status("Timed out waiting for CAPTCHA solution", "error")
        return None
        
    except Exception as e:
        print_status(f"Error solving CAPTCHA: {e}", "error")
        return None

def get_ip_info(ip_address: str) -> Dict:
    """Get IP geolocation information with multiple fallback services"""
    services = [
        {
            'url': f'http://ip-api.com/json/{ip_address}',
            'timeout': 5,
            'parser': lambda data: {
                'country': data.get('country', 'Unknown'),
                'city': data.get('city', 'Unknown'),
                'isp': data.get('isp', 'Unknown')
            }
        },
        {
            'url': f'https://ipapi.co/{ip_address}/json/',
            'timeout': 5,
            'parser': lambda data: {
                'country': data.get('country_name', 'Unknown'),
                'city': data.get('city', 'Unknown'),
                'isp': data.get('org', 'Unknown')
            }
        },
        {
            'url': f'https://ipwhois.app/json/{ip_address}',
            'timeout': 5,
            'parser': lambda data: {
                'country': data.get('country', 'Unknown'),
                'city': data.get('city', 'Unknown'),
                'isp': data.get('connection', {}).get('isp', 'Unknown')
            }
        }
    ]

    for service in services:
        try:
            response = requests.get(service['url'], timeout=service['timeout'])
            if response.status_code == 200:
                data = response.json()
                return service['parser'](data)
        except (requests.RequestException, json.JSONDecodeError) as e:
            print_status(f"Error with {service['url']}: {str(e)}", "warning")
            continue

    # If all services fail, return default values
    return {'country': 'Unknown', 'city': 'Unknown', 'isp': 'Unknown'}

def get_current_ip(proxy: Optional[Dict] = None) -> Tuple[str, Dict]:
    """Get current IP address and geolocation info"""
    try:
        # Try multiple IP detection services with proxy rotation
        ip_services = [
            'https://api.ipify.org?format=json',
            'https://api.myip.com',
            'https://api.ip.sb/ip'
        ]
        
        used_proxies = set()
        max_proxy_attempts = 3
        
        for _ in range(max_proxy_attempts):
            # Get a new proxy if needed
            if not proxy or proxy['url'] in used_proxies:
                proxy = proxy_manager.get_next_proxy()
                if not proxy or proxy['url'] in used_proxies:
                    continue
                used_proxies.add(proxy['url'])
            
            proxies = {
                'http': proxy['url'],
                'https': proxy['url']
            }
            
            # Try each IP service with current proxy
            for service in ip_services:
                try:
                    response = requests.get(service, proxies=proxies, timeout=5, verify=False)
                    if response.status_code == 200:
                        if service.endswith('ip.sb/ip'):
                            ip_address = response.text.strip()
                        else:
                            ip_address = response.json().get('ip')
                        if ip_address and ip_address != "unknown":
                            ip_info = get_ip_info(ip_address)
                            print_status(f"Using IP: {ip_address} ({ip_info['country']}, {ip_info['city']})", "info")
                            return ip_address, ip_info
                except Exception as e:
                    print_status(f"Error with service {service}: {str(e)}", "warning")
                    continue
            
            # If we get here, all services failed with current proxy
            proxy = None  # Force getting a new proxy on next iteration
        
        print_status("Failed to get valid IP after all proxy attempts", "error")
        return "unknown", {'country': 'Unknown', 'city': 'Unknown', 'isp': 'Unknown'}
            
    except Exception as e:
        print_status(f"Error getting current IP: {str(e)}", "error")
        return "unknown", {'country': 'Unknown', 'city': 'Unknown', 'isp': 'Unknown'}

def load_successful_claims() -> Dict:
    """Load successful claims from file"""
    try:
        with open(SUCCESSFUL_CLAIMS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"claims": []}

def load_unsuccessful_claims() -> Dict:
    """Load unsuccessful claims from file"""
    try:
        with open(UNSUCCESSFUL_CLAIMS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"claims": []}

def save_successful_claim(wallet_address: str, ip_address: str, tx_hash: str, private_key: str):
    """Save successful claim to file with private key"""
    claims = load_successful_claims()
    claims["claims"].append({
        "wallet_address": wallet_address,
        "ip_address": ip_address,
        "tx_hash": tx_hash,
        "private_key": private_key,
        "timestamp": datetime.now().isoformat()
    })
    with open(SUCCESSFUL_CLAIMS_FILE, "w") as file:
        json.dump(claims, file, indent=2)

def save_unsuccessful_claim(wallet_address: str, ip_address: str, reason: str, private_key: str):
    """Save unsuccessful claim to file with private key"""
    claims = load_unsuccessful_claims()
    claims["claims"].append({
        "wallet_address": wallet_address,
        "ip_address": ip_address,
        "reason": reason,
        "private_key": private_key,
        "timestamp": datetime.now().isoformat()
    })
    with open(UNSUCCESSFUL_CLAIMS_FILE, "w") as file:
        json.dump(claims, file, indent=2)

def process_wallet(wallet: Dict, history: Dict, current_time: datetime) -> bool:
    """Process a single wallet for faucet claiming"""
    wallet_address = wallet["address"]
    private_key = wallet["private_key"]
    
    # Skip if wallet has claimed in last 24 hours
    if wallet_address in history["wallet_claims"]:
        last_claim_time = datetime.fromisoformat(history["wallet_claims"][wallet_address])
        if current_time - last_claim_time < timedelta(hours=24):
            print_status(f"Skipping wallet {wallet_address} - already claimed in last 24 hours", "warning")
            save_unsuccessful_claim(wallet_address, "N/A", "Wallet already claimed in last 24 hours", private_key)
            return False
    
    print_status(f"\nProcessing wallet: {wallet_address}", "info")
    
    max_ip_attempts = 3
    ip_attempts = 0
    used_ips = set()
    
    while ip_attempts < max_ip_attempts:
        # Get current IP and check eligibility
        ip_address, ip_info = get_current_ip()
        
        # Skip if we've already tried this IP
        if ip_address in used_ips:
            print_status(f"IP {ip_address} already tried, getting new IP...", "info")
            continue
            
        used_ips.add(ip_address)
        
        if not is_eligible_to_claim(ip_address, wallet_address):
            print_status(f"IP {ip_address} ({ip_info['country']}) has already claimed in the last 24 hours", "warning")
            if ip_attempts < max_ip_attempts - 1:
                print_status(f"Trying with different IP (attempt {ip_attempts + 1}/{max_ip_attempts})", "info")
                ip_attempts += 1
                continue
            else:
                print_status("Max IP attempts reached", "error")
                save_unsuccessful_claim(wallet_address, ip_address, "Max IP attempts reached", private_key)
                return False
        
        # Only solve CAPTCHA if wallet and IP are eligible
        print_status("Wallet and IP eligible, solving CAPTCHA...", "info")
        captcha_solution = solve_captcha(HCAPTCHA_SITE_KEY, "https://faucet.0g.ai/")
        if captcha_solution:
            # Claim faucet with proxy retry logic
            success = claim_faucet(wallet_address, captcha_solution, wallet)
            if not success:
                print_status(f"Failed to claim faucet for wallet {wallet_address} after all proxy attempts", "error")
                save_unsuccessful_claim(wallet_address, ip_address, "Failed to claim after proxy attempts", private_key)
                return False
            return True
        else:
            print_status(f"Failed to solve CAPTCHA for wallet {wallet_address}", "error")
            save_unsuccessful_claim(wallet_address, ip_address, "Failed to solve CAPTCHA", private_key)
            return False
            
        ip_attempts += 1
    
    save_unsuccessful_claim(wallet_address, "N/A", "Max IP attempts reached", private_key)
    return False

def claim_faucet(wallet_address: str, captcha_solution: str, wallet: Dict, proxy: Optional[Dict] = None) -> bool:
    """Claim faucet with improved error handling and anti-bot protection"""
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://faucet.0g.ai",
        "referer": "https://faucet.0g.ai/",
        "user-agent": anti_bot.get_random_user_agent()
    }

    data = {
        "address": wallet_address,
        "hcaptchaToken": captcha_solution
    }

    max_proxy_attempts = 3
    proxy_attempts = 0
    used_proxies = set()

    while proxy_attempts < max_proxy_attempts:
        try:
            # Get current IP and geolocation info
            ip_address, ip_info = get_current_ip(proxy)

            # Check eligibility
            if not is_eligible_to_claim(ip_address, wallet_address):
                print_status(f"IP {ip_address} ({ip_info['country']}) has already claimed in the last 24 hours", "warning")
                if proxy_attempts < max_proxy_attempts - 1:
                    print_status(f"Retrying with different proxy (attempt {proxy_attempts + 1}/{max_proxy_attempts})", "info")
                    while True:
                        new_proxy = proxy_manager.get_next_proxy()
                        if new_proxy and new_proxy['url'] not in used_proxies:
                            proxy = new_proxy
                            used_proxies.add(proxy['url'])
                            break
                    proxy_attempts += 1
                    continue
                else:
                    print_status("Max proxy attempts reached for IP rate limited case", "error")
                    return False

            # Make request
            response = make_request(
                "POST",
                FAUCET_URL,
                headers=headers,
                json=data
            )
            response_data = response.json()
            
            # Log response
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response headers: {dict(response.headers)}")
            logger.info(f"Response data: {json.dumps(response_data, indent=2)}")
            
            # Handle response
            if response.status_code == 200 and "message" in response_data:
                tx_hash = response_data["message"]
                print_status(f"Successfully claimed faucet for wallet {wallet_address}", "success")
                print_status(f"Transaction hash: {tx_hash}", "success")
                update_claim_history(ip_address, wallet_address)
                save_successful_claim(wallet_address, ip_address, tx_hash, wallet["private_key"])
                return True
            else:
                print_status(f"Failed to claim faucet for wallet {wallet_address}", "error")
                if 'error' in response_data:
                    print_status(f"Error details: {response_data['error']}", "error")
                save_unsuccessful_claim(wallet_address, ip_address, f"Failed to claim: {response_data.get('error', 'Unknown error')}", wallet["private_key"])
                return False
                
        except Exception as e:
            print_status(f"Error claiming faucet: {e}", "error")
            logger.error(f"Request error: {e}")
            if proxy_attempts < max_proxy_attempts - 1:
                print_status(f"Retrying with different proxy (attempt {proxy_attempts + 1}/{max_proxy_attempts})", "info")
                while True:
                    new_proxy = proxy_manager.get_next_proxy()
                    if new_proxy and new_proxy['url'] not in used_proxies:
                        proxy = new_proxy
                        used_proxies.add(proxy['url'])
                        break
                proxy_attempts += 1
                continue
            save_unsuccessful_claim(wallet_address, ip_address, f"Error: {str(e)}", wallet["private_key"])
            return False

    return False

def load_claim_history():
    """Load claim history from file"""
    try:
        with open(CLAIM_HISTORY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"ip_claims": {}, "wallet_claims": {}}

def save_claim_history(history):
    """Save claim history to file"""
    with open(CLAIM_HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=2)

def is_eligible_to_claim(ip_address: str, wallet_address: str) -> bool:
    """Check if IP and wallet are eligible to claim"""
    history = load_claim_history()
    current_time = datetime.now()
    
    # Check IP rate limit
    if ip_address in history["ip_claims"]:
        last_claim_time = datetime.fromisoformat(history["ip_claims"][ip_address])
        if current_time - last_claim_time < timedelta(hours=24):
            print_status(f"IP {ip_address} has already claimed in the last 24 hours", "warning")
            return False
    
    # Check wallet rate limit
    if wallet_address in history["wallet_claims"]:
        last_claim_time = datetime.fromisoformat(history["wallet_claims"][wallet_address])
        if current_time - last_claim_time < timedelta(hours=24):
            print_status(f"Wallet {wallet_address} has already claimed in the last 24 hours", "warning")
            return False
    
    return True

def update_claim_history(ip_address: str, wallet_address: str):
    """Update claim history with new claim"""
    history = load_claim_history()
    current_time = datetime.now().isoformat()
    
    history["ip_claims"][ip_address] = current_time
    history["wallet_claims"][wallet_address] = current_time
    
    save_claim_history(history)

def create_wallet() -> Optional[Dict]:
    """Create a single Ethereum wallet"""
    try:
        # Create a new Ethereum account
        account = Account.create(os.urandom(32))  # 32 random bytes for the private key
        
        # Derive public key from private key
        private_key = account._private_key
        public_key = keys.PrivateKey(private_key).public_key
        
        # Wallet details
        wallet = {
            "address": account.address,
            "private_key": private_key.hex(),
            "public_key": public_key.to_hex(),
        }
        
        return wallet
    except Exception as e:
        print_status(f"Error creating wallet: {e}", "error")
        logger.error(f"Wallet creation error: {e}")
        return None

def load_wallets(file_path: str = WALLETS_FILE) -> List[Dict]:
    """Load wallets from file and optionally create new ones"""
    try:
        existing_wallets = []
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                existing_wallets = json.load(file)
                print_status(f"Loaded {len(existing_wallets)} existing wallets from {file_path}", "success")
        
        # Ask if user wants to create new wallets
        while True:
            response = input("\nDo you want to create new wallets? (yes/no): ").lower()
            if response in ['yes', 'no']:
                break
            print_status("Please enter 'yes' or 'no'", "warning")
        
        if response == 'yes':
            while True:
                try:
                    num_wallets = int(input("Enter the number of new wallets to create: "))
                    if num_wallets > 0:
                        break
                    print_status("Please enter a positive number", "warning")
                except ValueError:
                    print_status("Please enter a valid number", "warning")
            
            if num_wallets > 0:
                print_status(f"Creating {num_wallets} new wallets...", "progress")
                new_wallets = []
                
                for i in range(num_wallets):
                    wallet = create_wallet()
                    if wallet:
                        new_wallets.append(wallet)
                        print_status(f"Created wallet {i+1}/{num_wallets}: {wallet['address']}", "success")
                
                if new_wallets:
                    # Combine existing and new wallets
                    all_wallets = existing_wallets + new_wallets
                    
                    # Save all wallets to file
                    with open(file_path, 'w') as f:
                        json.dump(all_wallets, f, indent=4)
                    
                    print_status(f"Successfully added {len(new_wallets)} new wallets. Total wallets: {len(all_wallets)}", "success")
                    return all_wallets
                else:
                    print_status("Failed to create new wallets. Using existing wallets.", "warning")
                    return existing_wallets
        
        return existing_wallets
        
    except Exception as e:
        print_status(f"Error loading/creating wallets: {e}", "error")
        logger.error(f"Wallet loading/creation error: {e}")
        exit(1)

def print_summary(wallets: List[Dict]):
    """Print overall summary of the faucet claiming process"""
    successful_claims = load_successful_claims()
    unsuccessful_claims = load_unsuccessful_claims()
    history = load_claim_history()
    
    total_wallets = len(wallets)
    total_successful = len(successful_claims["claims"])
    total_failed = len(unsuccessful_claims["claims"])
    total_skipped = len(history["wallet_claims"])
    
    print_status("\n=== FAUCET CLAIMING SUMMARY ===", "info")
    print_status(f"Total Wallets: {total_wallets}", "info")
    print_status(f"Successfully Claimed: {total_successful}", "success")
    print_status(f"Failed Claims: {total_failed}", "error")
    print_status(f"Skipped (Already Claimed): {total_skipped}", "warning")
    print_status(f"Remaining Wallets: {total_wallets - total_successful - total_failed - total_skipped}", "info")
    
    # Print failure reasons
    if total_failed > 0:
        print_status("\n=== FAILURE REASONS ===", "warning")
        failure_reasons = {}
        for claim in unsuccessful_claims["claims"]:
            reason = claim["reason"]
            failure_reasons[reason] = failure_reasons.get(reason, 0) + 1
        
        for reason, count in failure_reasons.items():
            print_status(f"{reason}: {count} wallets", "warning")
    
    print_status("\n=== SUCCESSFUL CLAIMS BY COUNTRY ===", "success")
    country_stats = {}
    for claim in successful_claims["claims"]:
        ip_info = get_ip_info(claim["ip_address"])
        country = ip_info["country"]
        country_stats[country] = country_stats.get(country, 0) + 1
    
    for country, count in country_stats.items():
        print_status(f"{country}: {count} claims", "success")

def print_banner():
    """Print the ASCII art banner"""
    banner = """
  ('-.      .-')    ('-. .-.             
  ( OO ).-. ( OO ). ( OO )  /             
  / . --. /(_)---\_),--. ,--. ,--. ,--.   
  | \-.  \ /    _ | |  | |  | |  | |  |   
.-'-'  |  |\  :` `. |   .|  | |  | | .-') 
 \| |_.'  | '..`''.)|       | |  |_|( OO )
  |  .-.  |.-._)   \|  .-.  | |  | | `-' /
  |  | |  |\       /|  | |  |('  '-'(_.-' 
  `--' `--' `-----' `--' `--'  `-----'    
                                                                                                  
    Auto Faucet Claim Tool For 0G Labs- Ashu || XD
    Author  : Ashu || XD
    Get Updates: https://telegram.dog/lootersera_th    
    """
    print(Fore.CYAN + banner + Style.RESET_ALL)

def main():
    print_banner()
    print_status("Starting faucet claim process...", "info")
    
    # Load wallets and proxies
    wallets = load_wallets()
    if not proxy_manager.load_proxies():
        print_status("Warning: No valid proxies found. Using direct connection which may be rate limited.", "warning")
    else:
        print_status(f"Successfully loaded {len(proxy_manager.proxies)} proxies", "success")

    # Load claim history
    history = load_claim_history()
    current_time = datetime.now()

    # Get number of threads from user
    while True:
        try:
            num_threads = int(input("\nEnter number of concurrent threads (1-10): "))
            if 1 <= num_threads <= 10:
                break
            print_status("Please enter a number between 1 and 10", "warning")
        except ValueError:
            print_status("Please enter a valid number", "warning")

    print_status(f"Starting processing with {num_threads} threads...", "info")

    # Create thread pool
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit all wallet processing tasks
        future_to_wallet = {
            executor.submit(process_wallet, wallet, history, current_time): wallet 
            for wallet in wallets
        }

        # Process completed tasks
        for future in concurrent.futures.as_completed(future_to_wallet):
            wallet = future_to_wallet[future]
            try:
                success = future.result()
                if success:
                    print_status(f"Successfully processed wallet {wallet['address']}", "success")
            except Exception as e:
                print_status(f"Error processing wallet {wallet['address']}: {e}", "error")

    print_status("\nFaucet claim process completed!", "success")
    
    # Print final summary
    print_summary(wallets)

if __name__ == "__main__":
    main()
