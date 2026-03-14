"""
八字用神分析模块
根据五行平衡、日主强弱、格局喜忌分析用神
"""

from typing import Dict, List, Tuple, Optional

class BaziYongshenAnalyzer:
    """八字用神分析器"""
    
    # 天干五行
    STEM_ELEMENTS = {
        '甲': '木', '乙': '木',
        '丙': '火', '丁': '火',
        '戊': '土', '己': '土',
        '庚': '金', '辛': '金',
        '壬': '水', '癸': '水'
    }
    
    # 地支五行
    BRANCH_ELEMENTS = {
        '子': '水', '亥': '水',
        '寅': '木', '卯': '木',
        '巳': '火', '午': '火',
        '申': '金', '酉': '金',
        '辰': '土', '戌': '土', '丑': '土', '未': '土'
    }
    
    # 地支藏干（简化版）
    BRANCH_HIDDEN_STEMS = {
        '子': ['癸'],
        '丑': ['己', '癸', '辛'],
        '寅': ['甲', '丙', '戊'],
        '卯': ['乙'],
        '辰': ['戊', '乙', '癸'],
        '巳': ['丙', '戊', '庚'],
        '午': ['丁', '己'],
        '未': ['己', '丁', '乙'],
        '申': ['庚', '壬', '戊'],
        '酉': ['辛'],
        '戌': ['戊', '辛', '丁'],
        '亥': ['壬', '甲']
    }
    
    # 季节五行
    SEASON_ELEMENTS = {
        '寅': '木', '卯': '木', '辰': '土',  # 春季
        '巳': '火', '午': '火', '未': '土',  # 夏季
        '申': '金', '酉': '金', '戌': '土',  # 秋季
        '亥': '水', '子': '水', '丑': '土',  # 冬季
    }
    
    # 日主强弱判断规则
    DAY_MASTER_STRENGTH_RULES = {
        '木': {'旺': ['寅', '卯', '亥', '子'], '衰': ['申', '酉', '巳', '午']},
        '火': {'旺': ['巳', '午', '寅', '卯'], '衰': ['亥', '子', '申', '酉']},
        '土': {'旺': ['辰', '戌', '丑', '未'], '衰': ['寅', '卯', '申', '酉']},
        '金': {'旺': ['申', '酉', '辰', '戌'], '衰': ['巳', '午', '寅', '卯']},
        '水': {'旺': ['亥', '子', '申', '酉'], '衰': ['辰', '戌', '丑', '未']}
    }
    
    @classmethod
    def analyze_yongshen(cls, bazi_data: Dict) -> Dict:
        """
        分析八字用神
        Args:
            bazi_data: 八字数据，包含四柱和五行信息
        Returns:
            用神分析结果
        """
        try:
            # 提取八字四柱
            year_pillar = bazi_data.get('bazi', {}).get('year_pillar', '')
            month_pillar = bazi_data.get('bazi', {}).get('month_pillar', '')
            day_pillar = bazi_data.get('bazi', {}).get('day_pillar', '')
            hour_pillar = bazi_data.get('bazi', {}).get('hour_pillar', '')
            
            if not all([year_pillar, month_pillar, day_pillar, hour_pillar]):
                return {"error": "八字数据不完整"}
            
            # 日主信息
            day_master = bazi_data.get('day_master', {})
            day_stem = day_master.get('stem', '')
            day_element = day_master.get('element', '')
            
            if not day_stem or not day_element:
                return {"error": "日主信息缺失"}
            
            # 1. 五行统计（包含藏干）
            elements_count = cls._count_elements_with_hidden(year_pillar, month_pillar, day_pillar, hour_pillar)
            
            # 2. 日主强弱分析
            strength_analysis = cls._analyze_day_master_strength(day_stem, day_element, elements_count)
            
            # 3. 格局判断
            pattern = cls._determine_pattern(strength_analysis, elements_count)
            
            # 4. 用神选择
            yongshen_analysis = cls._select_yongshen(day_element, pattern, elements_count, month_pillar[1])
            
            # 5. 调候分析
            tiaohou_analysis = cls._analyze_tiaohou(day_element, month_pillar[1])
            
            # 6. 综合分析
            comprehensive_analysis = cls._comprehensive_analysis(
                day_stem, day_element, pattern, yongshen_analysis, tiaohou_analysis
            )
            
            return {
                "success": True,
                "elements_count": elements_count,
                "strength_analysis": strength_analysis,
                "pattern": pattern,
                "yongshen": yongshen_analysis,
                "tiaohou": tiaohou_analysis,
                "comprehensive": comprehensive_analysis,
                "recommendations": cls._generate_recommendations(yongshen_analysis, tiaohou_analysis)
            }
            
        except Exception as e:
            return {"error": f"用神分析失败: {str(e)}"}
    
    @classmethod
    def _count_elements_with_hidden(cls, year: str, month: str, day: str, hour: str) -> Dict[str, int]:
        """统计五行数量（包含地支藏干）"""
        elements = {'金': 0, '木': 0, '水': 0, '火': 0, '土': 0}
        
        pillars = [year, month, day, hour]
        
        for pillar in pillars:
            if len(pillar) != 2:
                continue
            
            stem = pillar[0]
            branch = pillar[1]
            
            # 天干五行
            if stem in cls.STEM_ELEMENTS:
                elements[cls.STEM_ELEMENTS[stem]] += 1
            
            # 地支本气五行
            if branch in cls.BRANCH_ELEMENTS:
                elements[cls.BRANCH_ELEMENTS[branch]] += 1
            
            # 地支藏干五行
            if branch in cls.BRANCH_HIDDEN_STEMS:
                for hidden_stem in cls.BRANCH_HIDDEN_STEMS[branch]:
                    if hidden_stem in cls.STEM_ELEMENTS:
                        elements[cls.STEM_ELEMENTS[hidden_stem]] += 0.3  # 藏干权重较低
        
        # 转换为整数（四舍五入）
        for element in elements:
            elements[element] = round(elements[element])
        
        return elements
    
    @classmethod
    def _analyze_day_master_strength(cls, day_stem: str, day_element: str, elements_count: Dict[str, int]) -> Dict:
        """分析日主强弱"""
        # 1. 五行数量对比
        same_element = elements_count.get(day_element, 0)
        total_elements = sum(elements_count.values())
        
        # 2. 生扶关系
        support_elements = 0
        suppress_elements = 0
        
        # 五行相生关系
        generate_map = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
        overcome_map = {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}
        
        # 生我者为印，我生者为食伤
        for element, count in elements_count.items():
            if element == day_element:
                continue
            if generate_map.get(element) == day_element:  # 生我者
                support_elements += count
            elif overcome_map.get(day_element) == element:  # 我克者（耗我）
                suppress_elements += count * 0.5
            elif overcome_map.get(element) == day_element:  # 克我者
                suppress_elements += count
        
        # 3. 强弱判断
        strength_score = same_element + support_elements - suppress_elements
        average = total_elements / 5  # 平均每行应有数量
        
        if strength_score > average * 1.5:
            strength = "身强"
        elif strength_score < average * 0.5:
            strength = "身弱"
        else:
            strength = "中和"
        
        return {
            "day_stem": day_stem,
            "day_element": day_element,
            "same_element_count": same_element,
            "support_count": support_elements,
            "suppress_count": suppress_elements,
            "strength_score": round(strength_score, 2),
            "strength": strength,
            "analysis": cls._get_strength_analysis(strength, day_element)
        }
    
    @classmethod
    def _get_strength_analysis(cls, strength: str, day_element: str) -> str:
        """获取日主强弱分析"""
        analyses = {
            "身强": {
                '木': '日主木旺，如参天大树，有担当但易固执',
                '火': '日主火旺，如太阳当空，热情但易急躁',
                '土': '日主土旺，如高山厚土，稳重但易保守',
                '金': '日主金旺，如宝剑锋刃，刚毅但易锋利',
                '水': '日主水旺，如江河奔流，智慧但易多变'
            },
            "身弱": {
                '木': '日主木弱，如小草初生，需水木滋养',
                '火': '日主火弱，如烛火摇曳，需木火生扶',
                '土': '日主土弱，如沙土松散，需火土帮扶',
                '金': '日主金弱，如薄金易折，需土金相助',
                '水': '日主水弱，如浅溪细流，需金水相生'
            },
            "中和": {
                '木': '日主木中和，如青松挺拔，刚柔并济',
                '火': '日主火中和，如炉火温暖，热情适度',
                '土': '日主土中和，如大地承载，厚德载物',
                '金': '日主金中和，如金石兼修，刚柔相济',
                '水': '日主水中和，如清泉流淌，智慧通达'
            }
        }
        
        return analyses.get(strength, {}).get(day_element, "日主力量平衡")
    
    @classmethod
    def _determine_pattern(cls, strength_analysis: Dict, elements_count: Dict[str, int]) -> Dict:
        """判断格局"""
        strength = strength_analysis.get("strength", "中和")
        day_element = strength_analysis.get("day_element", "")
        
        # 特殊格局判断（简化版）
        pattern = "普通格局"
        pattern_detail = ""
        
        if strength == "身强":
            # 检查是否从强格
            same_count = elements_count.get(day_element, 0)
            total = sum(elements_count.values())
            
            if same_count >= total * 0.7:  # 同五行占比超过70%
                pattern = "从强格"
                pattern_detail = f"日主{day_element}极旺，宜顺其势"
            else:
                pattern = "身强格"
                pattern_detail = "日主偏旺，宜克泄耗"
        
        elif strength == "身弱":
            # 检查是否从弱格
            suppress_count = 0
            total = sum(elements_count.values())
            
            # 计算克泄耗的力量
            for element, count in elements_count.items():
                if element != day_element:
                    suppress_count += count
            
            if suppress_count >= total * 0.7:  # 克泄耗力量超过70%
                pattern = "从弱格"
                pattern_detail = f"日主{day_element}极弱，宜从其势"
            else:
                pattern = "身弱格"
                pattern_detail = "日主偏弱，宜生扶"
        
        else:  # 中和
            pattern = "中和格"
            pattern_detail = "五行相对平衡，流通为佳"
        
        return {
            "pattern": pattern,
            "detail": pattern_detail,
            "recommendation": cls._get_pattern_recommendation(pattern, day_element)
        }
    
    @classmethod
    def _get_pattern_recommendation(cls, pattern: str, day_element: str) -> str:
        """获取格局建议"""
        recommendations = {
            "身强格": "宜用克、泄、耗的五行来平衡",
            "身弱格": "宜用生、扶、助的五行来补益",
            "从强格": "宜顺其旺势，用生扶的五行",
            "从弱格": "宜从其弱势，用克泄耗的五行",
            "中和格": "五行平衡，流通顺畅为佳",
            "普通格局": "根据具体五行配置选择用神"
        }
        return recommendations.get(pattern, "根据具体分析选择用神")
    
    @classmethod
    def _select_yongshen(cls, day_element: str, pattern: Dict, elements_count: Dict[str, int], month_branch: str) -> Dict:
        """选择用神"""
        pattern_type = pattern.get("pattern", "")
        
        # 五行相生相克关系
        generate_map = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
        overcome_map = {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}
        generated_by_map = {'木': '水', '火': '木', '土': '火', '金': '土', '水': '金'}
        
        yongshen_elements = []
        jishen_elements = []
        analysis = ""
        
        if pattern_type in ["身强格", "从强格"]:
            # 身强宜克泄耗
            # 1. 克：官杀（克我者）
            if overcome_map.get(day_element):
                yongshen_elements.append(overcome_map[day_element])
                analysis += f"用{overcome_map[day_element]}（官杀）克制日主{day_element}。"
            
            # 2. 泄：食伤（我生者）
            if generate_map.get(day_element):
                yongshen_elements.append(generate_map[day_element])
                analysis += f"用{generate_map[day_element]}（食伤）泄日主{day_element}之气。"
            
            # 3. 耗：财星（我克者）
            # 注意：我克者为财，但身强才能担财
            # 这里简化处理
            
            # 忌神：生扶日主的五行
            jishen_elements.append(day_element)  # 比劫
            if generated_by_map.get(day_element):
                jishen_elements.append(generated_by_map[day_element])  # 印星
        
        elif pattern_type in ["身弱格", "从弱格"]:
            # 身弱宜生扶
            # 1. 生：印星（生我者）
            if generated_by_map.get(day_element):
                yongshen_elements.append(generated_by_map[day_element])
                analysis += f"用{generated_by_map[day_element]}（印星）生扶日主{day_element}。"
            
            # 2. 扶：比劫（同我者）
            yongshen_elements.append(day_element)
            analysis += f"用{day_element}（比劫）帮扶日主。"
            
            # 忌神：克泄耗日主的五行
            if overcome_map.get(day_element):
                jishen_elements.append(overcome_map[day_element])  # 官杀
            if generate_map.get(day_element):
                jishen_elements.append(generate_map[day_element])  # 食伤
        
        else:  # 中和格
            # 中和宜流通
            # 找出最弱的五行作为用神
            min_element = min(elements_count.items(), key=lambda x: x[1])
            yongshen_elements.append(min_element[0])
            analysis += f"五行相对平衡，宜补益最弱的{min_element[0]}行。"
            
            # 找出最强的五行作为忌神
            max_element = max(elements_count.items(), key=lambda x: x[1])
            if max_element[0] != min_element[0]:
                jishen_elements.append(max_element[0])
        
        # 去重
        yongshen_elements = list(set(yongshen_elements))
        jishen_elements = list(set(jishen_elements))
        
        # 根据季节调候（优先级调整）
        yongshen_elements = cls._adjust_by_season(yongshen_elements, month_branch, day_element)
        
        return {
            "yongshen": yongshen_elements,
            "jishen": jishen_elements,
            "analysis": analysis,
            "priority": cls._get_yongshen_priority(yongshen_elements, day_element)
        }
    
    @classmethod
    def _adjust_by_season(cls, yongshen_elements: List[str], month_branch: str, day_element: str) -> List[str]:
        """根据季节调候调整用神"""
        if month_branch not in cls.SEASON_ELEMENTS:
            return yongshen_elements
        
        season_element = cls.SEASON_ELEMENTS[month_branch]
        
        # 调候原则：寒则温之，热则凉之，燥则润之，湿则燥之
        tiaohou_map = {
            # 春季（木旺）：需要金来修剪，需要火来温暖
            '木': ['金', '火'],
            # 夏季（火旺）：需要水来降温，需要金来生水
            '火': ['水', '金'],
            # 秋季（金旺）：需要火来炼金，需要木来生火
            '金': ['火', '木'],
            # 冬季（水旺）：需要火来温暖，需要土来制水
            '水': ['火', '土'],
            # 四季土（土旺）：需要木来疏土，需要金来泄土
            '土': ['木', '金']
        }
        
        tiaohou_elements = tiaohou_map.get(season_element, [])
        
        # 如果调候用神不在原用神中，且不与日主冲突，则添加
        adjusted = yongshen_elements.copy()
        for element in tiaohou_elements:
            if element not in adjusted:
                # 检查是否与日主相克（简化判断）
                if element != day_element:  # 这里简化，实际需要更复杂的判断
                    adjusted.append(element)
        
        return adjusted
    
    @classmethod
    def _get_yongshen_priority(cls, yongshen_elements: List[str], day_element: str) -> List[Dict]:
        """获取用神优先级"""
        priority_list = []
        
        for element in yongshen_elements:
            # 根据与日主的关系确定优先级
            if element == day_element:
                priority = 3  # 比劫：中等优先级
                relation = "比劫（帮扶）"
            elif cls._is_generate_to(element, day_element):
                priority = 1  # 印星：高优先级（生我）
                relation = "印星（生扶）"
            elif cls._is_generated_by(day_element, element):
                priority = 2  # 食伤：中等优先级（泄我）
                relation = "食伤（泄秀）"
            elif cls._is_overcome_by(element, day_element):
                priority = 2  # 财星：中等优先级（我克）
                relation = "财星（我克）"
            elif cls._is_overcome_to(element, day_element):
                priority = 4  # 官杀：低优先级（克我）
                relation = "官杀（克制）"
            else:
                priority = 5  # 其他：最低优先级
                relation = "调候"
            
            priority_list.append({
                "element": element,
                "priority": priority,
                "relation": relation,
                "description": cls._get_element_description(element)
            })
        
        # 按优先级排序
        priority_list.sort(key=lambda x: x["priority"])
        return priority_list
    
    @classmethod
    def _is_generate_to(cls, element1: str, element2: str) -> bool:
        """判断element1是否生element2"""
        generate_map = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
        return generate_map.get(element1) == element2
    
    @classmethod
    def _is_generated_by(cls, element1: str, element2: str) -> bool:
        """判断element1是否被element2生"""
        generate_map = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
        return generate_map.get(element2) == element1
    
    @classmethod
    def _is_overcome_to(cls, element1: str, element2: str) -> bool:
        """判断element1是否克element2"""
        overcome_map = {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}
        return overcome_map.get(element1) == element2
    
    @classmethod
    def _is_overcome_by(cls, element1: str, element2: str) -> bool:
        """判断element1是否被element2克"""
        overcome_map = {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}
        return overcome_map.get(element2) == element1
    
    @classmethod
    def _get_element_description(cls, element: str) -> str:
        """获取五行描述"""
        descriptions = {
            '金': '代表义气、果断、刚毅，主西方，白色，秋季',
            '木': '代表仁爱、生长、条达，主东方，青色，春季',
            '水': '代表智慧、流动、变化，主北方，黑色，冬季',
            '火': '代表礼仪、热情、光明，主南方，红色，夏季',
            '土': '代表诚信、包容、稳重，主中央，黄色，四季末'
        }
        return descriptions.get(element, "")
    
    @classmethod
    def _analyze_tiaohou(cls, day_element: str, month_branch: str) -> Dict:
        """调候分析"""
        if month_branch not in cls.SEASON_ELEMENTS:
            return {"analysis": "无法判断季节", "suggestions": []}
        
        season_element = cls.SEASON_ELEMENTS[month_branch]
        season_name = cls._get_season_name(month_branch)
        
        # 调候原则
        tiaohou_rules = {
            '木': {  # 春季
                'analysis': '春季木旺，需金修剪，需火温暖',
                'suggestions': ['宜用金制木', '宜用火暖局', '避免水过多']
            },
            '火': {  # 夏季
                'analysis': '夏季火旺，需水调候，需金生水',
                'suggestions': ['宜用水降温', '宜用金生水', '避免木过多']
            },
            '金': {  # 秋季
                'analysis': '秋季金旺，需火炼金，需木生火',
                'suggestions': ['宜用火炼金', '宜用木生火', '避免土过多']
            },
            '水': {  # 冬季
                'analysis': '冬季水寒，需火暖局，需土制水',
                'suggestions': ['宜用火暖局', '宜用土制水', '避免金过多']
            },
            '土': {  # 四季土
                'analysis': '土旺四季，需木疏土，需金泄土',
                'suggestions': ['宜用木疏土', '宜用金泄秀', '避免火过多']
            }
        }
        
        rule = tiaohou_rules.get(season_element, {"analysis": "", "suggestions": []})
        
        return {
            "season": season_name,
            "season_element": season_element,
            "analysis": rule["analysis"],
            "suggestions": rule["suggestions"]
        }
    
    @classmethod
    def _get_season_name(cls, month_branch: str) -> str:
        """获取季节名称"""
        season_map = {
            '寅': '春季正月', '卯': '春季二月', '辰': '春季三月',
            '巳': '夏季四月', '午': '夏季五月', '未': '夏季六月',
            '申': '秋季七月', '酉': '秋季八月', '戌': '秋季九月',
            '亥': '冬季十月', '子': '冬季十一月', '丑': '冬季十二月'
        }
        return season_map.get(month_branch, "未知季节")
    
    @classmethod
    def _comprehensive_analysis(cls, day_stem: str, day_element: str, pattern: Dict, 
                                yongshen: Dict, tiaohou: Dict) -> Dict:
        """综合分析"""
        yongshen_elements = yongshen.get("yongshen", [])
        jishen_elements = yongshen.get("jishen", [])
        
        # 生成综合分析
        analysis = f"日主{day_stem}({day_element})，{pattern.get('detail', '')}。"
        
        if yongshen_elements:
            analysis += f"喜用神为：{'、'.join(yongshen_elements)}。"
        
        if jishen_elements:
            analysis += f"忌神为：{'、'.join(jishen_elements)}。"
        
        analysis += f"生于{tiaohou.get('season', '')}，{tiaohou.get('analysis', '')}"
        
        return {
            "summary": analysis,
            "key_points": [
                f"日主：{day_stem}({day_element})",
                f"格局：{pattern.get('pattern', '')}",
                f"用神：{'、'.join(yongshen_elements) if yongshen_elements else '无'}",
                f"忌神：{'、'.join(jishen_elements) if jishen_elements else '无'}",
                f"调候：{tiaohou.get('analysis', '')}"
            ]
        }
    
    @classmethod
    def _generate_recommendations(cls, yongshen: Dict, tiaohou: Dict) -> List[str]:
        """生成建议"""
        recommendations = []
        
        # 用神建议
        yongshen_elements = yongshen.get("yongshen", [])
        if yongshen_elements:
            rec = f"宜加强{'、'.join(yongshen_elements)}五行能量"
            recommendations.append(rec)
        
        # 忌神建议
        jishen_elements = yongshen.get("jishen", [])
        if jishen_elements:
            rec = f"宜避免或减弱{'、'.join(jishen_elements)}五行影响"
            recommendations.append(rec)
        
        # 调候建议
        tiaohou_suggestions = tiaohou.get("suggestions", [])
        recommendations.extend(tiaohou_suggestions)
        
        # 通用建议
        recommendations.extend([
            "根据用神选择职业、方位、颜色等",
            "注意五行平衡，避免极端",
            "结合大运流年动态调整"
        ])
        
        return recommendations


# 测试函数
def test_yongshen():
    """测试用神分析"""
    print("八字用神分析测试")
    print("=" * 60)
    
    # 测试用例
    test_cases = [
        {
            "name": "1995-08-22 18:50 男",
            "bazi": {
                "year_pillar": "乙亥",
                "month_pillar": "甲申", 
                "day_pillar": "乙酉",
                "hour_pillar": "乙酉"
            },
            "day_master": {
                "stem": "乙",
                "element": "木"
            },
            "elements": {"金": 3, "木": 4, "水": 1, "火": 0, "土": 0}
        },
        {
            "name": "2020-09-23 22:38 男",
            "bazi": {
                "year_pillar": "庚子",
                "month_pillar": "乙酉",
                "day_pillar": "己巳",
                "hour_pillar": "乙亥"
            },
            "day_master": {
                "stem": "己",
                "element": "土"
            },
            "elements": {"金": 2, "木": 2, "水": 2, "火": 1, "土": 1}
        },
        {
            "name": "2024-03-13 16:00 男",
            "bazi": {
                "year_pillar": "甲辰",
                "month_pillar": "丁卯",
                "day_pillar": "丙子",
                "hour_pillar": "丙申"
            },
            "day_master": {
                "stem": "丙",
                "element": "火"
            },
            "elements": {"金": 1, "木": 2, "水": 2, "火": 2, "土": 1}
        }
    ]
    
    for case in test_cases:
        print(f"\n📊 测试: {case['name']}")
        print(f"八字: {case['bazi']['year_pillar']} {case['bazi']['month_pillar']} {case['bazi']['day_pillar']} {case['bazi']['hour_pillar']}")
        print(f"日主: {case['day_master']['stem']}({case['day_master']['element']})")
        print(f"五行: {case['elements']}")
        
        # 构建完整数据
        bazi_data = {
            "bazi": case["bazi"],
            "day_master": case["day_master"],
            "elements": case["elements"]
        }
        
        # 分析用神
        result = BaziYongshenAnalyzer.analyze_yongshen(bazi_data)
        
        if "error" in result:
            print(f"❌ 错误: {result['error']}")
            continue
        
        print(f"📈 日主强弱: {result['strength_analysis']['strength']}")
        print(f"   {result['strength_analysis']['analysis']}")
        
        print(f"🎭 格局: {result['pattern']['pattern']}")
        print(f"   {result['pattern']['detail']}")
        
        print(f"🌟 用神: {', '.join(result['yongshen']['yongshen'])}")
        print(f"   {result['yongshen']['analysis']}")
        
        print(f"❌ 忌神: {', '.join(result['yongshen']['jishen']) if result['yongshen']['jishen'] else '无'}")
        
        print(f"🌤️ 调候: {result['tiaohou']['season']} - {result['tiaohou']['analysis']}")
        
        print(f"📝 综合分析: {result['comprehensive']['summary']}")
        
        print(f"💡 建议:")
        for i, rec in enumerate(result['recommendations'], 1):
            print(f"   {i}. {rec}")
        
        print("-" * 60)

if __name__ == "__main__":
    test_yongshen()