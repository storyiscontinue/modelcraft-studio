/* ==========================================================================
   ModelCraft - Elite Mathematical & Fourier Simulation Engine
   Redesigned for Warm Beige Editorial Theme. Complies with security policies.
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {

    /* ==========================================================================
       1. 实时 3D 洛伦兹吸引子仿真器 (Lorenz Attractor)
       ========================================================================== */
    const attractorCanvas = document.getElementById('attractor-canvas');
    if (attractorCanvas) {
        const ctx = attractorCanvas.getContext('2d');
        const dpr = window.devicePixelRatio || 1;
        
        let width = attractorCanvas.width = attractorCanvas.offsetWidth * dpr;
        let height = attractorCanvas.height = attractorCanvas.offsetHeight * dpr;
        ctx.scale(dpr, dpr);

        let logicalWidth = attractorCanvas.offsetWidth;
        let logicalHeight = attractorCanvas.offsetHeight;

        window.addEventListener('resize', () => {
            width = attractorCanvas.width = attractorCanvas.offsetWidth * dpr;
            height = attractorCanvas.height = attractorCanvas.offsetHeight * dpr;
            ctx.scale(dpr, dpr);
            logicalWidth = attractorCanvas.offsetWidth;
            logicalHeight = attractorCanvas.offsetHeight;
        });

        // 洛伦兹混沌数学方程参数
        const sigma = 10;
        const rho = 28;
        const beta = 8 / 3;
        const dt = 0.005;

        // 建立两条不同初始值的小球运动轨线 (展示混沌系统的敏感性)
        const trajectories = [
            {
                color: 'rgba(198, 114, 83, 0.75)', /* 陶土红 */
                x: 0.1, y: 0, z: 0,
                history: []
            },
            {
                color: 'rgba(111, 131, 112, 0.75)', /* 鼠尾草绿 */
                x: 0.1, y: 0.002, z: 0,
                history: []
            }
        ];

        const maxHistory = 380;
        let yaw = 0.6;
        let pitch = 0.35;
        let isDragging = false;
        let startX = 0, startY = 0;
        let startYaw = 0, startPitch = 0;

        // 拖拽旋转视角
        attractorCanvas.addEventListener('mousedown', (e) => {
            isDragging = true;
            startX = e.clientX;
            startY = e.clientY;
            startYaw = yaw;
            startPitch = pitch;
        });

        window.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            const dx = e.clientX - startX;
            const dy = e.clientY - startY;
            yaw = startYaw + dx * 0.007;
            pitch = startPitch + dy * 0.007;
        });

        window.addEventListener('mouseup', () => {
            isDragging = false;
        });

        // 3D 转换投影
        function project3D(x, y, z) {
            const cosY = Math.cos(yaw);
            const sinY = Math.sin(yaw);
            let rx1 = x * cosY - y * sinY;
            let ry1 = x * sinY + y * cosY;
            let rz1 = z;

            const cosP = Math.cos(pitch);
            const sinP = Math.sin(pitch);
            let rx2 = rx1;
            let ry2 = ry1 * cosP - rz1 * sinP;
            let rz2 = ry1 * sinP + rz1 * cosP;

            const scale = logicalHeight / 50; 
            const screenX = logicalWidth / 2 + rx2 * scale;
            const screenY = logicalHeight / 2 - (rz2 - 25) * scale;

            return { x: screenX, y: screenY };
        }

        function drawAttractor() {
            // 亮色渲染的尾迹虚化
            ctx.fillStyle = 'rgba(253, 252, 249, 0.12)';
            ctx.fillRect(0, 0, logicalWidth, logicalHeight);

            trajectories.forEach(t => {
                const dx_val = sigma * (t.y - t.x) * dt;
                const dy_val = (t.x * (rho - t.z) - t.y) * dt;
                const dz_val = (t.x * t.y - beta * t.z) * dt;

                t.x += dx_val;
                t.y += dy_val;
                t.z += dz_val;

                t.history.push({ x: t.x, y: t.y, z: t.z });
                if (t.history.length > maxHistory) {
                    t.history.shift();
                }

                if (t.history.length < 2) return;

                ctx.beginPath();
                const startPt = project3D(t.history[0].x, t.history[0].y, t.history[0].z);
                ctx.moveTo(startPt.x, startPt.y);

                for (let i = 1; i < t.history.length; i++) {
                    const pt = project3D(t.history[i].x, t.history[i].y, t.history[i].z);
                    ctx.lineTo(pt.x, pt.y);
                }

                ctx.strokeStyle = t.color;
                ctx.lineWidth = 1.8;
                ctx.lineCap = 'round';
                ctx.lineJoin = 'round';
                ctx.stroke();
            });

            requestAnimationFrame(drawAttractor);
        }

        drawAttractor();
    }


    /* ==========================================================================
       2. 傅里叶级数圆周行星轮实时数学模拟器 (Fourier Showcase)
       ========================================================================== */
    const fourierCanvas = document.getElementById('fourier-canvas');
    if (fourierCanvas) {
        const fctx = fourierCanvas.getContext('2d');
        const fdpr = window.devicePixelRatio || 1;
        
        let fwidth = fourierCanvas.width = fourierCanvas.offsetWidth * fdpr;
        let fheight = fourierCanvas.height = fourierCanvas.offsetHeight * fdpr;
        fctx.scale(fdpr, fdpr);

        let flogWidth = fourierCanvas.offsetWidth;
        let flogHeight = fourierCanvas.offsetHeight;

        window.addEventListener('resize', () => {
            fwidth = fourierCanvas.width = fourierCanvas.offsetWidth * fdpr;
            fheight = fourierCanvas.height = fourierCanvas.offsetHeight * fdpr;
            fctx.scale(fdpr, fdpr);
            flogWidth = fourierCanvas.offsetWidth;
            flogHeight = fourierCanvas.offsetHeight;
        });

        // 傅里叶模拟变量
        let time = 0;
        let fourierPath = [];
        let harmonicsCount = 5;
        let waveType = 'square'; // square, sawtooth, triangle
        let isPaused = false;

        const harmonicsSlider = document.getElementById('fourier-harmonics-slider');
        const harmonicsValLabel = document.getElementById('fourier-harmonics-val');
        const waveTypeBtns = document.querySelectorAll('#fourier-wave-types .toggle-btn');
        const btnFourierPause = document.getElementById('btn-fourier-pause');
        const btnFourierReset = document.getElementById('btn-fourier-reset');

        // 控制器绑定
        if (harmonicsSlider) {
            harmonicsSlider.addEventListener('input', (e) => {
                harmonicsCount = parseInt(e.target.value);
                harmonicsValLabel.textContent = harmonicsCount;
                // 动态更新滑块背景进度条
                const pct = (harmonicsCount - 1) / (25 - 1) * 100;
                harmonicsSlider.style.background = `linear-gradient(to right, var(--accent-clay) 0%, var(--accent-brass) ${pct}%, var(--text-muted) ${pct}%, var(--text-muted) 100%)`;
            });
            // 初始化滑轨背景
            const initPct = (harmonicsCount - 1) / (25 - 1) * 100;
            harmonicsSlider.style.background = `linear-gradient(to right, var(--accent-clay) 0%, var(--accent-brass) ${initPct}%, var(--text-muted) ${initPct}%, var(--text-muted) 100%)`;
        }

        waveTypeBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                waveTypeBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                waveType = btn.getAttribute('data-wave');
                fourierPath = []; // 切换波形清空画笔历史
            });
        });

        if (btnFourierPause) {
            btnFourierPause.addEventListener('click', () => {
                isPaused = !isPaused;
                btnFourierPause.textContent = isPaused ? "恢复模拟" : "暂停模拟";
            });
        }

        if (btnFourierReset) {
            btnFourierReset.addEventListener('click', () => {
                fourierPath = [];
                time = 0;
            });
        }

        function drawFourier() {
            fctx.clearRect(0, 0, flogWidth, flogHeight);

            // 中心基准位置
            const centerX = flogWidth * 0.28;
            const centerY = flogHeight * 0.5;
            let cx = centerX;
            let cy = centerY;

            // 绘制级数行星圆环
            for (let i = 0; i < harmonicsCount; i++) {
                let prevX = cx;
                let prevY = cy;

                let n = 0;
                let radius = 0;

                // 物理方程：根据不同的波形级数公式，算各阶分量的半径与频率
                if (waveType === 'square') {
                    n = i * 2 + 1; // 仅奇数阶谐波
                    radius = 65 * (4 / (n * Math.PI)); // 振幅衰减系数
                } else if (waveType === 'sawtooth') {
                    n = i + 1; // 包含所有谐波
                    radius = 50 * (2 / (n * Math.PI)) * (n % 2 === 0 ? -1 : 1);
                } else if (waveType === 'triangle') {
                    n = i * 2 + 1;
                    radius = 70 * (8 / ((n * Math.PI) ** 2)) * (i % 2 === 1 ? -1 : 1);
                }

                // 行星周转坐标增量 (经典匀速圆周运动方程)
                const angularSpeed = n * time;
                cx += radius * Math.cos(angularSpeed);
                cy += radius * Math.sin(angularSpeed);

                // 绘制圆形环形轨道 (黄铜色细线)
                fctx.beginPath();
                fctx.arc(prevX, prevY, Math.abs(radius), 0, Math.PI * 2);
                fctx.strokeStyle = 'rgba(184, 144, 71, 0.15)';
                fctx.lineWidth = 1;
                fctx.stroke();

                // 绘制行星径向连线 (黄铜色粗线)
                fctx.beginPath();
                fctx.moveTo(prevX, prevY);
                fctx.lineTo(cx, cy);
                fctx.strokeStyle = 'rgba(44, 37, 30, 0.3)';
                fctx.lineWidth = 1.2;
                fctx.stroke();

                // 绘制衔接节点小球
                fctx.beginPath();
                fctx.arc(cx, cy, 2, 0, Math.PI * 2);
                fctx.fillStyle = 'var(--text-charcoal)';
                fctx.fill();
            }

            // 保存最终行星笔尖的 Y 坐标到历史记录
            if (!isPaused) {
                fourierPath.unshift(cy);
                if (fourierPath.length > 600) {
                    fourierPath.pop();
                }
            }

            // 绘制笔尖水平拉伸连线 (引出指示虚线)
            const graphXStart = flogWidth * 0.58;
            fctx.beginPath();
            fctx.moveTo(cx, cy);
            fctx.lineTo(graphXStart, fourierPath[0] || cy);
            fctx.strokeStyle = 'rgba(198, 114, 83, 0.25)';
            fctx.lineWidth = 1;
            fctx.setLineDash([3, 3]);
            fctx.stroke();
            fctx.setLineDash([]); // 重置虚线样式

            // 绘制笔尖拉伸出来的波动曲线 (陶土红线)
            fctx.beginPath();
            if (fourierPath.length > 0) {
                fctx.moveTo(graphXStart, fourierPath[0]);
                for (let j = 1; j < fourierPath.length; j++) {
                    // X轴随时间向右拉伸：每个像素点间隔 0.6px
                    fctx.lineTo(graphXStart + j * 0.6, fourierPath[j]);
                }
            }
            fctx.strokeStyle = 'var(--accent-clay)';
            fctx.lineWidth = 2.2;
            fctx.stroke();

            // 绘制笔头红色大发光点
            fctx.beginPath();
            fctx.arc(cx, cy, 4, 0, Math.PI * 2);
            fctx.fillStyle = 'var(--accent-clay)';
            fctx.shadowBlur = 6;
            fctx.shadowColor = 'var(--accent-clay)';
            fctx.fill();
            fctx.shadowBlur = 0; // 重置发光

            // 时间推移
            if (!isPaused) {
                time += 0.035;
            }

            requestAnimationFrame(drawFourier);
        }

        drawFourier();
    }


    /* ==========================================================================
       3. 拓扑工作流点击高亮与连线更新 (Topology Link Update)
       ========================================================================== */
    const topologyNodes = document.querySelectorAll('.topology-node');
    const detailCard = document.getElementById('node-detail-card');
    const detailTechName = document.getElementById('detail-tech-name');
    const detailTitle = document.getElementById('detail-display-title');
    const detailDesc = document.getElementById('detail-display-desc');
    const detailMathFormula = document.getElementById('detail-math-formula');
    const detailSkillUsed = document.getElementById('detail-skill-used');
    const detailFilesGenerated = document.getElementById('detail-files-generated');

    const nodeData = {
        "1": {
            tech: "comp-prob-analysis",
            title: "赛题拆解 (Problem Analysis)",
            desc: "智能提取 PDF 与 DOCX 题面文本。加载内置 Skills 剥离赛题条件、背景与隐含边界参数，在本地生成 `PROBLEM_ANALYSIS.md` 分析大纲报告。",
            formula: "P_core = TF-IDF(W_i) ⊗ Skill_prior ⟶ Output(PROBLEM_ANALYSIS.md)",
            skill: "comp-prob-analysis",
            files: "PROBLEM_ANALYSIS.md"
        },
        "2": {
            tech: "comp-modeling",
            title: "数学建模 (Model Setup)",
            desc: "建立方程模型与验证参数。软件将自主推导控制微分方程以及状态空间矩阵，确定求解算法的严密边界，并写入本地 `MODELING_REPORT.md`。",
            formula: "dx/dt = f(x, u, t)   s.t.   g(x, u) ≤ 0 ⟶ Output(MODELING_REPORT.md)",
            skill: "comp-modeling",
            files: "MODELING_REPORT.md"
        },
        "3": {
            tech: "comp-code",
            title: "代码求解 (Code Execution)",
            desc: "自动编写并运行科学计算与仿真脚本 `code/main.py`。智能监测本地收敛性，执行基线不退化、网格剖分校验，吐出 `RESULTS.md` 及图表参数缓存文件。",
            formula: "x_{k+1} = x_k + (h/6)(k_1 + 2k_2 + 2k_3 + k_4) ⟶ Output(code/main.py, RESULTS.md)",
            skill: "comp-code",
            files: "code/main.py, RESULTS.md, validation_report.json"
        },
        "4": {
            tech: "analyze-results",
            title: "统计复核 (Result Audit)",
            desc: "对 Python 跑算结果进行双重统计合理性审计。执行判定系数检测与变量范围越界复核，验证模型的自稳定性与敏感性，杜绝偏态坏解。",
            formula: "R^2 = 1 - [Σ(y_i - ŷ_i)^2 / Σ(y_i - ȳ)^2] ⟶ Limit Check (PASS)",
            skill: "analyze-results",
            files: "数据校验状态: 100% 物理通过"
        },
        "5": {
            tech: "paper-figure",
            title: "图表导出 (Figures Script)",
            desc: "利用 matplotlib 等组件，将数值求解的缓存矩阵导出为排版所需的矢量 PDF 图表与 LaTeX 表格，并列出 LaTeX 导入文件清单。",
            formula: "Fig_vector = Matplotlib(X, Y) ⟶ Output(figures/curve_fit.pdf, figures/data_table.tex)",
            skill: "paper-figure",
            files: "figures/curve_fit.pdf, figures/data_table.tex"
        },
        "6": {
            tech: "comp-paper-zh",
            title: "论文起草 (Drafting LaTeX)",
            desc: "载入高水准竞赛模板 Skill，生成结构化 LaTeX 中文论文源码 `paper/main.tex`。自动挂载假设、公式推导、数值列表与矢量插图的交叉引用索引。",
            formula: "Paper_LaTeX = Σ Templates + Sections(Abstract, Modeling, Results) ⟶ Output(paper/main.tex)",
            skill: "comp-paper-zh",
            files: "paper/main.tex"
        },
        "7": {
            tech: "ai-compliance",
            title: "合规记录 (Compliance Log)",
            desc: "根据竞赛合规组最新防作弊指令，软件自动导出工作流中 AI 协作 Prompt 的调用历史与 Token 消耗审计单，编写合规附件 `AI_TOOL_USAGE_DETAILS.md`。",
            formula: "Audit_trail = {Prompt_k, Tokens_k} ⟶ Output(AI_TOOL_USAGE_DETAILS.md)",
            skill: "ai-compliance",
            files: "AI_TOOL_USAGE_DETAILS.md, paper/AI_USAGE_DECLARATION.md"
        },
        "8": {
            tech: "quality-check",
            title: "三轮独立复审 (Quality Review)",
            desc: "调用三个隔离大模型模拟独立“评审人”，交叉审计代码、论文合理性及排版细节，盲审评分需全部通过，阻断敷衍或空白占位符溢出。",
            formula: "Accept = ∏_{m=1}^3 Review_m ≥ 0.95 ⟶ Status (APPROVED)",
            skill: "quality-check-r1, r2, r3",
            files: "Quality_Check_Report.md"
        },
        "9": {
            tech: "comp-compile-zh",
            title: "成果编译 (XeLaTeX PDF)",
            desc: "一键激活本地 XeLaTeX 编译，自动配置交叉引用并输出精美论文 PDF，剔除中间编译日志，在独立成果文件夹下打包支撑代码压缩包。",
            formula: "XeLaTeX(paper/main.tex) ⟶ Output(成果发布/main.pdf, 支撑材料.zip)",
            skill: "comp-compile-zh",
            files: "成果发布/main.pdf, 支撑材料.zip"
        }
    };

    // 更新拓扑连线的高亮类
    function updateTopologyLines(activeStep) {
        const paths = [
            'path-1-2', 'path-2-3', 'path-3-4', 'path-4-5',
            'path-5-6', 'path-6-7', 'path-7-8', 'path-8-9'
        ];
        paths.forEach((pathId, index) => {
            const pathEl = document.getElementById(pathId);
            if (!pathEl) return;
            pathEl.classList.remove('active', 'completed');
            
            const lineIndex = index + 2; // path-1-2 连接到第二步
            if (activeStep > lineIndex) {
                pathEl.classList.add('completed');
            } else if (activeStep === lineIndex) {
                pathEl.classList.add('active');
            }
        });
    }

    topologyNodes.forEach(node => {
        node.addEventListener('click', () => {
            topologyNodes.forEach(n => n.classList.remove('active'));
            node.classList.add('active');

            const step = node.getAttribute('data-step');
            const data = nodeData[step];

            if (data) {
                detailTechName.textContent = data.tech;
                detailTitle.textContent = data.title;
                detailDesc.textContent = data.desc;
                detailMathFormula.textContent = data.formula;
                detailSkillUsed.textContent = data.skill;
                detailFilesGenerated.textContent = data.files;

                // 联动高亮 SVG 连线
                updateTopologyLines(parseInt(step));

                detailCard.style.transform = 'scale(0.98)';
                setTimeout(() => detailCard.style.transform = 'scale(1)', 150);
            }
        });
    });


    /* ==========================================================================
       4. 学术仿真终端逻辑 (Recorder Workbench)
       ========================================================================== */
    const terminalStartBtn = document.getElementById('terminal-start-btn');
    const terminalResetBtn = document.getElementById('terminal-reset');
    const termLogsContainer = document.getElementById('terminal-logs');
    const termTokens = document.getElementById('stats-tokens');
    const termCost = document.getElementById('stats-cost');
    const termFileTree = document.getElementById('terminal-file-tree');
    const termEmptyTreeMsg = document.getElementById('file-tree-empty');
    const termGaugeDot = document.getElementById('gauge-dot');
    const termGaugeText = document.getElementById('gauge-text');

    let simRunning = false;
    let simStepIndex = 0;
    let simLogIndex = 0;
    let simTokens = 0;
    let simCost = 0.00;
    let simTimer = null;

    const terminalStepsData = [
        {
            stepNum: 1,
            tokens: 15100,
            cost: 0.15,
            files: ["PROBLEM_ANALYSIS.md"],
            logs: [
                "[INFO] 正在扫描本地工作空间并挂载题面文档...",
                "[SYSTEM] 读取物理文件: '2026_CUMCM_Problem_A.pdf' (1.42 MB)",
                "[SKILL] 加载学术微技能: comp-prob-analysis ... [OK]",
                "[API] 发起赛题解析请求 (model: gpt-4o)...",
                "[SYSTEM] 识别目标自变量: 储罐流量 q(t), 系统压力 P_in.",
                "[FILE] 成功在本地成果树生成文件: 'PROBLEM_ANALYSIS.md'",
                "[INFO] 阶段 1 (赛题拆解) 闭环通过！"
            ]
        },
        {
            stepNum: 2,
            tokens: 24500,
            cost: 0.25,
            files: ["MODELING_REPORT.md"],
            logs: [
                "[INFO] 准备建立系统状态矩阵方程...",
                "[SKILL] 加载学术微技能: comp-modeling ... [OK]",
                "[SYSTEM] 推导一阶常微分控制模型: dP/dt = k * (q_in - q_out)",
                "[FILE] 写入数学模型与建模大纲文档: 'MODELING_REPORT.md'",
                "[INFO] 阶段 2 (数学建模) 闭环通过！"
            ]
        },
        {
            stepNum: 3,
            tokens: 43000,
            cost: 0.43,
            files: ["code/main.py", "RESULTS.md", "validation_report.json"],
            logs: [
                "[INFO] 开始起草科学计算求解 Python 脚本...",
                "[SKILL] 加载学术微技能: comp-code ... [OK]",
                "[SYSTEM] 本地建立安全沙箱环境并执行 code/main.py ...",
                "[RUN] Python 3.10 求解器开始积分。龙格-库塔求解中...",
                "[RUN] 收敛性检查: 残差范数 L2 = 1.22e-6 (符合物理定律)",
                "[FILE] 生成试验结果数据缓存: 'validation_report.json'",
                "[FILE] 成功写入求解结论大纲: 'RESULTS.md'",
                "[INFO] 阶段 3 (求解代码) 闭环通过！"
            ]
        },
        {
            stepNum: 4,
            tokens: 11000,
            cost: 0.11,
            files: [],
            logs: [
                "[INFO] 正在对数据结论进行合理性与敏感度自检...",
                "[SKILL] 加载学术微技能: analyze-results ... [OK]",
                "[SYSTEM] 参数一致性校验: 相关系数 R-squared = 0.9945 (PASS)",
                "[INFO] 阶段 4 (结果复核) 闭环通过！"
            ]
        },
        {
            stepNum: 5,
            tokens: 16000,
            cost: 0.16,
            files: ["figures/curve_fit.pdf", "figures/data_table.tex"],
            logs: [
                "[INFO] 提炼数值结果并绘制矢量图表...",
                "[SKILL] 加载学术微技能: paper-figure ... [OK]",
                "[FILE] 导出 Matplotlib 矢量插图: 'figures/curve_fit.pdf'",
                "[FILE] 成功格式化输出 LaTeX 数据表格: 'figures/data_table.tex'",
                "[INFO] 阶段 5 (图表提炼) 闭环通过！"
            ]
        },
        {
            stepNum: 6,
            tokens: 36000,
            cost: 0.36,
            files: ["paper/main.tex"],
            logs: [
                "[INFO] 准备起草学术竞赛中文论文源码...",
                "[SKILL] 加载学术微技能: comp-paper-zh ... [OK]",
                "[SYSTEM] 解析论文假设与公式推导排版模板...",
                "[FILE] 写入 LaTeX 主控论文工程文件: 'paper/main.tex'",
                "[INFO] 阶段 6 (论文起草) 闭环通过！"
            ]
        },
        {
            stepNum: 7,
            tokens: 9500,
            cost: 0.09,
            files: ["AI_TOOL_USAGE_DETAILS.md", "paper/AI_USAGE_DECLARATION.md"],
            logs: [
                "[INFO] 记录 AI 辅助提示词与日志痕迹清单...",
                "[SKILL] 加载学术微技能: ai-compliance ... [OK]",
                "[FILE] 成功写出 AI 合规辅助使用详情: 'AI_TOOL_USAGE_DETAILS.md'",
                "[INFO] 阶段 7 (合规记录) 闭环通过！"
            ]
        },
        {
            stepNum: 8,
            tokens: 22000,
            cost: 0.22,
            files: ["Quality_Check_Report.md"],
            logs: [
                "[INFO] 启动三轮独立盲评质检隔离程序...",
                "[SYSTEM] 第一轮逻辑合理度盲审: 通过。无前后论据驳回项。",
                "[SYSTEM] 第二轮公式映射校验: 通过。与 main.py 参数映射吻合。",
                "[FILE] 写入质检交叉评估汇总报告: 'Quality_Check_Report.md'",
                "[INFO] 阶段 8 (三轮质检) 全部通过！允许编译！"
            ]
        },
        {
            stepNum: 9,
            tokens: 12000,
            cost: 0.12,
            files: ["成果发布/main.pdf", "成果发布/支撑材料.zip"],
            logs: [
                "[INFO] 启动本地学术排版 XeLaTeX 自动编译流...",
                "[SKILL] 加载学术微技能: comp-compile-zh ... [OK]",
                "[RUN] 执行本地指令: xelatex -no-shell-escape paper/main.tex",
                "[SYSTEM] 自动排版结束。XeLaTeX 以错误码 0 顺利退出！",
                "[FILE] 生成论文最终 PDF 终稿: '成果发布/main.pdf'",
                "[FILE] 导出压缩包代码包: '成果发布/支撑材料.zip'",
                "[SYSTEM] 恭喜宝宝！ModelCraft 本地数模工作流圆满闭环运行！🎉"
            ]
        }
    ];

    function appendTermLog(text, className = '') {
        const row = document.createElement('div');
        row.className = 'output-row';
        if (className) row.classList.add(className);
        row.textContent = text;
        termLogsContainer.appendChild(row);
        termLogsContainer.scrollTop = termLogsContainer.scrollHeight;
    }

    function addTermFile(fileName) {
        if (termEmptyTreeMsg) termEmptyTreeMsg.style.display = 'none';

        const item = document.createElement('div');
        item.className = 'file-node newly-created';

        const icon = document.createElement('span');
        icon.textContent = fileName.endsWith('.pdf') ? '📕 ' : fileName.endsWith('.zip') ? '📦 ' : '📄 ';

        const nameSpan = document.createElement('span');
        nameSpan.textContent = fileName;

        item.appendChild(icon);
        item.appendChild(nameSpan);
        termFileTree.appendChild(item);
    }

    function setTopologyNodeActive(stepNum) {
        topologyNodes.forEach(node => {
            const num = parseInt(node.getAttribute('data-step'));
            node.classList.remove('active', 'completed');
            if (num === stepNum) {
                node.classList.add('active');
                node.click(); // 联动改变详情
            } else if (num < stepNum) {
                node.classList.add('completed');
            }
        });
        updateTopologyLines(stepNum);
    }

    function simLoop() {
        if (!simRunning) return;

        const currentStep = terminalStepsData[simStepIndex];

        if (simLogIndex < currentStep.logs.length) {
            const logText = currentStep.logs[simLogIndex];
            let colorClass = '';
            if (logText.startsWith('[SYSTEM]')) colorClass = 'text-success';
            else if (logText.startsWith('[API]')) colorClass = 'text-cyan';
            else if (logText.startsWith('[RUN]')) colorClass = 'text-warning';
            else if (logText.includes('[FILE]')) colorClass = 'text-cyan';
            else if (logText.includes('🎉') || logText.includes('SUCCESS')) colorClass = 'text-success';

            appendTermLog(logText, colorClass);

            if (logText.includes('[FILE]')) {
                const match = logText.match(/'([^']+)'/);
                if (match && match[1]) {
                    addTermFile(match[1]);
                }
            }

            // 平滑累加 Token 费率
            const shareCount = currentStep.logs.length;
            simTokens += Math.round(currentStep.tokens / shareCount);
            
            // 无浮点精度误差累计
            let exactCost = 0;
            for (let i = 0; i < simStepIndex; i++) {
                exactCost += terminalStepsData[i].cost;
            }
            exactCost += (terminalStepsData[simStepIndex].cost / shareCount) * (simLogIndex + 1);
            simCost = exactCost;

            termTokens.textContent = simTokens.toLocaleString();
            termCost.textContent = `¥${simCost.toFixed(2)}`;

            simLogIndex++;
            simTimer = setTimeout(simLoop, Math.random() * 250 + 150);
        } else {
            simStepIndex++;
            simLogIndex = 0;

            if (simStepIndex < terminalStepsData.length) {
                setTopologyNodeActive(terminalStepsData[simStepIndex].stepNum);
                simTimer = setTimeout(simLoop, 600);
            } else {
                simRunning = false;
                termGaugeDot.className = "gauge-dot";
                termGaugeText.textContent = "运行完成 (工作流完全闭环)";
                terminalStartBtn.textContent = "重新运行";
                terminalResetBtn.style.display = 'inline-block';
                appendTermLog("[SUCCESS] 本地论文与竞赛打包成果物已放置于发布目录。", "text-success");
            }
        }
    }

    terminalStartBtn.addEventListener('click', () => {
        if (simStepIndex >= terminalStepsData.length) {
            resetSim();
        }

        if (!simRunning) {
            simRunning = true;
            termGaugeDot.className = "gauge-dot running";
            termGaugeText.textContent = "正在处理本地 Skills...";
            terminalStartBtn.textContent = "暂停运行";
            terminalResetBtn.style.display = 'inline-block';

            if (simStepIndex === 0 && simLogIndex === 0) {
                termLogsContainer.replaceChildren();
                appendTermLog("[SYSTEM] 初始化本地沙箱边界，建立套接字物理阻断...", "text-success");
                setTopologyNodeActive(1);
            }

            simTimer = setTimeout(simLoop, 400);
        } else {
            simRunning = false;
            termGaugeDot.className = "gauge-dot";
            termGaugeText.textContent = "已暂停";
            terminalStartBtn.textContent = "恢复运行";
            if (simTimer) clearTimeout(simTimer);
        }
    });

    terminalResetBtn.addEventListener('click', () => {
        resetSim();
    });

    function resetSim() {
        simRunning = false;
        simStepIndex = 0;
        simLogIndex = 0;
        simTokens = 0;
        simCost = 0.00;
        if (simTimer) clearTimeout(simTimer);

        termGaugeDot.className = "gauge-dot";
        termGaugeText.textContent = "就绪 (DPAPI 加密保护)";
        terminalStartBtn.textContent = "启动工作流";
        terminalResetBtn.style.display = 'none';

        termTokens.textContent = "0";
        termCost.textContent = "¥0.00";

        termFileTree.replaceChildren();
        if (termEmptyTreeMsg) {
            termEmptyTreeMsg.style.display = 'block';
            termFileTree.appendChild(termEmptyTreeMsg);
        }

        termLogsContainer.replaceChildren();
        appendTermLog("// 首次启动处于“API 尚未配置”状态，请配置中转站后运行", "text-muted");
        appendTermLog("[SYSTEM] 本地环境审计完成。所有已知外部遥测域名已被底层 Socket 阻断。", "text-success");

        topologyNodes.forEach(node => {
            node.classList.remove('active', 'completed');
        });
        topologyNodes[0].classList.add('active');
        topologyNodes[0].click();
        updateTopologyLines(1);
    }


    /* ==========================================================================
       5. 实时算力计费估算 (Calculator Slider Engine)
       ========================================================================== */
    const sliderTokensInput = document.getElementById('slider-tokens-input');
    const sliderPriceInput = document.getElementById('slider-price-input');
    const valTokens = document.getElementById('val-tokens');
    const valPrice = document.getElementById('val-price');
    const calcTotalCost = document.getElementById('calc-total-cost');
    const calcUsdCost = document.getElementById('calc-usd-cost');
    const calcStepCost = document.getElementById('calc-step-cost');

    function updateCalculator() {
        const tokens = parseInt(sliderTokensInput.value);
        const price = parseFloat(sliderPriceInput.value);

        valTokens.textContent = tokens.toLocaleString();
        valPrice.textContent = `${price.toFixed(1)} 元`;

        // 费率公式
        const total = (tokens / 1000000) * price;
        const totalUsd = total / 7.25;
        const stepAverage = total / 9;

        calcTotalCost.textContent = `¥${total.toFixed(2)}`;
        calcUsdCost.textContent = `$${totalUsd.toFixed(2)}`;
        
        // 动态展示极微小单步费率精度
        calcStepCost.textContent = stepAverage < 0.01 ? `¥${stepAverage.toFixed(4)}` : `¥${stepAverage.toFixed(2)}`;

        // 行星轮滑轨色彩渲染
        const tokensPct = (tokens - 50000) / (1000000 - 50000) * 100;
        sliderTokensInput.style.background = `linear-gradient(to right, var(--accent-clay) 0%, var(--accent-brass) ${tokensPct}%, var(--text-muted) ${tokensPct}%, var(--text-muted) 100%)`;

        const priceMin = parseFloat(sliderPriceInput.min || 0.1);
        const priceMax = parseFloat(sliderPriceInput.max || 100);
        const pricePct = (price - priceMin) / (priceMax - priceMin) * 100;
        sliderPriceInput.style.background = `linear-gradient(to right, var(--accent-clay) 0%, var(--accent-brass) ${pricePct}%, var(--text-muted) ${pricePct}%, var(--text-muted) 100%)`;
    }

    if (sliderTokensInput && sliderPriceInput) {
        sliderTokensInput.addEventListener('input', updateCalculator);
        sliderPriceInput.addEventListener('input', updateCalculator);
        updateCalculator();
    }
});
