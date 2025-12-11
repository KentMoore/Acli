// 主程序入口：当 DOM 加载完成后执行
document.addEventListener('DOMContentLoaded', () => {
    initTypewriter();
    initScrollInteractions();
    initLearningDays();
    initTabs();
    initCaseSimulation();
    initStatsAnimation();
    initFaq();
    initContactForm();
    initScrollReveal();
    initTerminal();
    initParticles();    // 新增：粒子特效
});

// --- 功能模块定义 ---

/**
 * 1. 打字机效果
 * 生效页面：任何包含 #typed-text 的页面
 */
function initTypewriter() {
    const typedTextEl = document.getElementById("typed-text");
    if (!typedTextEl) return;

    // 如果页面上有终端，打字机可以简化或只显示一句，避免视觉冲突
    // 这里保持原样，也可以修改文案
    const lines = [
        "· 喜欢折腾大数据全家桶：Hadoop / Hive / Spark / Flink",
        "· 用代码把想法变成现实",
        "· 在数据里看游戏，在游戏里找数据"
    ];
    // ... (保持原有的打字机逻辑不变，或者如果觉得太乱可以注释掉这部分的执行)
    // 为了更简洁，我们这里保留逻辑，但文案可以精简

    let lineIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    const typingDelay = 60;
    const pauseDelay = 1100;

    function typeLoop() {
        if (!isDeleting && charIndex <= lines[lineIndex].length) {
            const currentLine = lines[lineIndex].slice(0, charIndex);
            charIndex++;
            typedTextEl.textContent = currentLine;
            setTimeout(typeLoop, typingDelay);
        } else if (!isDeleting && charIndex > lines[lineIndex].length) {
            isDeleting = true;
            setTimeout(typeLoop, pauseDelay);
        } else if (isDeleting && charIndex >= 0) {
            const currentLine = lines[lineIndex].slice(0, charIndex);
            charIndex--;
            typedTextEl.textContent = currentLine;
            setTimeout(typeLoop, typingDelay / 1.6);
        } else {
            isDeleting = false;
            lineIndex = (lineIndex + 1) % lines.length;
            setTimeout(typeLoop, typingDelay);
        }
    }

    typeLoop();
}

/**
 * ... (Scroll Interactions, Learning Days, Tabs, Case Simulation, Stats, FAQ, Contact Form logic remains same) ...
 * (I will only append the NEW functions below to keep the file clean in this tool call context, 
 *  but in reality, I need to make sure I don't delete the middle part. 
 *  Wait, the tool replaces specific strings. I should be careful.)
 */

// *IMPORTANT*: I will use the `replace` tool to specifically target the end of the file or insert the new functions.
// However, the user asked to "Add ... to the DOMContentLoaded ... and define their logic".
// The best way is to replace the `document.addEventListener` block to include the calls, 
// and then append the new functions at the end.

// Let's try to do it in one go if possible, or two.
// First, update the DOMContentLoaded block.


/**
 * 2. 滚动交互优化（Back To Top + 平滑滚动链接）
 * 优化点：添加了 throttle 节流，避免 scroll 事件高频触发
 */
function initScrollInteractions() {
    const backToTopBtn = document.getElementById("back-to-top");

    // 节流辅助函数
    function throttle(func, limit) {
        let inThrottle;
        return function () {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    }

    // 监听页面滚动，显示/隐藏回到顶部按钮
    if (backToTopBtn) {
        window.addEventListener("scroll", throttle(() => {
            if (window.scrollY > 280) {
                backToTopBtn.classList.add("show");
            } else {
                backToTopBtn.classList.remove("show");
            }
        }, 100)); // 100ms 节流

        // 确保点击时平滑滚动回顶部
        backToTopBtn.addEventListener("click", (e) => {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: "smooth" });
            // 将焦点移回页面顶部（如 main 或 body），方便键盘用户
            document.body.focus();
        });
    }

    // 处理所有锚点链接的平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return; // 忽略仅用于回到顶部的 # 链接

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({ behavior: 'smooth' });
                // 更新 URL hash 但不跳转
                history.pushState(null, null, targetId);
                // 聚焦目标元素以支持无障碍访问
                targetElement.focus({ preventScroll: true });
            }
        });
    });
}

/**
 * 3. 学习天数计算
 * 生效页面：首页
 */
function initLearningDays() {
    const learningDaysSpan = document.getElementById("learning-days");
    if (!learningDaysSpan) return;

    const startDate = new Date("2024-09-01");
    const today = new Date();
    const diffTime = today.getTime() - startDate.getTime();
    const diffDays = Math.max(1, Math.floor(diffTime / (1000 * 60 * 60 * 24)));
    learningDaysSpan.textContent = diffDays;
}

/**
 * 4. 兴趣 Tabs
 * 优化点：添加 ARIA 属性增强无障碍访问 (WAI-ARIA)
 */
function initTabs() {
    const tabList = document.querySelector(".hobby-tabs");
    const tabs = document.querySelectorAll(".hobby-tab");
    const panels = document.querySelectorAll(".hobby-panel");

    if (!tabList || tabs.length === 0) return;

    // 设置容器角色
    tabList.setAttribute("role", "tablist");

    tabs.forEach((tab, index) => {
        const targetId = tab.getAttribute("data-target");
        const panel = document.getElementById(targetId);

        // 设置 Tab 角色和属性
        tab.setAttribute("role", "tab");
        tab.setAttribute("aria-selected", tab.classList.contains("active"));
        tab.setAttribute("aria-controls", targetId);
        tab.setAttribute("id", `tab-control-${index}`);
        tab.setAttribute("tabindex", tab.classList.contains("active") ? "0" : "-1");

        // 设置 Panel 角色和属性
        if (panel) {
            panel.setAttribute("role", "tabpanel");
            panel.setAttribute("aria-labelledby", `tab-control-${index}`);
            // 初始隐藏状态通过 CSS display 控制，这里不需要 aria-hidden
        }

        // 点击事件
        tab.addEventListener("click", () => {
            switchTab(tab, tabs, panels);
        });

        // 键盘导航支持 (左右箭头切换)
        tab.addEventListener("keydown", (e) => {
            let newIndex = index;
            if (e.key === "ArrowLeft") {
                newIndex = (index - 1 + tabs.length) % tabs.length;
                tabs[newIndex].click();
                tabs[newIndex].focus();
            } else if (e.key === "ArrowRight") {
                newIndex = (index + 1) % tabs.length;
                tabs[newIndex].click();
                tabs[newIndex].focus();
            }
        });
    });
}

function switchTab(selectedTab, allTabs, allPanels) {
    const targetId = selectedTab.getAttribute("data-target");

    // 更新 Tabs 状态
    allTabs.forEach((tab) => {
        const isActive = tab === selectedTab;
        tab.classList.toggle("active", isActive);
        tab.setAttribute("aria-selected", isActive);
        tab.setAttribute("tabindex", isActive ? "0" : "-1");
    });

    // 更新 Panels 状态
    allPanels.forEach((panel) => {
        const isActive = panel.id === targetId;
        panel.classList.toggle("active", isActive);
    });
}

/**
 * 5. 模拟开箱
 * 生效页面：detail.html
 */
function initCaseSimulation() {
    const openCaseBtn = document.getElementById("open-case-btn");
    const openCaseResultEl = document.getElementById("open-case-result");

    if (!openCaseBtn || !openCaseResultEl) return;

    const caseResults = [
        "普通蓝色：还行，至少不是白给。",
        "紫色品质：有点小赚，继续冲！",
        "粉色品质：可以发个朋友圈炫耀一下。",
        "红色品质：今天的运气都在这里了！",
        "金色刀/手套：欧皇附体，恭喜！"
    ];

    openCaseBtn.addEventListener("click", () => {
        // 简单的随机逻辑
        const index = Math.floor(Math.random() * caseResults.length);
        openCaseResultEl.textContent = "开箱结果：" + caseResults[index];
        // 聚焦结果以便屏幕阅读器读取
        openCaseResultEl.setAttribute("tabindex", "-1");
        openCaseResultEl.focus();
    });
}

/**
 * 6. 数字增长动画
 * 生效页面：首页
 */
function initStatsAnimation() {
    const statNumbers = document.querySelectorAll(".stat-number");
    const statsSection = document.querySelector(".stats-strip");

    if (statNumbers.length === 0) return;

    let statsAnimated = false;

    function animate() {
        if (statsAnimated) return;
        statsAnimated = true;

        statNumbers.forEach((el) => {
            const target = Number(el.getAttribute("data-target") || "0");
            const duration = 1500;
            const startTime = performance.now();

            function update(now) {
                const progress = Math.min(1, (now - startTime) / duration);
                // 简单的缓动函数 (Ease Out Quad)
                const easeProgress = 1 - (1 - progress) * (1 - progress);

                const current = Math.floor(easeProgress * target);
                el.textContent = current;

                if (progress < 1) {
                    requestAnimationFrame(update);
                } else {
                    el.textContent = target;
                }
            }
            requestAnimationFrame(update);
        });
    }

    if (statsSection && "IntersectionObserver" in window) {
        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                animate();
                observer.disconnect();
            }
        }, { threshold: 0.3 });
        observer.observe(statsSection);
    } else {
        animate(); // 降级处理
    }
}

/**
 * 7. FAQ 折叠面板
 * 优化点：添加 ARIA 属性 (aria-expanded, aria-controls)
 */
function initFaq() {
    const faqItems = document.querySelectorAll(".faq-item");

    if (faqItems.length === 0) return;

    faqItems.forEach((item, index) => {
        const questionBtn = item.querySelector(".faq-question");
        const answerPanel = item.querySelector(".faq-answer");

        if (!questionBtn || !answerPanel) return;

        // 设置 ID 用于 aria-controls
        const panelId = `faq-ans-${index}`;
        answerPanel.setAttribute("id", panelId);

        // 设置按钮属性
        questionBtn.setAttribute("aria-expanded", "false");
        questionBtn.setAttribute("aria-controls", panelId);

        questionBtn.addEventListener("click", () => {
            const isOpen = item.classList.contains("open");

            // 关闭其他所有项（手风琴效果）
            faqItems.forEach((otherItem) => {
                otherItem.classList.remove("open");
                const otherBtn = otherItem.querySelector(".faq-question");
                if (otherBtn) otherBtn.setAttribute("aria-expanded", "false");
            });

            // 切换当前项
            if (!isOpen) {
                item.classList.add("open");
                questionBtn.setAttribute("aria-expanded", "true");
            } else {
                // 如果已经是打开的，上面的关闭逻辑已经处理了，这里只需要确保状态正确
                // (实际上上面的 forEach 已经移除了 open class)
            }
        });
    });
}

/**
 * 8. 联系表单
 * 生效页面：about.html
 */
function initContactForm() {
    const contactForm = document.getElementById("contact-form");
    const formResult = document.getElementById("form-result");

    if (!contactForm || !formResult) return;

    contactForm.addEventListener("submit", (e) => {
        e.preventDefault();
        // 使用 FormData 获取数据
        const formData = new FormData(contactForm);
        const name = formData.get("name").trim();
        const message = formData.get("message").trim();

        if (!name || !message) {
            formResult.textContent = "请至少填写称呼和想说的话（这里只做本地演示，不会真的发送）。";
            formResult.style.color = "var(--highlight)"; // 使用 CSS 变量
            return;
        }

        formResult.textContent = "已收到你的“假装提交”😊 这只是页面展示，不会真正发送到服务器。";
        formResult.style.color = "#22c55e";
        contactForm.reset();
    });
}

/**
 * 9. 滚动显现动画 (Scroll Reveal)
 * 逻辑：使用 IntersectionObserver 监听带有 .reveal 的元素
 */
function initScrollReveal() {
    const revealElements = document.querySelectorAll(".reveal");

    if (revealElements.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("active");
                // 可选：动画完成后取消监听（如果只想触发一次）
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1, // 元素进入视口 10% 时触发
        rootMargin: "0px 0px -50px 0px" // 稍微延迟一点触发
    });

    revealElements.forEach((el) => observer.observe(el));
}

/**
 * 10. 极客终端 (Web Terminal)
 * 生效页面：首页
 */
function initTerminal() {
    const terminalInput = document.getElementById("terminal-input");
    const terminalOutput = document.getElementById("terminal-output");
    const terminalWindow = document.querySelector(".terminal-window");

    if (!terminalInput || !terminalOutput) return;

    // 点击终端任意位置聚焦输入框
    if (terminalWindow) {
        terminalWindow.addEventListener("click", () => terminalInput.focus());
    }

    // 初始欢迎语
    const welcomeMsg = [
        "Welcome to My_Web_OS [Version 1.0.0]",
        "(c) 2025 Me. All rights reserved.",
        "",
        "Type 'help' to see available commands.",
        ""
    ];

    let msgIndex = 0;
    function printWelcome() {
        if (msgIndex < welcomeMsg.length) {
            addToOutput(welcomeMsg[msgIndex]);
            msgIndex++;
            setTimeout(printWelcome, 300);
        }
    }
    // 延迟一点执行，等页面加载稳当
    setTimeout(printWelcome, 800);

    // 命令处理
    terminalInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            const command = terminalInput.value.trim().toLowerCase();
            const originalCommand = terminalInput.value; // 保留原格式用于显示

            // 显示用户输入的命令
            addToOutput(`<span class="cmd-prompt">visitor@web:~$</span> ${originalCommand}`);

            // 清空输入框
            terminalInput.value = "";

            // 处理命令
            processCommand(command);

            // 自动滚动到底部
            const terminalBody = document.querySelector(".terminal-body");
            if (terminalBody) terminalBody.scrollTop = terminalBody.scrollHeight;
        }
    });

    function processCommand(cmd) {
        let response = "";
        switch (cmd) {
            case "help":
                response = `Available commands:
  <span class="cmd-keyword">about</span>    - Brief introduction
  <span class="cmd-keyword">skills</span>   - List technical skills
  <span class="cmd-keyword">contact</span>  - Show contact info
  <span class="cmd-keyword">clear</span>    - Clear terminal screen
  <span class="cmd-keyword">date</span>     - Show current date`;
                break;
            case "about":
                response = "I am a student passionate about Big Data and Backend Development.\nTrying to turn coffee into code.";
                break;
            case "skills":
                response = `[Languages]  Java, Python, SQL, JavaScript
[Big Data]   Hadoop, Hive, Spark, Flink
[Tools]      Git, Linux, Docker, VS Code`;
                break;
            case "contact":
                response = "Email: student@university.edu\nGithub: github.com/myname";
                break;
            case "clear":
                terminalOutput.innerHTML = "";
                return;
            case "date":
                response = new Date().toString();
                break;
            case "":
                return;
            default:
                response = `<span class="cmd-error">Command not found: ${cmd}</span>. Type 'help' for list.`;
        }
        addToOutput(response);
    }

    function addToOutput(html) {
        const div = document.createElement("div");
        div.className = "terminal-line";
        div.innerHTML = html;
        terminalOutput.appendChild(div);
    }
}

/**
 * 11. 粒子背景特效 (Canvas Particle Network)
 * 生效页面：首页
 */
function initParticles() {
    const canvas = document.getElementById("hero-canvas");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    let width, height;
    let particles = [];

    // 配置参数
    const particleCount = 60; // 粒子数量
    const connectionDistance = 150; // 连线距离
    const moveSpeed = 0.5; // 移动速度

    // 初始化尺寸
    function resize() {
        width = canvas.width = canvas.offsetWidth;
        height = canvas.height = canvas.offsetHeight;
    }

    window.addEventListener("resize", resize);
    resize();

    // 粒子类
    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.vx = (Math.random() - 0.5) * moveSpeed;
            this.vy = (Math.random() - 0.5) * moveSpeed;
            this.size = Math.random() * 2 + 1;
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;

            // 边界反弹
            if (this.x < 0 || this.x > width) this.vx *= -1;
            if (this.y < 0 || this.y > height) this.vy *= -1;
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = "rgba(148, 163, 184, 0.4)"; // Slate-400 with opacity
            ctx.fill();
        }
    }

    // 初始化粒子
    for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
    }

    // 动画循环
    function animate() {
        ctx.clearRect(0, 0, width, height);

        // 更新并绘制粒子
        particles.forEach((p, index) => {
            p.update();
            p.draw();

            // 绘制连线
            for (let j = index + 1; j < particles.length; j++) {
                const p2 = particles[j];
                const dx = p.x - p2.x;
                const dy = p.y - p2.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < connectionDistance) {
                    ctx.beginPath();
                    ctx.strokeStyle = `rgba(148, 163, 184, ${0.15 * (1 - distance / connectionDistance)})`;
                    ctx.lineWidth = 1;
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.stroke();
                }
            }
        });

        requestAnimationFrame(animate);
    }

    animate();
}