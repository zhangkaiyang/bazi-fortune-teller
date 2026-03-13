# 八字算命网站 (Bazi Fortune Teller)

一个现代化的八字命理分析系统，输入出生年月日时，输出八字排盘、五行分析和年度运势。

![八字算命](https://img.shields.io/badge/八字-命理分析-red)
![Vue.js](https://img.shields.io/badge/Vue.js-3.x-green)
![FastAPI](https://img.shields.io/badge/FastAPI-Python-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ 功能特性

### 🎯 核心功能
- **八字排盘**：精确计算年柱、月柱、日柱、时柱
- **五行分析**：可视化五行平衡图表
- **十神解析**：详细的关系和性格分析
- **年度运势**：基于八字的运势预测
- **生活建议**：个性化的改进建议

### 🎨 特色功能
- **响应式设计**：支持桌面、平板、手机
- **传统美学**：中国红、太极元素、传统配色
- **实时计算**：输入即得结果，无需等待
- **数据可视化**：五行平衡图表，一目了然
- **隐私保护**：本地计算，不存储敏感信息

## 🚀 快速开始

### 环境要求
- Node.js 16+
- Python 3.8+
- Git

### 安装步骤

```bash
# 克隆项目
git clone https://github.com/zhangkaiyang/bazi-fortune-teller.git
cd bazi-fortune-teller

# 安装前端依赖
cd frontend
npm install

# 安装后端依赖
cd ../backend
pip install -r requirements.txt

# 启动开发服务器
# 前端
cd frontend
npm run dev

# 后端
cd backend
python main.py
```

## 🏗️ 项目结构

```
bazi-fortune-teller/
├── frontend/          # Vue.js 前端应用
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/           # FastAPI 后端服务
│   ├── api/
│   ├── services/
│   ├── models/
│   └── main.py
├── shared/           # 共享代码
│   └── bazi-calculator.js
├── docs/            # 文档
│   ├── 项目设计文档.md
│   └── API文档.md
├── prototype.html   # 原型界面
└── README.md
```

## 📊 技术架构

### 前端技术栈
- **Vue 3** + **Vite** + **TypeScript**
- **Element Plus** UI 组件库
- **ECharts** 数据可视化
- **Tailwind CSS** 样式框架

### 后端技术栈
- **FastAPI** Python Web 框架
- **SQLite/PostgreSQL** 数据库
- **JWT** 认证
- **Redis** 缓存（可选）

### 八字计算库
- **lunar-python**：农历转换
- **sizhu**：四柱计算
- **opencc**：简繁转换

## 📱 界面预览

### 输入界面
```
┌─────────────────────────────────────┐
│           八字命理分析系统           │
│              🧮  🪐  📜             │
├─────────────────────────────────────┤
│ 出生日期： [YYYY-MM-DD]  📅         │
│ 出生时间： [HH:MM]       ⏰         │
│ 性别：     ○ 男   ○ 女            │
│ 是否考虑真太阳时： ☑ 是  ☐ 否      │
│                                     │
│        [ 开始测算 ]  [ 重置 ]       │
└─────────────────────────────────────┘
```

### 结果界面
```
┌─────────────────────────────────────┐
│       🧮 八字命理分析结果 🪐         │
├─────────────────────────────────────┤
│ 八字排盘：己巳 丁丑 庚辰 庚辰       │
│ 五行分析：金2 木0 水1 火2 土3      │
│ 日主分析：庚金，性格坚毅果断        │
│ 2026年运势：事业有突破，注意健康     │
│ 生活建议：多接触绿色植物            │
└─────────────────────────────────────┘
```

## 🔧 开发计划

### 阶段 1：MVP (1-2周)
- [x] 项目设计和原型
- [ ] 八字计算核心算法
- [ ] 基础输入界面
- [ ] 简单结果显示
- [ ] 本地存储查询记录

### 阶段 2：功能完善 (2-3周)
- [ ] 五行分析可视化
- [ ] 十神关系图
- [ ] 年度运势详细分析
- [ ] 用户账户系统

### 阶段 3：高级功能 (3-4周)
- [ ] 八字合婚功能
- [ ] 每日运势推送
- [ ] 命理知识库
- [ ] 移动端适配

### 阶段 4：优化部署 (1-2周)
- [ ] 性能优化
- [ ] SEO 优化
- [ ] 多语言支持
- [ ] 生产部署

## 📖 八字计算原理

### 1. 农历转换
- 公历转农历
- 考虑节气划分月份
- 真太阳时校正

### 2. 四柱计算
- 年柱：立春为界
- 月柱：节气划分
- 日柱：公式计算
- 时柱：日干推算

### 3. 五行分析
- 天干地支五行属性
- 五行生克关系
- 五行平衡建议

### 4. 十神解析
- 比肩、劫财
- 食神、伤官
- 正财、偏财
- 正官、七杀
- 正印、偏印

## 🧪 测试数据

```json
{
  "birth_date": "1990-01-15",
  "birth_time": "08:30",
  "gender": "male",
  "use_solar_time": true
}
```

预期结果：
- 八字：己巳 丁丑 庚辰 庚辰
- 五行：金2 木0 水1 火2 土3
- 日主：庚金（阳金）
- 运势：2026年丙午年，事业有突破

## 🤝 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系我们

- 项目作者：大黄
- GitHub：[zhangkaiyang](https://github.com/zhangkaiyang)
- 邮箱：787653759@qq.com

## ⚠️ 免责声明

本系统仅供娱乐参考，不构成任何专业建议。命理测算结果不应作为人生决策的唯一依据。请理性看待，积极面对生活。

---

**八字算命，传统文化，科学看待，娱乐为主**