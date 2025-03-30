# 🚀 0G Faucet Claimer

<div align="center">

![0G Faucet](https://img.shields.io/badge/0G-Faucet-blue)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

<div align="center">
  <h3>⚡ Fast & Efficient Faucet Claiming ⚡</h3>
</div>

## 🌟 Features

> 🔄 **Multi-wallet Support**: Process multiple wallets simultaneously
>
> 🌐 **Smart Proxy Rotation**: Automatic proxy switching with health tracking
>
> 📍 **IP Geolocation**: Track and manage IP locations
>
> 🛡️ **Anti-Bot Protection**: Built-in protection mechanisms
>
> ⚡ **Multi-threading**: Process multiple claims concurrently
>
> 🤖 **CAPTCHA Integration**: Automatic CAPTCHA solving
>
> 📊 **Detailed Analytics**: Comprehensive logging and statistics
>
> ✅ **Success Tracking**: Monitor successful and failed claims

## 🛠️ Installation

### 📦 Prerequisites

- Python 3.8 or higher
- Git
- pip (Python package manager)

### 🐧 Ubuntu Installation Guide

1. Update system packages:

   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. Install Python and pip:

   ```bash
   sudo apt install python3 python3-pip git -y
   ```

3. Clone the repository:

   ```bash
   git clone https://github.com/Ashuxd-X/0G-Faucet.git
   cd 0G-Faucet
   ```

4. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

### 🪟 Windows Installation Guide

1. Install Python:

   - Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
   - Run installer with "Add Python to PATH" option checked
   - Verify installation: `python --version`

2. Install Git:

   - Download Git from [git-scm.com](https://git-scm.com/download/win)
   - Run installer with default options

3. Clone the repository:

   ```bash
   git clone https://github.com/Ashuxd-X/0G-Faucet.git
   cd 0G-Faucet
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. Create environment file:

   ```bash
   # Ubuntu/Linux
   cp .env.example .env

   # Windows
   copy .env.example .env
   ```

2. Edit `.env` file with your settings:

   ```env
   ANTICAPTCHA_API_KEY=your_anticaptcha_api_key
   FAUCET_URL=https://faucet.0g.ai/api/faucet
   ```

3. Prepare data files:

   ```bash
   # Ubuntu/Linux
   cp data/wallets.example.json data/wallets.json
   cp data/proxies.example.txt data/proxies.txt

   # Windows
   copy data\wallets.example.json data\wallets.json
   copy data\proxies.example.txt data\proxies.txt
   ```

4. Edit data files:
   - Add your wallet addresses to `data/wallets.json`
   - Add your proxy list to `data/proxies.txt`

## 🚀 Usage

### 🐧 Ubuntu/Linux Execution

1. Run the script:

   ```bash
   python3 src/faucet.py
   ```

2. Follow the prompts:
   - Create new wallets (optional)
   - Set number of concurrent threads
   - Monitor the claiming process

### 🪟 Windows Execution

1. Run the script:

   ```bash
   python src/faucet.py
   ```

2. Follow the prompts:
   - Create new wallets (optional)
   - Set number of concurrent threads
   - Monitor the claiming process

### 📊 Monitoring Output

- Check `data/successful_claims.json` for successful claims
- Check `data/unsuccessful_claims.json` for failed claims
- View `data/claim_history.json` for complete history
- Monitor `logs/faucet.log` for detailed logging

### 🔄 Common Operations

1. **Adding New Wallets**:

   ```bash
   # Edit wallets.json with new addresses
   nano data/wallets.json  # Linux
   notepad data\wallets.json  # Windows
   ```

2. **Updating Proxies**:

   ```bash
   # Edit proxies.txt with new proxy list
   nano data/proxies.txt  # Linux
   notepad data\proxies.txt  # Windows
   ```

3. **Viewing Logs**:
   ```bash
   # Real-time log viewing
   tail -f logs/faucet.log  # Linux
   type logs\faucet.log  # Windows
   ```

## 📁 Project Structure

```
0G-Faucet/
├── 📄 README.md
├── 📄 requirements.txt
├── 📄 .env.example
├── 📄 LICENSE
├── 📁 src/
│   └── 📄 faucet.py
├── 📁 data/
│   ├── 📄 wallets.example.json
│   └── 📄 proxies.example.txt
└── 📁 logs/
```

## 📊 Output Files

- `data/successful_claims.json`: Records of successful claims
- `data/unsuccessful_claims.json`: Records of failed claims
- `data/claim_history.json`: History of claims
- `logs/faucet.log`: Detailed logging information

## 🔒 Security

- Private keys are stored securely
- Proxies are rotated automatically
- Rate limiting protection
- IP geolocation tracking

## 📞 Support

For support, join our Telegram channel: [Looters Era](https://telegram.dog/lootersera_th)

## ⚠️ Disclaimer

> **Educational Purpose Only**
>
> This project is created for educational and learning purposes only. It serves as a demonstration of blockchain interaction and faucet claiming mechanisms.
>
> **Use at Your Own Risk**
>
> - This tool is provided "as is" without any warranties
> - Users are responsible for their own actions and compliance with network rules
> - The developers are not responsible for any misuse or consequences
> - Always verify the security and legitimacy of any blockchain interaction
> - Use this tool responsibly and in accordance with the network's terms of service

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For support, join our Telegram channel: [Looters Era](https://telegram.dog/lootersera_th)

---

<div align="center">
  <h3>Made with ❤️ by Ashu || XD</h3>
</div>

<!--
  ╔══════════════════════════════════════╗
  ║  Thanks for using 0G Faucet Claimer  ║
  ╚══════════════════════════════════════╝
-->
