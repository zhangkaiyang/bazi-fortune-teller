// 添加测试用神分析的按钮和功能

const fs = require('fs');
const path = require('path');

const htmlFile = path.join(__dirname, 'prototype.html');
let htmlContent = fs.readFileSync(htmlFile, 'utf8');

// 1. 在按钮区域添加测试按钮
const buttonsSection = '<div class="buttons">';
if (htmlContent.includes(buttonsSection)) {
    // 在按钮区域添加测试按钮
    const testButton = `
                <button type="button" class="btn-secondary" onclick="testYongshenDisplay()" style="background: linear-gradient(45deg, #4CAF50, #45a049); color: white;">
                    🧪 测试用神分析
                </button>`;
    
    htmlContent = htmlContent.replace(buttonsSection, buttonsSection + '\n' + testButton);
    console.log('✅ 测试按钮已添加到界面');
}

// 2. 添加测试函数到JavaScript部分
const testFunction = `
        // 测试用神分析显示
        function testYongshenDisplay() {
            // 先清空现有结果
            document.getElementById('resultSection').style.display = 'none';
            document.getElementById('resultContainer').innerHTML = '';
            
            // 模拟API返回的数据
            const testData = {
                success: true,
                data: {
                    bazi: { 
                        year_pillar: "乙亥", 
                        month_pillar: "甲申", 
                        day_pillar: "乙酉", 
                        hour_pillar: "乙酉",
                        full_bazi: "乙亥 甲申 乙酉 乙酉"
                    },
                    elements: { "金": 3, "木": 4, "水": 1, "火": 0, "土": 0 },
                    day_master: {
                        stem: "乙",
                        element: "木",
                        personality: "如藤蔓花草，柔顺温和，适应力强",
                        yinyang: "阴"
                    },
                    fortune: {
                        year: "乙亥",
                        analysis: "财运亨通，但需注意健康，劳逸结合",
                        suggestions: [
                            "保持积极心态，面对挑战",
                            "注意身体健康，合理作息",
                            "多与贵人交流，拓展人脉",
                            "把握投资机会，但需谨慎"
                        ]
                    },
                    basic_info: {
                        solar_date: "1995-08-22",
                        solar_time: "18:50",
                        gender: "male",
                        age: 31,
                        chinese_zodiac: "猪",
                        element: "木"
                    },
                    detailed_fortune: {
                        overall_fortune: {
                            level: "中平",
                            score: 57.53,
                            description: "运势平稳，稳中求进",
                            color: "#FFC107"
                        },
                        element_analysis: {
                            balance_score: 49.22,
                            elements: { "金": 3, "木": 4, "水": 1, "火": 0, "土": 0 },
                            element_names: { "金": "Metal", "木": "Wood", "水": "Water", "火": "Fire", "土": "Earth" },
                            relations: {
                                "相生": ["木→火", "火→土", "土→金", "金→水", "水→木"],
                                "相克": ["木→土", "土→水", "水→火", "火→金", "金→木"]
                            },
                            imbalance: ["金元素过旺", "木元素过旺", "火元素缺失", "土元素缺失"]
                        },
                        day_master_analysis: {
                            element: "金",
                            count: 3,
                            percentage: 37.5,
                            strength: "中",
                            description: "日主适中，状态平稳"
                        },
                        year_fortune: {
                            current_year: 2026,
                            year_pillar: "丙午",
                            fortune: "平稳发展",
                            advice: "稳扎稳打，积累实力"
                        },
                        detailed_suggestions: [
                            "五行略有失衡，建议通过饮食、颜色、方位等方式进行调整。",
                            "日主适中，稳中求进，平衡发展。",
                            "保持积极心态，注重身心健康。",
                            "多行善事，积累福报。",
                            "把握时机，顺势而为。"
                        ],
                        lucky_directions: ["西", "西北"],
                        lucky_colors: ["黑色、蓝色", "红色、紫色", "黄色、棕色"],
                        lucky_numbers: [4, 9]
                    },
                    use_solar_time: true,
                    yongshen_analysis: {
                        success: true,
                        elements_count: { "金": 4, "木": 4, "水": 2, "火": 0, "土": 0 },
                        strength_analysis: {
                            day_stem: "乙",
                            day_element: "木",
                            same_element_count: 4,
                            support_count: 2,
                            suppress_count: 4.0,
                            strength_score: 2.0,
                            strength: "中和",
                            analysis: "日主木中和，如青松挺拔，刚柔并济"
                        },
                        pattern: {
                            pattern: "中和格",
                            detail: "五行相对平衡，流通为佳",
                            recommendation: "五行平衡，流通顺畅为佳"
                        },
                        yongshen: {
                            yongshen: ["火"],
                            jishen: ["金"],
                            analysis: "五行相对平衡，宜补益最弱的火行。",
                            priority: [
                                {
                                    element: "火",
                                    priority: 5,
                                    relation: "调候",
                                    description: "代表礼仪、热情、光明，主南方，红色，夏季"
                                }
                            ]
                        },
                        tiaohou: {
                            season: "秋季七月",
                            season_element: "金",
                            analysis: "秋季金旺，需火炼金，需木生火",
                            suggestions: ["宜用火炼金", "宜用木生火", "避免土过多"]
                        },
                        comprehensive: {
                            summary: "日主乙(木)，五行相对平衡，流通为佳。喜用神为：火。忌神为：金。生于秋季七月，秋季金旺，需火炼金，需木生火",
                            key_points: [
                                "日主：乙(木)",
                                "格局：中和格",
                                "用神：火",
                                "忌神：金",
                                "调候：秋季金旺，需火炼金，需木生火"
                            ]
                        },
                        recommendations: [
                            "宜加强火五行能量",
                            "宜避免或减弱金五行影响",
                            "宜用火炼金",
                            "宜用木生火",
                            "避免土过多",
                            "根据用神选择职业、方位、颜色等",
                            "注意五行平衡，避免极端",
                            "结合大运流年动态调整"
                        ]
                    }
                },
                message: "八字计算成功"
            };
            
            // 显示结果区域
            document.getElementById('resultSection').style.display = 'block';
            
            // 显示结果
            displayResult(testData.data, new Date('1995-08-22T18:50:00'), 'male');
            
            // 滚动到结果区域
            document.getElementById('resultSection').scrollIntoView({ behavior: 'smooth' });
            
            console.log('🧪 用神分析测试数据已加载');
        }`;

// 在JavaScript部分添加测试函数（在页面初始化之前）
const initPattern = '// 初始化页面';
if (htmlContent.includes(initPattern)) {
    htmlContent = htmlContent.replace(initPattern, testFunction + '\n\n        ' + initPattern);
    console.log('✅ 测试函数已添加到JavaScript');
}

// 保存更新后的文件
fs.writeFileSync(htmlFile, htmlContent, 'utf8');

console.log('🎉 测试功能添加完成！');
console.log('📋 使用方法：');
console.log('1. 访问 http://139.159.230.20');
console.log('2. 点击"测试用神分析"按钮');
console.log('3. 查看用神分析显示效果');
console.log('4. 也可以正常输入出生信息进行实际计算');