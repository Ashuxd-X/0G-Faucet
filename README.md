# 0G Faucet 🚰

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)](https://github.com/Ashuxd-X/0G-Faucet)

A powerful and secure faucet system for the 0G Network, designed to distribute test tokens efficiently and fairly. Built with Python and FastAPI, this faucet system provides a robust solution for developers and users to obtain test tokens on the 0G Network.

## 🌟 Features

- **Secure Authentication**: Multi-level security with API key and wallet verification
- **Rate Limiting**: Built-in protection against abuse
- **Fair Distribution**: Smart cooldown system to ensure equitable token distribution
- **Easy Configuration**: Simple setup through environment variables
- **Detailed Logging**: Comprehensive logging for monitoring and debugging
- **Health Monitoring**: Built-in health check endpoint
- **Error Handling**: Robust error management and user feedback
- **Documentation**: Comprehensive API documentation with Swagger UI

## 📋 Description

The 0G Faucet is a specialized service designed to facilitate the distribution of test tokens on the 0G Network. It serves as a crucial tool for developers, testers, and users who need test tokens for development, testing, or experimentation purposes.

### Key Capabilities

- **Token Distribution**: Efficiently distributes test tokens to verified users
- **Security Measures**: Implements multiple security layers to prevent abuse
- **User Management**: Tracks user requests and implements cooldown periods
- **Network Integration**: Seamlessly connects with the 0G Network
- **Monitoring Tools**: Provides detailed insights into faucet operations
- **Developer Friendly**: Easy to set up and integrate with existing systems

### Use Cases

- Development and testing on the 0G Network
- User onboarding and testing
- Network stress testing
- Integration testing
- Educational purposes

## 🛠️ Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Ashuxd-X/0G-Faucet.git
   cd 0G-Faucet
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. Create a `.env` file:

   ```env
   ANTICAPTCHA_API_KEY=your_anticaptcha_api_key
   FAUCET_URL=https://faucet.0g.ai/api/claim
   ```

2. Prepare your files:
   - `data/wallets.json`: List of Ethereum wallets
   - `data/proxies.txt`: List of proxies

## 🚀 Usage

1. Run the script:

   ```bash
   python src/faucet.py
   ```

2. Follow the prompts:
   - Create new wallets (optional)
   - Set number of concurrent threads
   - Monitor the claiming process

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

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For support, join our Telegram channel: [Looters Era](https://telegram.dog/lootersera_th)

---

<div align="center">
  <h3>Made with ❤️ by Ash || XD</h3>
</div>

<!--
  ╔══════════════════════════════════════╗
  ║  Thanks for using 0G Faucet Claimer  ║
  ╚══════════════════════════════════════╝
-->
