"""
八字运势详细分析模块
提供更详细的运势分析和建议
"""

from datetime import datetime
from typing import Dict, List, Tuple

class FortuneAnalyzer:
    """八字运势详细分析器"""
    
    def __init__(self):
        self.fortune_levels = {
            "大吉": {
                "score": 90,
                "color": "#4CAF50",
                "description": "运势极佳，诸事顺利"
            },
            "吉": {
                "score": 75,
                "color": "#8BC34A",
                "description": "运势良好，积极进取"
            },
            "中平": {
                "score": 60,
                "color": "#FFC107",
                "description": "运势平稳，稳中求进"
            },
            "小凶": {
                "score": 45,
                "color": "#FF9800",
                "description": "略有阻碍，谨慎行事"
            },
            "大凶": {
                "score": 30,
                "color": "#F44336",
                "description": "运势不佳，保守为宜"
            }
        }
        
        self.element_names = {
            "金": "Metal",
            "木": "Wood",
            "水": "Water",
            "火": "Fire",
            "土": "Earth"
        }
        
        self.element_relations = {
            "相生": ["木→火", "火→土", "土→金", "金→水", "水→木"],
            "相克": ["木→土", "土→水", "水→火", "火→金", "金→木"]
        }
    
    def analyze_detailed_fortune(self, bazi_data: Dict, elements: Dict) -> Dict:
        """
        详细分析八字运势
        
        Args:
            bazi_data: 八字数据
            elements: 五行元素数据
            
        Returns:
            详细运势分析结果
        """
        # 计算五行平衡度
        balance_score = self._calculate_balance_score(elements)
        
        # 分析日主强弱
        day_master_strength = self._analyze_day_master_strength(bazi_data, elements)
        
        # 分析十神关系
        ten_gods = self._analyze_ten_gods(bazi_data)
        
        # 分析流年运势
        year_fortune = self._analyze_year_fortune(bazi_data)
        
        # 生成详细建议
        suggestions = self._generate_suggestions(balance_score, day_master_strength, ten_gods)
        
        # 计算综合运势等级
        overall_score = self._calculate_overall_score(balance_score, day_master_strength)
        fortune_level = self._get_fortune_level(overall_score)
        
        return {
            "overall_fortune": {
                "level": fortune_level,
                "score": overall_score,
                "description": self.fortune_levels[fortune_level]["description"],
                "color": self.fortune_levels[fortune_level]["color"]
            },
            "element_analysis": {
                "balance_score": balance_score,
                "elements": elements,
                "element_names": self.element_names,
                "relations": self.element_relations,
                "imbalance": self._find_imbalanced_elements(elements)
            },
            "day_master_analysis": day_master_strength,
            "ten_gods_analysis": ten_gods,
            "year_fortune": year_fortune,
            "detailed_suggestions": suggestions,
            "lucky_directions": self._get_lucky_directions(bazi_data),
            "lucky_colors": self._get_lucky_colors(elements),
            "lucky_numbers": self._get_lucky_numbers(bazi_data)
        }
    
    def _calculate_balance_score(self, elements: Dict) -> float:
        """计算五行平衡度得分"""
        total = sum(elements.values())
        if total == 0:
            return 0
        
        # 计算标准差（越小越平衡）
        mean = total / 5
        variance = sum((count - mean) ** 2 for count in elements.values()) / 5
        std_dev = variance ** 0.5
        
        # 转换为0-100的分数（越高越平衡）
        max_std_dev = total * 0.4  # 假设最大不平衡度
        balance_score = max(0, 100 - (std_dev / max_std_dev * 100))
        
        return round(balance_score, 2)
    
    def _analyze_day_master_strength(self, bazi_data: Dict, elements: Dict) -> Dict:
        """分析日主强弱"""
        day_master_element = bazi_data.get("day_master", {}).get("element", "金")
        day_master_count = elements.get(day_master_element, 0)
        
        # 计算日主在八字中的比例
        total_elements = sum(elements.values())
        percentage = (day_master_count / total_elements * 100) if total_elements > 0 else 0
        
        # 判断强弱
        if percentage >= 40:
            strength = "强"
            strength_desc = "日主得令，精力充沛"
        elif percentage >= 20:
            strength = "中"
            strength_desc = "日主适中，状态平稳"
        else:
            strength = "弱"
            strength_desc = "日主偏弱，需要扶助"
        
        return {
            "element": day_master_element,
            "count": day_master_count,
            "percentage": round(percentage, 2),
            "strength": strength,
            "description": strength_desc
        }
    
    def _analyze_ten_gods(self, bazi_data: Dict) -> List[Dict]:
        """分析十神关系"""
        # 简化的十神分析
        pillars = [
            {"position": "年柱", "pillar": bazi_data.get("year_pillar", "")},
            {"position": "月柱", "pillar": bazi_data.get("month_pillar", "")},
            {"position": "日柱", "pillar": bazi_data.get("day_pillar", "")},
            {"position": "时柱", "pillar": bazi_data.get("hour_pillar", "")}
        ]
        
        ten_gods = []
        for pillar in pillars:
            if pillar["pillar"]:
                ten_gods.append({
                    "position": pillar["position"],
                    "pillar": pillar["pillar"],
                    "relation": self._get_ten_god_relation(pillar["pillar"])
                })
        
        return ten_gods
    
    def _get_ten_god_relation(self, pillar: str) -> str:
        """获取十神关系（简化版）"""
        if not pillar or len(pillar) < 2:
            return "未知"
        
        # 简化的十神关系判断
        ten_god_map = {
            "甲": {"甲": "比肩", "乙": "劫财", "丙": "食神", "丁": "伤官", "戊": "偏财", "己": "正财", "庚": "七杀", "辛": "正官", "壬": "偏印", "癸": "正印"},
            "乙": {"甲": "劫财", "乙": "比肩", "丙": "伤官", "丁": "食神", "戊": "正财", "己": "偏财", "庚": "正官", "辛": "七杀", "壬": "正印", "癸": "偏印"},
            # 其他天干的映射可以继续添加
        }
        
        return ten_god_map.get(pillar[0], {}).get(pillar[1], "未知")
    
    def _analyze_year_fortune(self, bazi_data: Dict) -> Dict:
        """分析流年运势"""
        current_year = datetime.now().year
        year_stem_branch = self._get_year_stem_branch(current_year)
        
        return {
            "current_year": current_year,
            "year_pillar": year_stem_branch,
            "fortune": "平稳发展",
            "advice": "稳扎稳打，积累实力"
        }
    
    def _get_year_stem_branch(self, year: int) -> str:
        """根据年份获取天干地支"""
        # 简化的年份天干地支计算
        stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        stem_index = (year - 4) % 10
        branch_index = (year - 4) % 12
        
        return stems[stem_index] + branches[branch_index]
    
    def _generate_suggestions(self, balance_score: float, day_master_strength: Dict, ten_gods: List[Dict]) -> List[str]:
        """生成详细建议"""
        suggestions = []
        
        # 基于五行平衡的建议
        if balance_score >= 80:
            suggestions.append("五行平衡良好，继续保持当前的生活和工作节奏。")
        elif balance_score >= 60:
            suggestions.append("五行基本平衡，注意保持生活规律，避免极端。")
        else:
            suggestions.append("五行略有失衡，建议通过饮食、颜色、方位等方式进行调整。")
        
        # 基于日主强弱的建议
        if day_master_strength.get("strength") == "强":
            suggestions.append("日主强旺，适合主动进取，把握机会。")
        elif day_master_strength.get("strength") == "弱":
            suggestions.append("日主偏弱，宜保守行事，寻求贵人相助。")
        else:
            suggestions.append("日主适中，稳中求进，平衡发展。")
        
        # 通用建议
        suggestions.append("保持积极心态，注重身心健康。")
        suggestions.append("多行善事，积累福报。")
        suggestions.append("把握时机，顺势而为。")
        
        return suggestions
    
    def _find_imbalanced_elements(self, elements: Dict) -> List[str]:
        """找出不平衡的五行元素"""
        total = sum(elements.values())
        if total == 0:
            return []
        
        avg = total / 5
        imbalanced = []
        
        for element, count in elements.items():
            if count == 0:
                imbalanced.append(f"{element}元素缺失")
            elif count < avg * 0.5:
                imbalanced.append(f"{element}元素偏弱")
            elif count > avg * 1.5:
                imbalanced.append(f"{element}元素过旺")
        
        return imbalanced
    
    def _get_lucky_directions(self, bazi_data: Dict) -> List[str]:
        """获取吉利方位"""
        day_master_element = bazi_data.get("day_master", {}).get("element", "金")
        
        direction_map = {
            "金": ["西", "西北"],
            "木": ["东", "东南"],
            "水": ["北"],
            "火": ["南"],
            "土": ["中", "西南", "东北"]
        }
        
        return direction_map.get(day_master_element, ["各个方向"])
    
    def _get_lucky_colors(self, elements: Dict) -> List[str]:
        """获取吉利颜色"""
        # 根据五行生克关系推荐颜色
        colors = []
        
        if elements.get("金", 0) < 2:
            colors.append("白色、金色、银色")
        if elements.get("木", 0) < 2:
            colors.append("绿色、青色")
        if elements.get("水", 0) < 2:
            colors.append("黑色、蓝色")
        if elements.get("火", 0) < 2:
            colors.append("红色、紫色")
        if elements.get("土", 0) < 2:
            colors.append("黄色、棕色")
        
        if not colors:
            colors = ["根据五行平衡，各种颜色均可"]
        
        return colors
    
    def _get_lucky_numbers(self, bazi_data: Dict) -> List[int]:
        """获取幸运数字"""
        day_master_element = bazi_data.get("day_master", {}).get("element", "金")
        
        number_map = {
            "金": [4, 9],
            "木": [3, 8],
            "水": [1, 6],
            "火": [2, 7],
            "土": [5, 0]
        }
        
        return number_map.get(day_master_element, [1, 2, 3, 4, 5])
    
    def _calculate_overall_score(self, balance_score: float, day_master_strength: Dict) -> float:
        """计算综合运势得分"""
        # 五行平衡占60%，日主强弱占40%
        balance_weight = 0.6
        strength_weight = 0.4
        
        # 日主强弱评分
        strength_score_map = {"强": 85, "中": 70, "弱": 55}
        strength_score = strength_score_map.get(day_master_strength.get("strength", "中"), 70)
        
        overall_score = balance_score * balance_weight + strength_score * strength_weight
        return round(overall_score, 2)
    
    def _get_fortune_level(self, score: float) -> str:
        """根据得分获取运势等级"""
        if score >= 85:
            return "大吉"
        elif score >= 70:
            return "吉"
        elif score >= 55:
            return "中平"
        elif score >= 40:
            return "小凶"
        else:
            return "大凶"


# 使用示例
if __name__ == "__main__":
    analyzer = FortuneAnalyzer()
    
    # 示例数据
    bazi_data = {
        "year_pillar": "庚午",
        "month_pillar": "乙卯",
        "day_pillar": "辛未",
        "hour_pillar": "丙申",
        "day_master": {
            "stem": "辛",
            "element": "金",
            "yinyang": "阴",
            "personality": "细致、敏锐、有才华"
        }
    }
    
    elements = {
        "金": 3,
        "木": 2,
        "水": 0,
        "火": 2,
        "土": 1
    }
    
    result = analyzer.analyze_detailed_fortune(bazi_data, elements)
    print("详细运势分析结果:")
    print(result)