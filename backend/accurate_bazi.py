"""
准确的八字计算模块
基于传统八字算法
"""

from datetime import datetime
from typing import Dict

class AccurateBaziCalculator:
    """准确的八字计算器"""
    
    # 天干
    HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    
    # 地支
    EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 节气表（公历日期，简化版）
    # 每月第一个节气的大致日期和对应的月支
    SOLAR_TERMS = [
        (1, 5, '小寒', '丑'),   # 1月5日左右，丑月开始
        (2, 4, '立春', '寅'),   # 2月4日左右，寅月开始
        (3, 5, '惊蛰', '卯'),   # 3月5日左右，卯月开始
        (4, 4, '清明', '辰'),   # 4月4日左右，辰月开始
        (5, 5, '立夏', '巳'),   # 5月5日左右，巳月开始
        (6, 5, '芒种', '午'),   # 6月5日左右，午月开始
        (7, 7, '小暑', '未'),   # 7月7日左右，未月开始
        (8, 7, '立秋', '申'),   # 8月7日左右，申月开始
        (9, 7, '白露', '酉'),   # 9月7日左右，酉月开始
        (10, 8, '寒露', '戌'),  # 10月8日左右，戌月开始
        (11, 7, '立冬', '亥'),  # 11月7日左右，亥月开始
        (12, 7, '大雪', '子'),  # 12月7日左右，子月开始
    ]
    
    # 天干五行
    STEM_ELEMENTS = {
        '甲': '木', '乙': '木', '丙': '火', '丁': '火',
        '戊': '土', '己': '土', '庚': '金', '辛': '金',
        '壬': '水', '癸': '水'
    }
    
    # 地支五行
    BRANCH_ELEMENTS = {
        '子': '水', '丑': '土', '寅': '木', '卯': '木',
        '辰': '土', '巳': '火', '午': '火', '未': '土',
        '申': '金', '酉': '金', '戌': '土', '亥': '水'
    }
    
    # 日主性格
    DAY_MASTER_PERSONALITY = {
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
    
    @classmethod
    def get_month_branch(cls, month: int, day: int) -> str:
        """根据节气获取月支"""
        # 查找对应的节气
        for i in range(len(cls.SOLAR_TERMS)):
            term_month, term_day, _, branch = cls.SOLAR_TERMS[i]
            
            if month == term_month:
                if day >= term_day:
                    # 在当前节气之后，使用当前月支
                    return branch
                else:
                    # 在当前节气之前，使用上一个月的月支
                    prev_index = (i - 1) % 12
                    _, _, _, prev_branch = cls.SOLAR_TERMS[prev_index]
                    return prev_branch
        
        # 默认返回寅月（不应该执行到这里）
        return '寅'
    
    @classmethod
    def get_year_pillar(cls, year: int) -> str:
        """计算年柱"""
        stem_index = (year - 4) % 10
        branch_index = (year - 4) % 12
        return cls.HEAVENLY_STEMS[stem_index] + cls.EARTHLY_BRANCHES[branch_index]
    
    @classmethod
    def get_month_pillar(cls, year: int, month: int, day: int) -> str:
        """计算月柱"""
        # 获取年干
        year_stem = cls.get_year_pillar(year)[0]
        
        # 获取月支（根据节气）
        month_branch = cls.get_month_branch(month, day)
        
        # 五虎遁：根据年干确定月干
        month_stem_rules = {
            '甲': '丙', '己': '丙',  # 甲己之年丙作首
            '乙': '戊', '庚': '戊',  # 乙庚之岁戊为头
            '丙': '庚', '辛': '庚',  # 丙辛必定寻庚起
            '丁': '壬', '壬': '壬',  # 丁壬壬位顺行流
            '戊': '甲', '癸': '甲',  # 若问戊癸何方发，甲寅之上好追求
        }
        
        # 月支顺序（从寅月开始）
        branch_order = ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑']
        
        # 找到月支在顺序中的位置
        branch_index = branch_order.index(month_branch)
        
        # 获取起始天干
        start_stem = month_stem_rules[year_stem]
        start_index = cls.HEAVENLY_STEMS.index(start_stem)
        
        # 计算月干
        month_stem_index = (start_index + branch_index) % 10
        month_stem = cls.HEAVENLY_STEMS[month_stem_index]
        
        return month_stem + month_branch
    
    @classmethod
    def get_day_pillar(cls, year: int, month: int, day: int) -> str:
        """计算日柱（精确公式）"""
        # 日干支计算公式（适用于1900-2099年）
        
        # 调整年份和月份
        y = year % 100
        m = month
        
        if month <= 2:
            y = (year - 1) % 100
            m = month + 12
        
        # 世纪常数（1900-1999年为6，2000-2099为0）
        C = 0 if year >= 2000 else 6
        
        # 月基数表（调整后的月份）
        M_table = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]
        M = M_table[m - 1]
        
        # 闰年判断
        is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        if is_leap and m > 2:
            M += 1
        
        # 计算日干支序数
        S = (y + 7) * 5 + 15 + (y + 19) // 4 + M + day + C
        
        # 取模得到干支序数（1-60）
        G = S % 60
        if G == 0:
            G = 60
        
        # 转换为天干地支
        stem_index = (G - 1) % 10
        branch_index = (G - 1) % 12
        
        return cls.HEAVENLY_STEMS[stem_index] + cls.EARTHLY_BRANCHES[branch_index]
    
    @classmethod
    def get_hour_pillar(cls, day_stem: str, hour: int) -> str:
        """计算时柱"""
        # 时辰地支（23-1点为子时，1-3点为丑时，以此类推）
        hour_branch_index = ((hour + 1) // 2) % 12
        hour_branch = cls.EARTHLY_BRANCHES[hour_branch_index]
        
        # 五鼠遁：根据日干确定时干
        hour_stem_rules = {
            '甲': '甲', '己': '甲',  # 甲己还加甲
            '乙': '丙', '庚': '丙',  # 乙庚丙作初
            '丙': '戊', '辛': '戊',  # 丙辛从戊起
            '丁': '庚', '壬': '庚',  # 丁壬庚子居
            '戊': '壬', '癸': '壬',  # 戊癸何方发，壬子是真途
        }
        
        # 获取起始天干
        start_stem = hour_stem_rules[day_stem]
        start_index = cls.HEAVENLY_STEMS.index(start_stem)
        
        # 计算时干
        hour_stem_index = (start_index + hour_branch_index) % 10
        hour_stem = cls.HEAVENLY_STEMS[hour_stem_index]
        
        return hour_stem + hour_branch
    
    @classmethod
    def calculate_bazi(cls, year: int, month: int, day: int, hour: int) -> Dict:
        """计算八字四柱"""
        try:
            # 年柱
            year_pillar = cls.get_year_pillar(year)
            
            # 月柱
            month_pillar = cls.get_month_pillar(year, month, day)
            
            # 日柱
            day_pillar = cls.get_day_pillar(year, month, day)
            day_stem = day_pillar[0]
            
            # 时柱
            hour_pillar = cls.get_hour_pillar(day_stem, hour)
            
            # 完整八字
            full_bazi = f"{year_pillar} {month_pillar} {day_pillar} {hour_pillar}"
            
            # 统计五行
            elements = {'金': 0, '木': 0, '水': 0, '火': 0, '土': 0}
            
            # 分析八字中的五行
            pillars = [year_pillar, month_pillar, day_pillar, hour_pillar]
            for pillar in pillars:
                stem = pillar[0]
                branch = pillar[1]
                
                # 天干五行
                if stem in cls.STEM_ELEMENTS:
                    elements[cls.STEM_ELEMENTS[stem]] += 1
                
                # 地支五行
                if branch in cls.BRANCH_ELEMENTS:
                    elements[cls.BRANCH_ELEMENTS[branch]] += 1
            
            return {
                "year_pillar": year_pillar,
                "month_pillar": month_pillar,
                "day_pillar": day_pillar,
                "hour_pillar": hour_pillar,
                "full_bazi": full_bazi,
                "elements": elements,
                "day_master": {
                    "stem": day_stem,
                    "element": cls.STEM_ELEMENTS.get(day_stem, '未知'),
                    "personality": cls.DAY_MASTER_PERSONALITY.get(day_stem, '性格温和'),
                    "yinyang": "阳" if cls.HEAVENLY_STEMS.index(day_stem) % 2 == 0 else "阴"
                }
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "full_bazi": "计算错误"
            }

def calculate_bazi_accurate(birth_date: str, birth_time: str, gender: str) -> dict:
    """准确的八字计算函数（API兼容接口）"""
    from datetime import datetime
    
    # 解析日期时间
    dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    
    # 计算八字
    bazi_result = AccurateBaziCalculator.calculate_bazi(year, month, day, hour)
    
    if "error" in bazi_result:
        return bazi_result
    
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
    
    # 生肖
    chinese_zodiacs = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
    zodiac_index = (year - 4) % 12
    
    # 构建完整结果
    result = {
        "bazi": {
            "year_pillar": bazi_result["year_pillar"],
            "month_pillar": bazi_result["month_pillar"],
            "day_pillar": bazi_result["day_pillar"],
            "hour_pillar": bazi_result["hour_pillar"],
            "full_bazi": bazi_result["full_bazi"]
        },
        "elements": bazi_result["elements"],
        "day_master": bazi_result["day_master"],
        "fortune": {
            "year": bazi_result["year_pillar"],
            "analysis": fortunes[fortune_index],
            "suggestions": [
                "保持积极心态，面对挑战",
                "注意身体健康，合理作息",
                "多与贵人交流，拓展人脉",
                "把握投资机会，但需谨慎"
            ]
        },
        "basic_info": {
            "solar_date": f"{year}-{month:02d}-{day:02d}",
            "solar_time": f"{hour:02d}:{dt.minute:02d}",
            "gender": gender,
            "age": datetime.now().year - year,
            "chinese_zodiac": chinese_zodiacs[zodiac_index],
            "element": AccurateBaziCalculator.STEM_ELEMENTS.get(bazi_result["year_pillar"][0], '未知')
        }
    }
    
    return result

# 测试函数
def test():
    """测试函数"""
    test_cases = [
        ("2020-09-23", "22:38", "male", "庚子 乙酉 己巳 乙亥"),
        ("1990-01-15", "08:30", "male", "庚午 乙卯 辛未 丙申"),
        ("2000-05-20", "14:00", "female", "庚辰 辛巳 戊寅 己未"),
    ]
    
    print("八字计算测试")
    print("=" * 60)
    
    for birth_date, birth_time, gender, expected in test_cases:
        print(f"\n测试: {birth_date} {birth_time} {gender}")
        result = calculate_bazi_accurate(birth_date, birth_time, gender)
        
        if "error" in result:
            print(f"❌ 错误: {result['error']}")
            continue
        
        full_bazi = result["bazi"]["full_bazi"]
        print(f"计算结果: {full_bazi}")
        print(f"预期结果: {expected}")
        
        if full_bazi == expected:
            print("✅ 正确！")
        else:
            print("❌ 错误！")

if __name__ == "__main__":
    test()