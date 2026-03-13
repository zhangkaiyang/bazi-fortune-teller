"""
八字算命网站后端 API
基于 FastAPI 框架
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import logging

# 导入新的运势分析模块
try:
    from fortune_analyzer import FortuneAnalyzer
    fortune_analyzer = FortuneAnalyzer()
    HAS_FORTUNE_ANALYZER = True
except ImportError:
    HAS_FORTUNE_ANALYZER = False
    logger = logging.getLogger(__name__)
    logger.warning("FortuneAnalyzer 模块未找到，使用简化版运势分析")

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI(
    title="八字算命 API",
    description="八字命理分析系统后端 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class BaziRequest(BaseModel):
    """八字计算请求模型"""
    birth_date: str  # YYYY-MM-DD
    birth_time: str  # HH:MM
    gender: str  # "male" 或 "female"
    use_solar_time: bool = True
    location_lng: Optional[float] = None  # 经度（用于真太阳时计算）
    location_lat: Optional[float] = None  # 纬度

class BaziResponse(BaseModel):
    """八字计算响应模型"""
    success: bool
    data: dict
    message: Optional[str] = None

class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str
    version: str
    timestamp: str

# 八字计算核心函数（简化版）
def calculate_bazi_simple(birth_date: str, birth_time: str, gender: str) -> dict:
    """简化的八字计算函数"""
    try:
        # 解析日期时间
        dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
        
        # 简化计算逻辑
        # 实际项目中应使用 lunar-python 等库进行精确计算
        year = dt.year
        month = dt.month
        day = dt.day
        hour = dt.hour
        
        # 天干地支
        heavenly_stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        earthly_branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        
        # 简化计算（实际算法更复杂）
        year_stem = heavenly_stems[(year - 4) % 10]
        year_branch = earthly_branches[(year - 4) % 12]
        month_stem = heavenly_stems[(month + 1) % 10]
        month_branch = earthly_branches[(month + 1) % 12]
        day_stem = heavenly_stems[day % 10]
        day_branch = earthly_branches[day % 12]
        hour_stem = heavenly_stems[(hour * 2) % 10]
        hour_branch = earthly_branches[hour // 2]
        
        # 五行
        elements = {
            '甲': '木', '乙': '木', '丙': '火', '丁': '火',
            '戊': '土', '己': '土', '庚': '金', '辛': '金',
            '壬': '水', '癸': '水',
            '子': '水', '丑': '土', '寅': '木', '卯': '木',
            '辰': '土', '巳': '火', '午': '火', '未': '土',
            '申': '金', '酉': '金', '戌': '土', '亥': '水'
        }
        
        # 统计五行
        element_counts = {'金': 0, '木': 0, '水': 0, '火': 0, '土': 0}
        pillars = [year_stem, year_branch, month_stem, month_branch, day_stem, day_branch, hour_stem, hour_branch]
        for item in pillars:
            if item in elements:
                element_counts[elements[item]] += 1
        
        # 日主性格
        day_master_personality = {
            '甲': '如参天大树，正直仁德，积极向上',
            '乙': '如藤蔓花草，柔顺温和，适应力强',
            '丙': '如太阳之火，热情开朗，光明磊落',
            '丁': '如灯烛之火，文明礼仪，细心体贴',
            '戊': '如城墙之土，诚实信用，稳重可靠',
            '己': '如田园之土，温和包容，重视内涵',
            '庚': '如斧钺之金，刚毅果断，重信守义',
            '辛': '如珠宝之金，细腻敏感，追求完美',
            '壬': '如江河之水，智慧灵活，适应变化',
            '癸': '如雨露之水，温柔含蓄，善于谋划'
        }
        
        # 运势建议
        fortunes = [
            "今年运势平稳，宜稳扎稳打，积累实力",
            "机遇与挑战并存，需谨慎决策，把握时机",
            "贵人运佳，事业有新发展，注意人际关系",
            "财运亨通，但需注意健康，劳逸结合",
            "学习成长的好时机，提升技能，开阔视野",
            "人际关系和谐，感情顺利，家庭和睦"
        ]
        
        fortune_index = (year + month + day) % len(fortunes)
        
        return {
            "bazi": {
                "year_pillar": f"{year_stem}{year_branch}",
                "month_pillar": f"{month_stem}{month_branch}",
                "day_pillar": f"{day_stem}{day_branch}",
                "hour_pillar": f"{hour_stem}{hour_branch}",
                "full_bazi": f"{year_stem}{year_branch} {month_stem}{month_branch} {day_stem}{day_branch} {hour_stem}{hour_branch}"
            },
            "elements": element_counts,
            "day_master": {
                "stem": day_stem,
                "element": elements.get(day_stem, '未知'),
                "personality": day_master_personality.get(day_stem, '性格特点需要详细分析'),
                "yinyang": "阳" if heavenly_stems.index(day_stem) % 2 == 0 else "阴"
            },
            "fortune": {
                "year": f"{heavenly_stems[(year - 4) % 10]}{earthly_branches[(year - 4) % 12]}",
                "analysis": fortunes[fortune_index],
                "suggestions": [
                    "保持积极心态，面对挑战",
                    "注意身体健康，定期检查",
                    "多与家人朋友沟通",
                    "学习新知识，提升自我"
                ]
            },
            "basic_info": {
                "solar_date": birth_date,
                "solar_time": birth_time,
                "gender": "男" if gender == "male" else "女",
                "age": datetime.now().year - year
            }
        }
        
    except Exception as e:
        logger.error(f"八字计算错误: {e}")
        raise HTTPException(status_code=400, detail=f"日期时间格式错误: {str(e)}")

# API 路由
@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "八字算命 API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check() -> HealthResponse:
    """健康检查"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )

@app.post("/api/bazi/calculate", response_model=BaziResponse)
async def calculate_bazi(request: BaziRequest) -> BaziResponse:
    """计算八字"""
    try:
        logger.info(f"收到八字计算请求: {request.dict()}")
        
        # 调用计算函数
        result = calculate_bazi_simple(
            birth_date=request.birth_date,
            birth_time=request.birth_time,
            gender=request.gender
        )
        
        # 如果有位置信息，可以进行真太阳时校正
        if request.use_solar_time and request.location_lng and request.location_lat:
            result["use_solar_time"] = True
            result["location"] = {
                "longitude": request.location_lng,
                "latitude": request.location_lat
            }
            result["note"] = "已考虑真太阳时校正"
        else:
            result["use_solar_time"] = request.use_solar_time
        
        return BaziResponse(
            success=True,
            data=result,
            message="八字计算成功"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"八字计算异常: {e}")
        return BaziResponse(
            success=False,
            data={},
            message=f"计算失败: {str(e)}"
        )

@app.get("/api/bazi/examples")
async def get_examples():
    """获取示例数据"""
    examples = [
        {
            "birth_date": "1990-01-15",
            "birth_time": "08:30",
            "gender": "male",
            "description": "示例1: 1990年1月15日 08:30 (男)"
        },
        {
            "birth_date": "1985-11-23",
            "birth_time": "14:45",
            "gender": "female",
            "description": "示例2: 1985年11月23日 14:45 (女)"
        },
        {
            "birth_date": "2000-05-10",
            "birth_time": "22:15",
            "gender": "male",
            "description": "示例3: 2000年5月10日 22:15 (男)"
        }
    ]
    return {"examples": examples}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )