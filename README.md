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
