// static/js/main.js - Interactive Features

// Smooth scroll to top
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Show scroll to top button when scrolling
window.addEventListener('scroll', function() {
    const scrollBtn = document.getElementById('scrollTopBtn');
    if (scrollBtn) {
        if (window.scrollY > 300) {
            scrollBtn.classList.add('show');
        } else {
            scrollBtn.classList.remove('show');
        }
    }
});

// Add scroll to top button
document.addEventListener('DOMContentLoaded', function() {
    const btn = document.createElement('button');
    btn.id = 'scrollTopBtn';
    btn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    btn.className = 'scroll-top-btn';
    btn.onclick = scrollToTop;
    document.body.appendChild(btn);
    
    // Add styles for scroll button
    const style = document.createElement('style');
    style.textContent = `
        .scroll-top-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: linear-gradient(135deg, #2d7aff, #8a6eff);
            color: white;
            border: none;
            cursor: pointer;
            display: none;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            box-shadow: 0 5px 20px rgba(45, 122, 255, 0.3);
            transition: all 0.3s ease;
            z-index: 1000;
        }
        
        .scroll-top-btn.show {
            display: flex;
        }
        
        .scroll-top-btn:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(45, 122, 255, 0.5);
        }
    `;
    document.head.appendChild(style);
});

// Copy text to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showNotification('Copied to clipboard!', 'success');
    }).catch(function() {
        showNotification('Failed to copy', 'error');
    });
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} animate__animated animate__fadeInRight`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('animate__fadeOutRight');
        setTimeout(() => notification.remove(), 500);
    }, 3000);
}

// Add notification styles
const notificationStyle = document.createElement('style');
notificationStyle.textContent = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        border-radius: 10px;
        background: #1e2429;
        color: white;
        border-left: 4px solid;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 500;
    }
    
    .notification-success {
        border-left-color: #2ecc71;
    }
    
    .notification-error {
        border-left-color: #e74c3c;
    }
    
    .notification-info {
        border-left-color: #2d7aff;
    }
`;
document.head.appendChild(notificationStyle);

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    for (let input of inputs) {
        if (!input.value.trim()) {
            input.classList.add('error');
            showNotification(`${input.name || 'Field'} is required`, 'error');
            return false;
        }
    }
    return true;
}

// File upload preview
function previewFile(input) {
    if (input.files && input.files[0]) {
        const fileName = input.files[0].name;
        const preview = document.getElementById('filePreview');
        if (preview) {
            preview.innerHTML = `
                <div class="file-info">
                    <i class="fas fa-file-csv"></i>
                    <span>${fileName}</span>
                    <small>(${(input.files[0].size / 1024).toFixed(2)} KB)</small>
                </div>
            `;
        }
    }
}

// Add ripple effect to buttons
document.addEventListener('click', function(e) {
    const button = e.target.closest('.btn');
    if (!button) return;
    
    const ripple = document.createElement('span');
    ripple.className = 'ripple';
    
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = (e.clientX - rect.left - size/2) + 'px';
    ripple.style.top = (e.clientY - rect.top - size/2) + 'px';
    
    button.appendChild(ripple);
    
    setTimeout(() => ripple.remove(), 600);
});

// Add ripple styles
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    .btn {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(rippleStyle);

// Dark mode toggle (if needed)
function toggleDarkMode() {
    document.body.classList.toggle('light-mode');
    const isLight = document.body.classList.contains('light-mode');
    localStorage.setItem('lightMode', isLight);
}

// Check for saved preference
if (localStorage.getItem('lightMode') === 'true') {
    document.body.classList.add('light-mode');
}