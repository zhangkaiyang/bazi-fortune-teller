// 更新前端用神分析显示功能

// 读取原型文件
const fs = require('fs');
const path = require('path');

const htmlFile = path.join(__dirname, 'prototype.html');
let htmlContent = fs.readFileSync(htmlFile, 'utf8');

// 在displayResult函数中添加用神分析显示
const yongshenDisplayCode = `
            // 显示用神分析（如果存在）
            if (result.yongshen_analysis && result.yongshen_analysis.success) {
                const yongshen = result.yongshen_analysis;
                
                // 创建用神分析HTML
                let yongshenHTML = \`
                <div class="yongshen-section">
                    <h3>📊 用神分析</h3>
                    <div class="yongshen-grid">
                        <div class="yongshen-item">
                            <h4>日主分析</h4>
                            <p><strong>日主：</strong>\${yongshen.strength_analysis.day_stem}(\${yongshen.strength_analysis.day_element})</p>
                            <p><strong>强弱：</strong>\${yongshen.strength_analysis.strength}</p>
                            <p><strong>分析：</strong>\${yongshen.strength_analysis.analysis}</p>
                        </div>
                        
                        <div class="yongshen-item">
                            <h4>格局判断</h4>
                            <p><strong>格局：</strong>\${yongshen.pattern.pattern}</p>
                            <p><strong>详情：</strong>\${yongshen.pattern.detail}</p>
                            <p><strong>建议：</strong>\${yongshen.pattern.recommendation}</p>
                        </div>
                        
                        <div class="yongshen-item">
                            <h4>用神忌神</h4>
                            <p><strong>喜用神：</strong>\${yongshen.yongshen.yongshen.join('、')}</p>
                            <p><strong>忌神：</strong>\${yongshen.yongshen.jishen.join('、')}</p>
                            <p><strong>分析：</strong>\${yongshen.yongshen.analysis}</p>
                        </div>
                        
                        <div class="yongshen-item full-width">
                            <h4>调候分析</h4>
                            <p><strong>季节：</strong>\${yongshen.tiaohou.season} (\${yongshen.tiaohou.season_element})</p>
                            <p><strong>分析：</strong>\${yongshen.tiaohou.analysis}</p>
                            <p><strong>建议：</strong>\${yongshen.tiaohou.suggestions.join('；')}</p>
                        </div>
                        
                        <div class="yongshen-item full-width">
                            <h4>综合建议</h4>
                            <p><strong>总结：</strong>\${yongshen.comprehensive.summary}</p>
                            <div style="margin-top: 10px;">
                                <strong>关键要点：</strong>
                                <ul style="margin-top: 5px; padding-left: 20px;">
                                    \${yongshen.comprehensive.key_points.map(point => \`<li>\${point}</li>\`).join('')}
                                </ul>
                            </div>
                        </div>
                        
                        <div class="yongshen-item full-width">
                            <h4>详细建议</h4>
                            <ul style="margin-top: 5px; padding-left: 20px;">
                                \${yongshen.recommendations.map(rec => \`<li>\${rec}</li>\`).join('')}
                            </ul>
                        </div>
                    </div>
                </div>
                \`;
                
                // 插入到结果区域
                const resultContainer = document.getElementById('resultContainer');
                resultContainer.insertAdjacentHTML('beforeend', yongshenHTML);
            }`;

// 找到五行分析显示的位置，在用神分析之前插入
const insertPoint = htmlContent.indexOf('// 显示五行分析');
if (insertPoint !== -1) {
    // 找到五行分析显示代码的结束位置
    const elementsDisplayEnd = htmlContent.indexOf('document.getElementById(\'elementsChart\')', insertPoint);
    if (elementsDisplayEnd !== -1) {
        // 找到五行分析显示代码的完整结束位置（找到下一个函数或大括号结束）
        let endIndex = htmlContent.indexOf('}', elementsDisplayEnd);
        while (endIndex !== -1 && htmlContent.substring(elementsDisplayEnd, endIndex).split('{').length !== htmlContent.substring(elementsDisplayEnd, endIndex).split('}').length) {
            endIndex = htmlContent.indexOf('}', endIndex + 1);
        }
        
        if (endIndex !== -1) {
            // 在五行分析显示后插入用神分析代码
            const newHtml = htmlContent.substring(0, endIndex + 1) + 
                          '\n\n' + 
                          yongshenDisplayCode + 
                          '\n' + 
                          htmlContent.substring(endIndex + 1);
            
            fs.writeFileSync(htmlFile, newHtml, 'utf8');
            console.log('✅ 用神分析显示代码已成功添加到前端！');
        } else {
            console.log('❌ 无法找到五行分析显示代码的结束位置');
        }
    } else {
        console.log('❌ 无法找到五行分析显示代码');
    }
} else {
    console.log('❌ 无法找到五行分析显示的位置');
}

// 另外，我们还需要更新API调用部分，确保正确处理用神分析数据
console.log('📝 接下来需要更新API调用部分...');

// 检查API调用代码
const apiCallPattern = /fetch\(apiUrl,\s*\{[^}]*\}\)/;
if (apiCallPattern.test(htmlContent)) {
    console.log('✅ API调用代码已存在');
    
    // 添加一个简单的测试函数来验证用神分析显示
    const testYongshenFunction = `
// 测试用神分析显示
function testYongshenDisplay() {
    const testData = {
        success: true,
        data: {
            bazi: { year: "乙亥", month: "甲申", day: "乙酉", hour: "乙酉" },
            elements: { "金": 3, "木": 4, "水": 1, "火": 0, "土": 0 },
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
        }
    };
    
    // 模拟显示结果
    displayResult(testData.data, new Date('1995-08-22T18:50:00'), 'male');
    console.log('测试用神分析显示完成');
}
`;

    // 在文件末尾添加测试函数
    const newHtmlWithTest = htmlContent.replace(/<\/script>\s*<\/body>/, testYongshenFunction + '\n</script>\n</body>');
    fs.writeFileSync(htmlFile, newHtmlWithTest, 'utf8');
    console.log('✅ 测试函数已添加到前端');
} else {
    console.log('❌ 未找到API调用代码');
}

console.log('🎉 前端用神分析显示功能更新完成！');
console.log('📋 下一步：');
console.log('1. 访问 http://139.159.230.20 测试用神分析显示');
console.log('2. 如果需要，可以调用 testYongshenDisplay() 函数进行测试');
console.log('3. 检查用神分析部分的样式和布局');