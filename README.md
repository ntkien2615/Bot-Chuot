# 🐭 Bot Chuột

Đây là con bot Discord Chuột - Hàng nhà làm với tình yêu! 💖

## 🎮 Tính năng

- **🎯 Games**: Tetris, Tài Xỉu, Rock Paper Scissors, Gun Roulette, Guess Number
- **😄 Fun Commands**: Hack simulator, Kiss, Hug, Rate, và nhiều hơn nữa
- **💰 Economy**: Hệ thống kinh tế đơn giản
- **🔧 General**: Ping, Help, User Info, Search

## 🚀 Deploy lên Render.com

### 1. Chuẩn bị
1. Fork repository này
2. Tạo tài khoản [Render.com](https://render.com)
3. Chuẩn bị Discord Bot Token và MongoDB URI

### 2. Environment Variables
Tạo các environment variables sau trong Render:

```env
BOT_TOKEN=your_discord_bot_token
MONGO_URI=your_mongodb_uri
DEBUG_MODE=false
KEEPALIVE_URL=https://your-app-name.onrender.com
```

### 3. Deploy
1. Tạo **Web Service** mới trên Render
2. Connect GitHub repository
3. Chọn branch `main`
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `python main.py`
6. Thêm Environment Variables
7. Deploy!

## 📦 Local Development

```bash
# Clone repository
git clone https://github.com/your-username/Bot-Chuot.git
cd Bot-Chuot

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env với thông tin của bạn
# Chạy bot
python main.py
```

## 🛠️ Tech Stack

- **Python 3.11+**
- **discord.py** - Discord API wrapper
- **MongoDB** - Database
- **Flask** - Keep-alive web server
- **Render.com** - Hosting platform

## 📝 License

Hàng nhà làm - Sử dụng thoải mái! 🎉