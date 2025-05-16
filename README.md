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
Lớp cơ sở cho cơ sở dữ liệu, với các lớp con như FileDatabase và RuleDatabase.

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

2. Tạo file .env với token Discord:
```
discord_token=your_token_here
bot_owner_id=your_id_here
debug_mode=False
```

3. Chạy bot:
```
python main.py
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
