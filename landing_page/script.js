document.addEventListener('DOMContentLoaded', function() {
    // 汉堡菜单交互
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }
    
    // 处理hero图像的3D动画效果
    const heroImage = document.querySelector('.hero-image');
    const heroSection = document.querySelector('.hero');
    
    if (heroImage && heroSection) {
        // 初始化变换状态
        updateHeroImageTransform();
        
        // 监听滚动事件
        window.addEventListener('scroll', updateHeroImageTransform);
        
        function updateHeroImageTransform() {
            const scrollPosition = window.scrollY;
            const heroHeight = heroSection.offsetHeight;
            // 计算滚动百分比（限制在0-100%之间）
            const scrollPercentage = Math.min(scrollPosition / (heroHeight * 0.1), 1);
            
            // 根据滚动百分比计算旋转角度
            const rotateX = 10 * (1 - scrollPercentage);
            
            // 应用变换
            heroImage.style.transform = `rotateX(${rotateX}deg)`;
            
            // 当完全滚动到位时添加一个类
            if (scrollPercentage >= 1) {
                heroImage.classList.add('scrolled');
            } else {
                heroImage.classList.remove('scrolled');
            }
        }
    }
    
    // 获取GitHub Star数量
    function fetchGitHubStars() {
        const starsElement = document.querySelector('.stars-count');
        
        if (starsElement) {
            fetch('https://api.github.com/repos/AstrBotDevs/AstrBot')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    const stars = data.stargazers_count;
                    // 格式化星星数量，保留一位小数
                    let formattedStars;
                    if (stars >= 1000) {
                        formattedStars = (stars / 1000).toFixed(1) + 'k';
                    } else {
                        formattedStars = stars.toString();
                    }
                    starsElement.textContent = formattedStars;
                })
                .catch(error => {
                    console.error('获取GitHub stars失败:', error);
                    starsElement.textContent = '⭐';
                });
        }
    }
    
    // 调用函数获取星星数
    fetchGitHubStars();
    
    // 平滑滚动
    const scrollLinks = document.querySelectorAll('a[href^="#"]');
    
    scrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                // 关闭移动菜单（如果打开）
                if (navLinks.classList.contains('active')) {
                    navLinks.classList.remove('active');
                }
                
                // 平滑滚动到目标位置
                window.scrollTo({
                    top: targetElement.offsetTop - 70,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // 页面滚动时导航栏效果
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.boxShadow = 'none';
        }
    });
    
    // 动画效果
    const animateElements = document.querySelectorAll('.feature-card, .workflow-item, .use-case-card');
    
    // 简单的滚动动画
    function checkScroll() {
        animateElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < window.innerHeight - elementVisible) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    }
    
    // 初始化样式
    animateElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'all 0.6s ease';
    });
    
    // 检查初始状态
    checkScroll();
    
    // 监听滚动事件
    window.addEventListener('scroll', checkScroll);
});
