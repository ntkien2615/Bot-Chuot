# Discord Bot với Lập Trình Hướng Đối Tượng (OOP)

Bot Discord được viết bằng Python với kiến trúc hướng đối tượng (OOP) để dễ dàng bảo trì và mở rộng.

## Cấu trúc thư mục

```
├── commands/                  # Thư mục chứa các lệnh
│   ├── base_command.py        # Lớp cơ sở cho tất cả các lệnh
│   ├── command_manager.py     # Trình quản lý lệnh
│   ├── fun/                   # Lệnh giải trí
│   ├── general/               # Lệnh chung
│   ├── slash/                 # Lệnh slash
│   └── non-slash/             # Lệnh không phải slash
├── commands_info/             # Thông tin về lệnh
├── message/                   # Xử lý tin nhắn
├── status/                    # Xử lý trạng thái bot
├── txt_files/                 # Các file văn bản
├── img/                       # Hình ảnh
├── constants.py               # Hằng số
├── config.py                  # Cấu hình
├── database.py                # Cơ sở dữ liệu
├── error_handler.py           # Xử lý lỗi
├── keep_alive.py              # Giữ bot hoạt động
├── main.py                    # File chính của bot
├── utils.py                   # Tiện ích
└── requirements.txt           # Các thư viện cần thiết
```

## Cấu trúc OOP

### Lớp DiscordBot
Lớp chính quản lý toàn bộ bot, khởi tạo các thành phần và khởi động bot.

### Lớp BaseCommand
Lớp cơ sở cho tất cả các lệnh, cung cấp các phương thức chung.

### Lớp SlashCommand và PrefixCommand
Các lớp cơ sở cho lệnh slash và lệnh prefix, kế thừa từ BaseCommand.

### Lớp FunCommand, GeneralCommand, UtilityCommand
Các lớp cụ thể cho từng loại lệnh, kế thừa từ SlashCommand.

### Lớp CommandManager
Quản lý việc tải và đăng ký các lệnh.

### Lớp Database
Lớp cơ sở cho cơ sở dữ liệu, với các lớp con như FileDatabase, MongoDatabase và RuleDatabase.

### Lớp Config
Quản lý cấu hình bot, sử dụng mẫu Singleton để đảm bảo chỉ có một phiên bản.

### Lớp ErrorHandler
Xử lý các lỗi phát sinh trong quá trình hoạt động của bot.

### Lớp tiện ích
Các lớp như EmbedBuilder, MessageUtils, FileUtils, TimeUtils cung cấp các tiện ích chung.

## Cách sử dụng

1. Cài đặt các thư viện cần thiết:
```
pip install -r requirements.txt
```

2. Tạo file .env với token Discord và MongoDB:
```
# Discord Bot Settings
discord_token=your_token_here
bot_owner_id=your_id_here
debug_mode=False

# MongoDB Settings
MONGODB_URI=mongodb+srv://username:password@clustername.mongodb.net/?retryWrites=true&w=majority
MONGODB_DATABASE=botchuot
```

3. Chạy bot:
```
python main.py
```

## Sử dụng MongoDB

Bot này có tích hợp MongoDB để lưu trữ dữ liệu. Để sử dụng MongoDB:

1. Tạo tài khoản miễn phí trên [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Tạo một Cluster miễn phí
3. Tạo một Database User với quyền đọc và ghi
4. Lấy Connection String từ MongoDB Atlas
5. Thêm Connection String vào file .env như mẫu trên

Lớp MongoDatabase được thiết kế để hoạt động với MongoDB Atlas:

```python
from database import MongoDatabase

# Tạo một instance của MongoDatabase với collection cụ thể
db = MongoDatabase(collection_name="my_collection")

# Đảm bảo db đã được kết nối
db.load()

# Lưu dữ liệu
db.set("key1", "value1")
db.set("key2", {"name": "User", "age": 25})

# Lấy dữ liệu
result = db.get("key1")

# Tìm kiếm dữ liệu
results = db.search("user")

# Xóa dữ liệu
db.delete("key1")
```

## Thêm lệnh mới

Để thêm lệnh mới, tạo một file trong thư mục tương ứng (fun, general, v.v.) và kế thừa từ lớp tương ứng:

```python
from commands.base_command import FunCommand

class MyCommand(FunCommand):
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "mycommand"
        self.description = "Mô tả lệnh của tôi"
    
    async def execute(self, interaction, *args, **kwargs):
        # Xử lý lệnh
        await interaction.response.send_message("Hello!")
    
    @app_commands.command(name='mycommand', description='Mô tả lệnh của tôi')
    async def mycommand(self, interaction: discord.Interaction):
        await self.execute(interaction)

async def setup(bot):
    await bot.add_cog(MyCommand(bot))
```
