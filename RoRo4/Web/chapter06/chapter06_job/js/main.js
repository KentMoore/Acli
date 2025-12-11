// 页面功能
document.addEventListener('DOMContentLoaded', function() {
    // 轮播图功能
    const slides = document.querySelectorAll('.carousel-slide');
    const dots = document.querySelectorAll('.dot');
    const prevBtn = document.querySelector('.carousel-prev');
    const nextBtn = document.querySelector('.carousel-next');
    let currentSlide = 0;

    function showSlide(index) {
        slides.forEach(slide => slide.classList.remove('active'));
        dots.forEach(dot => dot.classList.remove('active'));
        
        slides[index].classList.add('active');
        dots[index].classList.add('active');
        currentSlide = index;
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }

    function prevSlide() {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(currentSlide);
    }

    // 点击圆点切换
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => showSlide(index));
    });

    // 箭头按钮事件
    nextBtn.addEventListener('click', nextSlide);
    prevBtn.addEventListener('click', prevSlide);

    // 自动轮播
    setInterval(nextSlide, 3000);

    // 获取真实视频时长
    function formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }

    function updateVideoDuration() {
        const videoCards = document.querySelectorAll('.video-card');
        
        videoCards.forEach(card => {
            const video = card.querySelector('.video-preview');
            const durationElement = card.querySelector('.video-duration');
            
            video.addEventListener('loadedmetadata', function() {
                if (video.duration && !isNaN(video.duration)) {
                    durationElement.textContent = formatTime(video.duration);
                }
            });
            
            // 如果视频已经加载完成
            if (video.readyState >= 1) {
                durationElement.textContent = formatTime(video.duration);
            }
        });
    }

    // 初始化视频时长
    updateVideoDuration();

    // 视频控制功能
    const videoCards = document.querySelectorAll('.video-card');
    
    videoCards.forEach(card => {
        const video = card.querySelector('.video-preview');
        const playBtn = card.querySelector('.play-btn');
        const volumeBtn = card.querySelector('.volume-btn');
        const fullscreenBtn = card.querySelector('.fullscreen-btn');
        const settingsBtn = card.querySelector('.settings-btn');
        
        let isPlaying = false;
        
        // 播放/暂停按钮
        playBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            if (isPlaying) {
                video.pause();
                playBtn.textContent = '▶';
            } else {
                video.play().catch(err => console.log('播放失败:', err));
                playBtn.textContent = '⏸';
            }
            isPlaying = !isPlaying;
        });
        
        // 初始化声音按钮状态
        volumeBtn.textContent = video.muted ? '🔇' : '🔊';
        
        // 声音按钮
        volumeBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            video.muted = !video.muted;
            volumeBtn.textContent = video.muted ? '🔇' : '🔊';
            // 如果开启声音，确保视频在播放
            if (!video.muted && !isPlaying) {
                video.play().catch(err => console.log('播放失败:', err));
                playBtn.textContent = '⏸';
                isPlaying = true;
            }
        });
        
        // 全屏按钮
        fullscreenBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            if (video.requestFullscreen) {
                video.requestFullscreen();
            } else if (video.webkitRequestFullscreen) {
                video.webkitRequestFullscreen();
            } else if (video.mozRequestFullScreen) {
                video.mozRequestFullScreen();
            }
        });
        
        // 设置按钮
        settingsBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            alert('设置功能');
        });
        
        // 鼠标悬停时自动播放预览
        card.addEventListener('mouseenter', function() {
            if (!isPlaying && video) {
                video.play().catch(err => console.log('自动播放失败:', err));
            }
        });
        
        // 鼠标离开时暂停
        card.addEventListener('mouseleave', function() {
            if (!isPlaying && video) {
                video.pause();
                video.currentTime = 0;
            }
        });
    });
    
    // 标签切换功能
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // 导航菜单切换
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            navItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // 搜索功能
    const searchInput = document.querySelector('.search-box input');
    const searchBtn = document.querySelector('.search-btn');
    
    searchBtn.addEventListener('click', function() {
        const searchTerm = searchInput.value.trim();
        if (searchTerm) {
            console.log('搜索:', searchTerm);
            // 这里可以添加实际的搜索逻辑
        }
    });
    
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchBtn.click();
        }
    });
});
