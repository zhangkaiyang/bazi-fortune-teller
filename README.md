# 八字算命网站 (Bazi Fortune Teller)

一个基于传统八字命理学的在线算命网站，提供八字计算、五行分析、运势预测等功能。

## 🌐 在线演示
- 网站地址: http://139.159.230.20
- API地址: http://139.159.230.20:8000
- API文档: http://139.159.230.20:8000/docs

## ✨ 功能特性

### 🧮 八字计算
- 输入出生日期、时间、性别
- 自动计算年柱、月柱、日柱、时柱
- 支持真太阳时调整
- 精确的农历转换

### ⚖️ 五行分析
- 金、木、水、火、土五行分布
- 五行相生相克关系
- 五行平衡度分析
- 可视化柱状图展示

### 📈 运势预测
- 基于日主和五行平衡的运势评分
- 运势等级：大吉、吉、中平、小凶、大凶
- 个性化生活建议
- 流年运势分析

### 🐕 其他功能
- 生肖计算
- 纳音五行
- 日主性格分析
- 查询历史统计

## 🏗️ 技术架构

### 前端
- **HTML5** + **CSS3** + **JavaScript**（原生）
- 响应式设计，支持手机、平板、电脑
- 中国传统配色（朱红、玄黑、金黄）
- 现代化UI设计

### 后端
- **Python FastAPI** - 高性能异步框架
- **SQLite** - 轻量级数据库
- **Nginx** - 反向代理服务器
- **八字算法** - 传统命理学算法

### 部署
- **Ubuntu 24.04** 服务器
- **Docker** 容器化（可选）
- **Python虚拟环境**
- **80/443端口** HTTP/HTTPS访问

## 🚀 快速部署

### 方式一：直接部署（推荐）
```bash
# 1. 克隆项目
git clone https://github.com/zhangkaiyang/bazi-fortune-teller.git
cd bazi-fortune-teller

# 2. 安装依赖
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. 启动后端服务
nohup python -m uvicorn main:app --host 0.0.0.0 --port 8000 &

# 4. 配置Nginx
sudo cp nginx-frontend.conf /etc/nginx/sites-available/bazi-fortune-teller
sudo ln -sf /etc/nginx/sites-available/bazi-fortune-teller /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### 方式二：Docker部署
```bash
# 使用Docker Compose一键部署
docker-compose up -d
```

### 方式三：使用管理脚本
```bash
# 启动服务
./start_direct.sh

# 停止服务
./stop_direct.sh

# 重启服务
./restart_direct.sh
```

## 📁 项目结构

```
bazi-fortune-teller/
├── backend/                    # 后端代码
│   ├── main.py                # FastAPI主程序
│   ├── bazi_calculator.py     # 八字计算器
│   ├── advanced_bazi.py       # 高级八字算法
│   ├── requirements.txt       # Python依赖
│   ├── venv/                  # Python虚拟环境
│   └── bazi.db               # SQLite数据库
├── frontend/                  # 前端代码
│   └── index.html            # 主页面
├── docs/                      # 文档
├── shared/                    # 共享资源
├── docker-compose.yml         # Docker Compose配置
├── nginx-frontend.conf        # Nginx配置
├── start_direct.sh           # 启动脚本
├── stop_direct.sh            # 停止脚本
├── restart_direct.sh         # 重启脚本
└── README.md                 # 项目说明
```

## 🔧 API接口

### 健康检查
```http
GET /health
```

### 八字计算
```http
POST /api/bazi/calculate
Content-Type: application/json

{
  "birth_date": "1990-01-15",
  "birth_time": "08:30",
  "gender": "male",
  "use_solar_time": true
}
```

### 查询统计
```http
GET /api/bazi/stats
```

### 示例数据
```http
GET /api/bazi/examples
```

## 📊 算法说明

### 八字计算原理
1. **年柱计算**：以立春为分界点
2. **月柱计算**：根据节气划分月份
3. **日柱计算**：基于公历日期计算
4. **时柱计算**：根据日干和时辰计算

### 五行分析
- 天干五行：甲乙木、丙丁火、戊己土、庚辛金、壬癸水
- 地支五行：寅卯木、巳午火、申酉金、亥子水、辰戌丑未土
- 藏干五行：考虑地支藏干的五行属性

### 运势预测
- **日主强弱**：分析日主五行在八字中的强弱
- **五行平衡**：分析金木水火土的分布平衡
- **生克关系**：分析五行相生相克关系
- **综合评分**：根据以上因素计算运势得分

## 🔒 隐私保护

- 不存储用户的出生日期等敏感信息
- 查询记录仅用于统计，不关联个人身份
- 所有计算在服务器端完成，客户端不保存数据
- 支持HTTPS加密传输（需要配置SSL证书）

## 📈 性能优化

- 使用FastAPI异步框架，支持高并发
- SQLite数据库，轻量级无依赖
- Nginx反向代理，支持缓存和负载均衡
- 前端静态资源CDN加速（可选）
- 数据库查询优化，支持索引

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- 感谢传统命理学的智慧
- 感谢所有开源项目的贡献者
- 感谢用户的支持和反馈

## 📞 联系方式

如有问题或建议，请通过GitHub Issues提交。

---

**免责声明**：本系统仅供娱乐参考，不构成任何专业建议。命理测算结果不应作为人生决策的唯一依据。