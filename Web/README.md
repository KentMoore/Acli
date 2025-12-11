# 我的兴趣爱好 - 个人展示网站

> 一个以"我的兴趣爱好"为主题的前端静态网站，用于展示个人在大数据、编程、游戏、音乐方面的兴趣。

**作者信息**：班级：24大数据1班 | 学号：241903440120 | 姓名：赖锦添

---

## 📁 项目结构

```
Web/
├── index.html          # 首页
├── detail.html         # 兴趣详情页
├── about.html          # 关于我 / 联系方式页
├── css/
│   └── style.css       # 全局样式 (1277行)
├── js/
│   └── main.js         # 主逻辑脚本 (596行)
├── images/             # AI 生成的主题图片
│   ├── hobby-coding.png
│   ├── hobby-game.png
│   ├── hobby-music.png
│   └── hobby-life.png
└── README.md           # 本文档
```

---

## ✨ 功能特性一览

| 功能 | 页面 | 实现方式 |
|------|------|----------|
| 打字机效果 | 首页 | JavaScript 定时器循环 |
| 粒子背景动画 | 首页 | Canvas + requestAnimationFrame |
| Web 终端模拟器 | 首页 | 键盘事件监听 + 命令解析 |
| 数字增长动画 | 首页 | IntersectionObserver + 缓动函数 |
| 滚动显现动画 | 全站 | IntersectionObserver + CSS transition |
| 兴趣 Tabs 切换 | 详情页 | data-target 属性 + classList 切换 |
| FAQ 折叠面板 | 关于页 | 手风琴效果 + max-height 动画 |
| 联系表单验证 | 关于页 | FormData API + 前端验证 |
| 回到顶部按钮 | 全站 | scroll 事件节流 + 平滑滚动 |
| 平滑锚点跳转 | 全站 | scrollIntoView({ behavior: 'smooth' }) |
| 故障文字特效 | 首页 | CSS clip-path + keyframes 动画 |

---

## 🎨 动画特效实现详解

### 1. 粒子背景动画 (Particle Network)

**文件**：`js/main.js` - `initParticles()` 函数 (第 511-596 行)

**原理**：使用 HTML5 Canvas 创建粒子系统，粒子在画布上随机运动，当两个粒子距离小于阈值时绘制连线。

```javascript
// 核心逻辑
class Particle {
    constructor() {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.vx = (Math.random() - 0.5) * moveSpeed;  // 随机速度
        this.vy = (Math.random() - 0.5) * moveSpeed;
    }
    update() {
        this.x += this.vx;
        this.y += this.vy;
        // 边界反弹
        if (this.x < 0 || this.x > width) this.vx *= -1;
        if (this.y < 0 || this.y > height) this.vy *= -1;
    }
}

// 动画循环
function animate() {
    ctx.clearRect(0, 0, width, height);
    particles.forEach((p, index) => {
        p.update();
        p.draw();
        // 绘制粒子间连线
        for (let j = index + 1; j < particles.length; j++) {
            const distance = Math.sqrt(dx*dx + dy*dy);
            if (distance < connectionDistance) {
                ctx.strokeStyle = `rgba(148, 163, 184, ${0.15 * (1 - distance/connectionDistance)})`;
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.stroke();
            }
        }
    });
    requestAnimationFrame(animate);
}
```

**CSS 配置**（style.css 第 114-125 行）：
```css
#hero-canvas {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 0;
    pointer-events: none;  /* 不阻挡鼠标点击 */
}
```

---

### 2. 滚动显现动画 (Scroll Reveal)

**文件**：`js/main.js` - `initScrollReveal()` 函数 (第 385-404 行)

**原理**：使用 IntersectionObserver API 监听元素进入视口，添加 `.active` 类触发 CSS 过渡动画。

```javascript
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add("active");
            observer.unobserve(entry.target);  // 只触发一次
        }
    });
}, {
    threshold: 0.1,  // 元素进入 10% 时触发
    rootMargin: "0px 0px -50px 0px"  // 延迟触发
});

document.querySelectorAll(".reveal").forEach(el => observer.observe(el));
```

**CSS 配置**（style.css 第 1096-1120 行）：
```css
.reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.8s cubic-bezier(0.5, 0, 0, 1);
}
.reveal.active {
    opacity: 1;
    transform: translateY(0);
}
/* 错峰延迟 */
.reveal-delay-100 { transition-delay: 0.1s; }
.reveal-delay-200 { transition-delay: 0.2s; }
```

---

### 3. 故障文字特效 (Glitch Effect)

**文件**：`css/style.css` (第 230-431 行)

**原理**：使用 `::before` 和 `::after` 伪元素复制文字，通过 `clip` 属性裁剪不同区域，配合 keyframes 动画产生抖动效果。

```css
.glitch {
    position: relative;
    color: var(--text-white);
}
.glitch::before, .glitch::after {
    content: attr(data-text);  /* 复制文字 */
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
}
.glitch::before {
    left: 2px;
    text-shadow: -1px 0 #ff00c1;
    animation: glitch-anim 5s infinite linear alternate-reverse;
}
.glitch::after {
    left: -2px;
    text-shadow: -1px 0 #00fff9;
    animation: glitch-anim2 5s infinite linear alternate-reverse;
}

@keyframes glitch-anim {
    0% { clip: rect(33px, 9999px, 11px, 0); }
    5% { clip: rect(78px, 9999px, 94px, 0); }
    /* ... 更多关键帧 */
}
```

---

### 4. 数字增长动画 (Counter Animation)

**文件**：`js/main.js` - `initStatsAnimation()` 函数 (第 259-305 行)

**原理**：使用 `requestAnimationFrame` 配合缓动函数 (Ease Out Quad) 实现平滑的数字递增。

```javascript
function animate() {
    statNumbers.forEach((el) => {
        const target = Number(el.getAttribute("data-target"));
        const duration = 1500;
        const startTime = performance.now();

        function update(now) {
            const progress = Math.min(1, (now - startTime) / duration);
            // Ease Out Quad 缓动
            const easeProgress = 1 - (1 - progress) * (1 - progress);
            el.textContent = Math.floor(easeProgress * target);
            if (progress < 1) requestAnimationFrame(update);
        }
        requestAnimationFrame(update);
    });
}
```

---

## 🔗 点击跳转实现

### 平滑锚点滚动

**文件**：`js/main.js` - `initScrollInteractions()` 函数 (第 86-139 行)

```javascript
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            e.preventDefault();
            targetElement.scrollIntoView({ behavior: 'smooth' });
            history.pushState(null, null, targetId);  // 更新 URL
            targetElement.focus({ preventScroll: true });  // 无障碍支持
        }
    });
});
```

### 回到顶部按钮

```javascript
// 节流处理，100ms 内只触发一次
window.addEventListener("scroll", throttle(() => {
    if (window.scrollY > 280) {
        backToTopBtn.classList.add("show");
    } else {
        backToTopBtn.classList.remove("show");
    }
}, 100));

backToTopBtn.addEventListener("click", (e) => {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: "smooth" });
});
```

---

## 🖥️ Web 终端模拟器

**文件**：`js/main.js` - `initTerminal()` 函数 (第 410-505 行)

支持的命令：
| 命令 | 功能 |
|------|------|
| `help` | 显示帮助信息 |
| `about` | 个人简介 |
| `skills` | 技能列表 |
| `contact` | 联系方式 |
| `date` | 当前日期 |
| `clear` | 清屏 |

---

## 🎛️ Tabs 切换与 FAQ 折叠

### Tabs 切换（详情页）

```javascript
// 通过 data-target 属性关联
tab.addEventListener("click", () => {
    tabs.forEach(t => t.classList.remove("active"));
    panels.forEach(p => p.classList.remove("active"));
    tab.classList.add("active");
    document.getElementById(tab.dataset.target).classList.add("active");
});
```

### FAQ 手风琴效果

```css
.faq-answer {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.22s ease;
}
.faq-item.open .faq-answer {
    max-height: 200px;
}
```

---

## 🛠️ 技术栈

- **HTML5** - 语义化标签
- **CSS3** - 变量、Grid、Flexbox、动画
- **JavaScript ES6+** - 模块化函数、IntersectionObserver、Canvas API
- **无框架依赖** - 纯原生实现

---

## 📱 响应式设计

- 使用 CSS Grid 和 Flexbox 布局
- 媒体查询适配移动端
- 视口宽度 1200px，移动端自动缩放

---

## 🚀 快速开始

1. 克隆或下载项目
2. 用浏览器打开 `index.html` 即可预览
3. 无需任何编译或构建步骤

---

## 📄 许可

本项目仅用于学习和作业展示。
