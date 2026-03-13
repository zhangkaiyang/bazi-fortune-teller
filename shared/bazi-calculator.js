/**
 * 八字计算器核心模块
 * 作者：大黄
 * 日期：2026-03-13
 */

// 天干地支对照表
const HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
const EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];

// 五行对照表
const ELEMENTS = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火',
    '戊': '土', '己': '土', '庚': '金', '辛': '金',
    '壬': '水', '癸': '水',
    '子': '水', '丑': '土', '寅': '木', '卯': '木',
    '辰': '土', '巳': '火', '午': '火', '未': '土',
    '申': '金', '酉': '金', '戌': '土', '亥': '水'
};

// 十神关系
const TEN_GODS = {
    '比肩': '同我者为比肩',
    '劫财': '同我异性为劫财',
    '食神': '我生者为食神',
    '伤官': '我生异性为伤官',
    '偏财': '我克者为偏财',
    '正财': '我克异性为正财',
    '七杀': '克我者为七杀',
    '正官': '克我异性为正官',
    '偏印': '生我者为偏印',
    '正印': '生我异性为正印'
};

// 生肖对照
const ZODIAC_ANIMALS = {
    '子': '鼠', '丑': '牛', '寅': '虎', '卯': '兔',
    '辰': '龙', '巳': '蛇', '午': '马', '未': '羊',
    '申': '猴', '酉': '鸡', '戌': '狗', '亥': '猪'
};

class BaziCalculator {
    constructor() {
        // 初始化数据
        this.solarTerms = this.getSolarTerms();
    }

    /**
     * 计算八字
     * @param {Date} birthDate - 出生日期时间
     * @param {string} gender - 性别 ('male' 或 'female')
     * @param {boolean} useSolarTime - 是否使用真太阳时
     * @returns {Object} 八字结果
     */
    calculate(birthDate, gender = 'male', useSolarTime = true) {
        // 1. 转换为农历（简化版，实际需要复杂计算）
        const lunarDate = this.solarToLunar(birthDate);
        
        // 2. 计算年柱
        const yearPillar = this.getYearPillar(birthDate.getFullYear());
        
        // 3. 计算月柱
        const monthPillar = this.getMonthPillar(birthDate);
        
        // 4. 计算日柱（使用公式）
        const dayPillar = this.getDayPillar(birthDate);
        
        // 5. 计算时柱
        const hourPillar = this.getHourPillar(dayPillar.stem, birthDate.getHours());
        
        // 6. 计算五行
        const elements = this.analyzeElements(yearPillar, monthPillar, dayPillar, hourPillar);
        
        // 7. 计算十神
        const tenGods = this.analyzeTenGods(dayPillar.stem, [yearPillar, monthPillar, dayPillar, hourPillar]);
        
        // 8. 分析日主
        const dayMaster = this.analyzeDayMaster(dayPillar.stem);
        
        // 9. 计算当前运势
        const fortune = this.calculateFortune(birthDate, gender);
        
        return {
            basicInfo: {
                solarDate: birthDate.toISOString().split('T')[0],
                solarTime: birthDate.toTimeString().split(' ')[0].substring(0, 5),
                lunarDate: lunarDate,
                gender: gender,
                age: this.calculateAge(birthDate)
            },
            bazi: {
                year: yearPillar,
                month: monthPillar,
                day: dayPillar,
                hour: hourPillar,
                fullBazi: `${yearPillar.stem}${yearPillar.branch} ${monthPillar.stem}${monthPillar.branch} ${dayPillar.stem}${dayPillar.branch} ${hourPillar.stem}${hourPillar.branch}`
            },
            elements: elements,
            tenGods: tenGods,
            dayMaster: dayMaster,
            fortune: fortune,
            zodiac: this.getZodiac(yearPillar.branch)
        };
    }

    /**
     * 计算年柱（简化版）
     */
    getYearPillar(year) {
        // 实际算法复杂，这里简化处理
        const stemIndex = (year - 4) % 10;
        const branchIndex = (year - 4) % 12;
        return {
            stem: HEAVENLY_STEMS[stemIndex],
            branch: EARTHLY_BRANCHES[branchIndex],
            element: ELEMENTS[HEAVENLY_STEMS[stemIndex]]
        };
    }

    /**
     * 计算月柱（简化版）
     */
    getMonthPillar(date) {
        const month = date.getMonth() + 1; // 0-11 -> 1-12
        // 简化：正月为寅，二月为卯...
        const branchIndex = (month + 1) % 12;
        const stemIndex = this.calculateMonthStem(date.getFullYear(), month);
        
        return {
            stem: HEAVENLY_STEMS[stemIndex],
            branch: EARTHLY_BRANCHES[branchIndex],
            element: ELEMENTS[HEAVENLY_STEMS[stemIndex]]
        };
    }

    /**
     * 计算日柱（简化版，实际需要复杂公式）
     */
    getDayPillar(date) {
        // 简化算法，实际需要使用复杂公式
        const day = date.getDate();
        const stemIndex = day % 10;
        const branchIndex = day % 12;
        
        return {
            stem: HEAVENLY_STEMS[stemIndex],
            branch: EARTHLY_BRANCHES[branchIndex],
            element: ELEMENTS[HEAVENLY_STEMS[stemIndex]]
        };
    }

    /**
     * 计算时柱
     */
    getHourPillar(dayStem, hour) {
        // 时柱根据地支和日干计算
        const hourBranchIndex = Math.floor((hour + 1) / 2) % 12;
        const dayStemIndex = HEAVENLY_STEMS.indexOf(dayStem);
        const hourStemIndex = (dayStemIndex * 2 + hourBranchIndex) % 10;
        
        return {
            stem: HEAVENLY_STEMS[hourStemIndex],
            branch: EARTHLY_BRANCHES[hourBranchIndex],
            element: ELEMENTS[HEAVENLY_STEMS[hourStemIndex]]
        };
    }

    /**
     * 分析五行
     */
    analyzeElements(year, month, day, hour) {
        const elements = { '金': 0, '木': 0, '水': 0, '火': 0, '土': 0 };
        
        [year, month, day, hour].forEach(pillar => {
            elements[ELEMENTS[pillar.stem]]++;
            elements[ELEMENTS[pillar.branch]]++;
        });
        
        // 分析五行平衡
        const total = Object.values(elements).reduce((a, b) => a + b, 0);
        const percentages = {};
        Object.keys(elements).forEach(key => {
            percentages[key] = (elements[key] / total * 100).toFixed(1) + '%';
        });
        
        // 找出最强和最弱的五行
        const sorted = Object.entries(elements).sort((a, b) => b[1] - a[1]);
        const strongest = sorted[0][0];
        const weakest = sorted[sorted.length - 1][0];
        
        return {
            counts: elements,
            percentages: percentages,
            strongest: strongest,
            weakest: weakest,
            balance: this.getBalanceAdvice(elements)
        };
    }

    /**
     * 分析十神
     */
    analyzeTenGods(dayStem, pillars) {
        const dayStemIndex = HEAVENLY_STEMS.indexOf(dayStem);
        const results = [];
        
        pillars.forEach((pillar, index) => {
            const stemIndex = HEAVENLY_STEMS.indexOf(pillar.stem);
            const relation = this.getStemRelation(dayStemIndex, stemIndex);
            
            results.push({
                pillar: `${pillar.stem}${pillar.branch}`,
                position: ['年', '月', '日', '时'][index],
                relation: relation,
                meaning: TEN_GODS[relation] || '未知',
                element: ELEMENTS[pillar.stem]
            });
        });
        
        return results;
    }

    /**
     * 分析日主
     */
    analyzeDayMaster(dayStem) {
        const element = ELEMENTS[dayStem];
        const yinyang = HEAVENLY_STEMS.indexOf(dayStem) % 2 === 0 ? '阳' : '阴';
        
        const personalities = {
            '甲': { nature: '阳木', desc: '如参天大树，正直仁德，积极向上' },
            '乙': { nature: '阴木', desc: '如藤蔓花草，柔顺温和，适应力强' },
            '丙': { nature: '阳火', desc: '如太阳之火，热情开朗，光明磊落' },
            '丁': { nature: '阴火', desc: '如灯烛之火，文明礼仪，细心体贴' },
            '戊': { nature: '阳土', desc: '如城墙之土，诚实信用，稳重可靠' },
            '己': { nature: '阴土', desc: '如田园之土，温和包容，重视内涵' },
            '庚': { nature: '阳金', desc: '如斧钺之金，刚毅果断，重信守义' },
            '辛': { nature: '阴金', desc: '如珠宝之金，细腻敏感，追求完美' },
            '壬': { nature: '阳水', desc: '如江河之水，智慧灵活，适应变化' },
            '癸': { nature: '阴水', desc: '如雨露之水，温柔含蓄，善于谋划' }
        };
        
        return {
            stem: dayStem,
            element: element,
            yinyang: yinyang,
            ...personalities[dayStem]
        };
    }

    /**
     * 计算运势（简化版）
     */
    calculateFortune(birthDate, gender) {
        const currentYear = new Date().getFullYear();
        const age = currentYear - birthDate.getFullYear();
        
        // 简化的大运计算（每10年一运）
        const majorLuckIndex = Math.floor(age / 10) % 10;
        const majorLuck = HEAVENLY_STEMS[majorLuckIndex] + EARTHLY_BRANCHES[majorLuckIndex];
        
        // 流年
        const yearStemIndex = (currentYear - 4) % 10;
        const yearBranchIndex = (currentYear - 4) % 12;
        const currentYearPillar = HEAVENLY_STEMS[yearStemIndex] + EARTHLY_BRANCHES[yearBranchIndex];
        
        // 简单运势分析
        const fortunes = [
            "平稳发展，宜守不宜攻",
            "机遇来临，把握时机",
            "挑战增多，谨慎行事",
            "贵人相助，事业上升",
            "财运亨通，投资有利",
            "健康需注意，劳逸结合",
            "感情顺利，人际关系和谐",
            "学习进步，技能提升",
            "变动较多，适应变化",
            "积累沉淀，等待时机"
        ];
        
        const fortuneIndex = currentYear % fortunes.length;
        
        return {
            currentYear: currentYearPillar,
            majorLuck: majorLuck,
            age: age,
            analysis: fortunes[fortuneIndex],
            suggestions: this.getYearSuggestions(currentYearPillar)
        };
    }

    /**
     * 辅助方法
     */
    solarToLunar(date) {
        // 简化版，实际需要复杂计算
        const year = date.getFullYear();
        const month = date.getMonth() + 1;
        const day = date.getDate();
        return `${year}年${month}月${day}日`;
    }

    calculateAge(birthDate) {
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }
        return age;
    }

    getStemRelation(dayStemIndex, otherStemIndex) {
        const relations = [
            ['比肩', '劫财', '偏印', '正印', '七杀', '正官', '偏财', '正财', '食神', '伤官'],
            ['劫财', '比肩', '正印', '偏印', '正官', '七杀', '正财', '偏财', '伤官', '食神']
        ];
        
        const diff = (otherStemIndex - dayStemIndex + 10) % 10;
        return relations[dayStemIndex % 2][diff];
    }

    getBalanceAdvice(elements) {
        const advice = [];
        
        if (elements['木'] < 1) advice.push('五行缺木，可多接触绿色植物');
        if (elements['火'] < 1) advice.push('五行缺火，可多接触红色物品');
        if (elements['土'] < 1) advice.push('五行缺土，可多接触黄色物品');
        if (elements['金'] < 1) advice.push('五行缺金，可多接触白色金属');
        if (elements['水'] < 1) advice.push('五行缺水，可多接触黑色蓝色');
        
        if (elements['木'] > 3) advice.push('木过旺，注意肝胆健康');
        if (elements['火'] > 3) advice.push('火过旺，注意心脏健康');
        if (elements['土'] > 3) advice.push('土过旺，注意脾胃健康');
        if (elements['金'] > 3) advice.push('金过旺，注意肺部健康');
        if (elements['水'] > 3) advice.push('水过旺，注意肾脏健康');
        
        return advice.length > 0 ? advice : ['五行相对平衡，继续保持'];
    }

    getYearSuggestions(yearPillar) {
        const suggestions = {
            '甲': ['多学习新知识', '注意人际关系'],
            '乙': ['耐心等待时机', '关注健康'],
            '丙': ['积极行动', '注意安全'],
            '丁': ['细致规划', '避免冲动'],
            '戊': ['稳扎稳打', '积累资源'],
            '己': ['灵活应变', '注意沟通'],
            '庚': ['果断决策', '注意压力'],
            '辛': ['精益求精', '注意细节'],
            '壬': ['开拓创新', '注意风险'],
            '癸': ['深思熟虑', '注意情绪']
        };
        
        const stem = yearPillar[0];
        return suggestions[stem] || ['保持积极心态', '注意身体健康'];
    }

    getZodiac(branch) {
        return ZODIAC_ANIMALS[branch] || '未知';
    }

    calculateMonthStem(year, month) {
        // 简化算法
        return (year * 2 + month) % 10;
    }

    getSolarTerms() {
        // 简化版节气表
        return {};
    }
}

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BaziCalculator;
}

// 使用示例
if (typeof window !== 'undefined') {
    window.BaziCalculator = BaziCalculator;
    
    // 示例用法
    const calculator = new BaziCalculator();
    const birthDate = new Date('1990-01-15T08:30:00');
    const result = calculator.calculate(birthDate, 'male', true);
    
    console.log('八字计算结果:', result);
}