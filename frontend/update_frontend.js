// 前端更新脚本 - 添加用神分析显示

// 修改displayResult函数来显示用神分析
const updatedDisplayResultFunction = `
function displayResult(result, dateTime, gender) {
    // 显示基本信息
    const basicInfo = \`
        <div class="basic-info-grid">
            <div class="info-item">
                <strong>出生时间：</strong>\${dateTime.toLocaleDateString()} \${dateTime.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
            </div>
            <div class="info-item">
                <strong>性别：</strong>\${gender === 'male' ? '男' : '女'}
            </div>
            <div class="info-item">
                <strong>年龄：</strong>\${result.basic_info?.age || '未知'}岁
            </div>
            <div class="info-item">
                <strong>生肖：</strong>\${result.basic_info?.chinese_zodiac || '未知'}
            </div>
        </div>
    \`;
    document.getElementById('basicInfo').innerHTML = basicInfo;
    
    // 显示八字网格
    const bazi = result.bazi;
    const baziGrid = \`
        <div class="bazi-pillar">
            <div class="pillar">\${bazi.year_pillar}</div>
            <div class="label">年柱</div>
        </div>
        <div class="bazi-pillar">
            <div class="pillar">\${bazi.month_pillar}</div>
            <div class="label">月柱</div>
        </div>
        <div class="bazi-pillar">
            <div class="pillar">\${bazi.day_pillar}</div>
            <div class="label">日柱</div>
        </div>
        <div class="bazi-pillar">
            <div class="pillar">\${bazi.hour_pillar}</div>
            <div class="label">时柱</div>
        </div>
    \`;
    document.getElementById('baziGrid').innerHTML = baziGrid;
    
    // 显示完整八字
    const fullBazi = \`
        <div class="full-bazi">
            <h4>完整八字：</h4>
            <div class="bazi-text">\${bazi.full_bazi}</div>
        </div>
    \`;
    document.getElementById('baziGrid').insertAdjacentHTML('afterend', fullBazi);
    
    // 显示五行分析
    const elements = result.elements;
    const total = Object.values(elements).reduce((a, b) => a + b, 0);
    const elementsChart = Object.entries(elements).map(([element, count]) => {
        const percentage = total > 0 ? (count / total * 100).toFixed(1) : 0;
        const elementClass = {
            '金': 'metal', '木': 'wood', '水': 'water', '火': 'fire', '土': 'earth'
        }[element];
        
        return \`
            <div class="element-bar">
                <div class="element-name">\${element}</div>
                <div class="element-bar-inner">
                    <div class="element-fill \${elementClass}" style="width: \${percentage}%"></div>
                </div>
                <div class="element-value">\${count}</div>
            </div>
        \`;
    }).join('');
    document.getElementById('elementsChart').innerHTML = elementsChart;
    
    // 显示日主分析
    const dayMaster = result.day_master;
    document.getElementById('dayMasterAnalysis').innerHTML = \`
        <h3>日主分析</h3>
        <div class="day-master-detail">
            <p><strong>日主：</strong>\${dayMaster.stem}(\${dayMaster.element}) - \${dayMaster.yinyang === '阳' ? '阳' : '阴'}\${dayMaster.element}</p>
            <p><strong>性格特点：</strong>\${dayMaster.personality}</p>
            <p><strong>五行：</strong>\${dayMaster.element}行</p>
        </div>
    \`;
    
    // 显示运势
    const fortune = result.fortune;
    document.getElementById('fortuneSection').innerHTML = \`
        <h3>📈 运势分析</h3>
        <div class="fortune-content">
            <p><strong>流年：</strong>\${fortune.year}</p>
            <p><strong>分析：</strong>\${fortune.analysis}</p>
            <div class="suggestions-list">
                <h4>建议：</h4>
                <ul>\${fortune.suggestions.map(s => \`<li>\${s}</li>\`).join('')}</ul>
            </div>
        </div>
    \`;
    
    // 显示用神分析（如果存在）
    const yongshenSection = document.createElement('div');
    yongshenSection.className = 'yongshen-section';
    yongshenSection.innerHTML = \`
        <h3>🌟 用神分析</h3>
        <div class="yongshen-content">
            \${result.yongshen_analysis ? renderYongshenAnalysis(result.yongshen_analysis) : '<p>用神分析数据加载中...</p>'}
        </div>
    \`;
    
    // 插入到运势部分之后
    const fortuneSection = document.getElementById('fortuneSection');
    fortuneSection.parentNode.insertBefore(yongshenSection, fortuneSection.nextSibling);
    
    // 显示建议
    const suggestionsList = (result.fortune?.suggestions || []).map(s => \`<li>\${s}</li>\`).join('');
    document.getElementById('suggestions').innerHTML = \`
        <h3>💡 生活建议</h3>
        <ul>\${suggestionsList}</ul>
    \`;
}

function renderYongshenAnalysis(yongshenData) {
    if (yongshenData.error) {
        return \`<p class="error">用神分析失败：\${yongshenData.error}</p>\`;
    }
    
    if (!yongshenData.success) {
        return '<p class="warning">用神分析未成功完成</p>';
    }
    
    const strength = yongshenData.strength_analysis;
    const pattern = yongshenData.pattern;
    const yongshen = yongshenData.yongshen;
    const tiaohou = yongshenData.tiaohou;
    const comprehensive = yongshenData.comprehensive;
    const recommendations = yongshenData.recommendations || [];
    
    return \`
        <div class="yongshen-grid">
            <div class="yongshen-item">
                <h4>日主强弱</h4>
                <p><strong>\${strength.strength}</strong></p>
                <p>\${strength.analysis}</p>
                <p>得分：\${strength.strength_score}</p>
            </div>
            
            <div class="yongshen-item">
                <h4>格局判断</h4>
                <p><strong>\${pattern.pattern}</strong></p>
                <p>\${pattern.detail}</p>
                <p>\${pattern.recommendation}</p>
            </div>
            
            <div class="yongshen-item">
                <h4>用神选择</h4>
                <p><strong>\${yongshen.yongshen.join('、') || '无'}</strong></p>
                <p>\${yongshen.analysis}</p>
                \${yongshen.priority ? \`
                    <div class="priority-list">
                        <h5>用神优先级：</h5>
                        \${yongshen.priority.map(p => \`
                            <div class="priority-item">
                                <span class="element-\${p.element}">\${p.element}</span> - \${p.relation} (\${p.description})
                            </div>
                        \`).join('')}
                    </div>
                \` : ''}
            </div>
            
            <div class="yongshen-item">
                <h4>忌神分析</h4>
                <p><strong>\${yongshen.jishen.join('、') || '无'}</strong></p>
                <p>需要避免或减弱的五行</p>
            </div>
            
            <div class="yongshen-item">
                <h4>调候分析</h4>
                <p><strong>\${tiaohou.season}</strong></p>
                <p>\${tiaohou.analysis}</p>
                <div class="tiaohou-suggestions">
                    \${tiaohou.suggestions ? tiaohou.suggestions.map(s => \`<p>• \${s}</p>\`).join('') : ''}
                </div>
            </div>
            
            <div class="yongshen-item full-width">
                <h4>综合分析</h4>
                <p>\${comprehensive.summary}</p>
                <div class="key-points">
                    <h5>关键要点：</h5>
                    <ul>
                        \${comprehensive.key_points.map(point => \`<li>\${point}</li>\`).join('')}
                    </ul>
                </div>
            </div>
            
            <div class="yongshen-item full-width">
                <h4>具体建议</h4>
                <div class="recommendations">
                    \${recommendations.map((rec, index) => \`
                        <div class="recommendation-item">
                            <span class="rec-number">\${index + 1}.</span>
                            <span>\${rec}</span>
                        </div>
                    \`).join('')}
                </div>
            </div>
        </div>
    \`;
}
`;

// 修改calculateBazi函数来调用真实API
const updatedCalculateBaziFunction = `
async function calculateBazi() {
    const birthDate = document.getElementById('birthDate').value;
    const birthTime = document.getElementById('birthTime').value;
    const gender = document.querySelector('input[name="gender"]:checked').value;
    const useSolarTime = document.getElementById('useSolarTime').checked;
    
    if (!birthDate || !birthTime) {
        alert('请填写完整的出生日期和时间');
        return;
    }
    
    // 显示加载中
    document.getElementById('loading').style.display = 'block';
    document.getElementById('resultSection').style.display = 'none';
    
    try {
        // 调用真实API
        const response = await fetch('http://localhost:8000/api/bazi/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                birth_date: birthDate,
                birth_time: birthTime,
                gender: gender,
                use_solar_time: useSolarTime
            })
        });
        
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.message || '八字计算失败');
        }
        
        // 显示结果
        const dateTime = new Date(birthDate + 'T' + birthTime);
        displayResult(data.data, dateTime, gender);
        
    } catch (error) {
        console.error('API调用失败:', error);
        alert('八字计算失败：' + error.message);
        
        // 回退到模拟计算
        const calculator = new SimpleBaziCalculator();
        const result = calculator.calculate(new Date(birthDate + 'T' + birthTime), gender);
        displayResult(result, new Date(birthDate + 'T' + birthTime), gender);
    } finally {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('resultSection').style.display = 'block';
        
        // 滚动到结果区域
        document.getElementById('resultSection').scrollIntoView({ behavior: 'smooth' });
    }
}
`;

// 添加CSS样式
const yongshenCSS = `
/* 用神分析样式 */
.yongshen-section {
    background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
    border: 2px solid #ff9800;
    border-radius: 15px;
    padding: 25px;
    margin: 25px 0;
    box-shadow: 0 5px 15px rgba(255, 152, 0, 0.1);
}

.yongshen-section h3 {
    color: #ff6f00;
    margin-bottom: 20px;
    font-size: 1.5rem;
    border-bottom: 2px solid #ffb74d;
    padding-bottom: 10px;
}

.yongshen-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin-top: 15px;
}

.yongshen-item {
    background: white;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    border-left: 4px solid #ff9800;
}

.yongshen-item.full-width {
    grid-column: 1 / -1;
}

.yongshen-item h4 {
    color: #ff6f00;
    margin-bottom: 10px;
    font-size: 1.2rem;
}

.yongshen-item h5 {
    color: #ff9800;
    margin: 10px 0 5px 0;
    font-size: 1rem;
}

.priority-list {
    margin-top: 10px;
    padding: 10px;
    background: #fff3e0;
    border-radius: 8px;
}

.priority-item {
    padding: 5px 0;
    border-bottom: 1px dashed #ffcc80;
}

.priority-item:last-child {
    border-bottom: none;
}

.element-金 { color: #ffd700; font-weight: bold; }
.element-木 { color: #4caf50; font-weight: bold; }
.element-水 { color: #2196f3; font-weight: bold; }
.element-火 { color: #f44336; font-weight: bold; }
.element-土 { color: #795548; font-weight: bold; }

.tiaohou-suggestions {
    margin-top: 10px;
    padding-left: 15px;
}

.tiaohou-suggestions p {
    margin: 5px 0;
    color: #666;
}

.key-points ul {
    list-style-type: none;
    padding-left: 0;
}

.key-points li {
    padding: 8px 0;
    border-bottom: 1px solid #eee;
}

.key-points li:last-child {
    border-bottom: none;
}

.recommendations {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
    margin-top: 15px;
}

.recommendation-item {
    background: #e8f5e9;
    padding: 12px;
    border-radius: 8px;
    border-left: 3px solid #4caf50;
}

.rec-number {
    display: inline-block;
    width: 25px;
    height: 25px;
    background: #4caf50;
    color: white;
    border-radius: 50%;
    text-align: center;
    line-height: 25px;
    margin-right: 10px;
    font-weight: bold;
}

/* 基本样式增强 */
.basic-info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin: 20px 0;
    padding: 15px;
    background: #f5f5f5;
    border-radius: 10px;
}

.info-item {
    padding: 10px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.full-bazi {
    text-align: center;
    margin: 20px 0;
    padding: 15px;
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    border-radius: 10px;
    border: 2px solid #2196f3;
}

.bazi-text {
    font-size: 1.8rem;
    font-weight: bold;
    color: #1565c0;
    margin: 10px 0;
    letter-spacing: 5px;
}

.day-master-detail {
    background: #f1f8e9;
    padding: 15px;
    border-radius: 10px;
    margin: 15px 0;
}

.fortune-content {
    background: #fff3e0;
    padding: 20px;
    border-radius: 10px;
    margin: 15px 0;
}

.suggestions-list ul {
    list-style-type: none;
    padding-left: 0;
}

.suggestions-list li {
    padding: 10px;
    margin: 5px 0;
    background: white;
    border-radius: 8px;
    border-left: 3px solid #4caf50;
}

.error {
    color: #f44336;
    background: #ffebee;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #f44336;
}

.warning {
    color: #ff9800;
    background: #fff3e0;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ff9800;
}
`;

console.log("前端更新代码已生成。请将以下内容添加到HTML文件中：");
console.log("\n1. 替换displayResult函数：");
console.log(updatedDisplayResultFunction);
console.log("\n2. 替换calculateBazi函数：");
console.log(updatedCalculateBaziFunction);
console.log("\n3. 添加CSS样式到<style>标签中：");
console.log(yongshenCSS);