// Main JavaScript file for common functionality

// CAPTCHA generation and validation - Visual Image Selection CAPTCHA
let currentCaptcha = { 
    challenge: '', 
    correctIndices: [], 
    selectedIndices: [],
    images: []
};
let captchaAttempts = 0;
const MAX_CAPTCHA_REDOS = Infinity; // Allow unlimited redos

// CAPTCHA image categories and emojis
const captchaCategories = {
    'books': { emoji: '📚', items: ['📚', '📖', '📕', '📗', '📘', '📙', '📓', '📔'] },
    'vehicles': { emoji: '🚗', items: ['🚗', '🚕', '🚙', '🚌', '🚎', '🏎️', '🚓', '🚑'] },
    'animals': { emoji: '🐶', items: ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼'] },
    'food': { emoji: '🍎', items: ['🍎', '🍌', '🍇', '🍊', '🍋', '🍉', '🍓', '🍑'] },
    'sports': { emoji: '⚽', items: ['⚽', '🏀', '🏈', '⚾', '🎾', '🏐', '🏉', '🎱'] },
    'electronics': { emoji: '💻', items: ['💻', '📱', '⌚', '🖥️', '⌨️', '🖱️', '📷', '📹'] },
    'nature': { emoji: '🌳', items: ['🌳', '🌲', '🌴', '🌵', '🌿', '🍀', '🌱', '🌾'] },
    'shapes': { emoji: '🔷', items: ['🔷', '🔶', '🔸', '🔹', '⬛', '⬜', '🔴', '🔵'] }
};

function refreshCaptcha() {
    // Refresh without incrementing redo attempts - used only for initial refresh button
    generateCaptcha(false);
}

function generateCaptcha(isRedo = false) {
    // Check if user has exceeded redo limit (only for redos, not initial generation)
    if (isRedo && captchaAttempts >= MAX_CAPTCHA_REDOS) {
        const refreshBtn = document.querySelector('.btn-refresh-captcha');
        if (refreshBtn) {
            refreshBtn.disabled = true;
            refreshBtn.style.opacity = '0.5';
            refreshBtn.style.cursor = 'not-allowed';
        }
        return;
    }
    
    // Increment attempts only if this is a redo
    if (isRedo) {
        captchaAttempts++;
    }
    
    // Select random category
    const categories = Object.keys(captchaCategories);
    const selectedCategory = categories[Math.floor(Math.random() * categories.length)];
    const categoryData = captchaCategories[selectedCategory];
    
    // Create grid of 9 images (3x3)
    const allItems = categoryData.items;
    const correctItems = [...allItems].sort(() => Math.random() - 0.5).slice(0, 4); // 4 correct items
    const wrongItems = Object.values(captchaCategories)
        .flatMap(cat => cat.items)
        .filter(item => !allItems.includes(item))
        .sort(() => Math.random() - 0.5)
        .slice(0, 5); // 5 wrong items
    
    // Mix correct and wrong items
    const mixedItems = [...correctItems, ...wrongItems].sort(() => Math.random() - 0.5);
    
    // Find indices of correct items in the mixed array
    const correctIndices = [];
    mixedItems.forEach((item, index) => {
        if (correctItems.includes(item)) {
            correctIndices.push(index);
        }
    });
    
    currentCaptcha = {
        challenge: `Select all ${selectedCategory}`,
        correctIndices: correctIndices.sort((a, b) => a - b),
        selectedIndices: [],
        images: mixedItems,
        category: selectedCategory
    };
    
    // Render CAPTCHA
    renderCaptcha();
}

function renderCaptcha() {
    const instructionEl = document.getElementById('captchaInstruction');
    const imagesEl = document.getElementById('captchaImages');
    const selectedEl = document.getElementById('captchaSelected');
    const refreshBtn = document.querySelector('.btn-refresh-captcha');
    
    if (instructionEl) {
        instructionEl.textContent = `Select all ${currentCaptcha.category}:`;
    }
    
    if (imagesEl) {
        imagesEl.innerHTML = '';
        currentCaptcha.images.forEach((emoji, index) => {
            const isSelected = currentCaptcha.selectedIndices.includes(index);
            const imgDiv = document.createElement('div');
            imgDiv.className = `captcha-image-item ${isSelected ? 'selected' : ''}`;
            imgDiv.textContent = emoji;
            imgDiv.onclick = () => toggleCaptchaSelection(index);
            imagesEl.appendChild(imgDiv);
        });
    }
    
    if (selectedEl) {
        const selectedCount = currentCaptcha.selectedIndices.length;
        const correctCount = currentCaptcha.correctIndices.length;
        let statusText = `Selected: ${selectedCount} / ${correctCount} required`;
        selectedEl.textContent = statusText;
        selectedEl.className = selectedCount === correctCount ? 'captcha-selected correct' : 'captcha-selected';
    }
    
    // Refresh button always stays enabled since we have unlimited redos
    if (refreshBtn) {
        refreshBtn.disabled = false;
        refreshBtn.style.opacity = '1';
        refreshBtn.style.cursor = 'pointer';
    }
}

function toggleCaptchaSelection(index) {
    const idx = currentCaptcha.selectedIndices.indexOf(index);
    if (idx > -1) {
        currentCaptcha.selectedIndices.splice(idx, 1);
    } else {
        currentCaptcha.selectedIndices.push(index);
    }
    currentCaptcha.selectedIndices.sort((a, b) => a - b);
    renderCaptcha();
}

function validateCaptcha() {
    // Check if CAPTCHA is initialized
    if (!currentCaptcha || !currentCaptcha.correctIndices || currentCaptcha.correctIndices.length === 0) {
        console.error('CAPTCHA not initialized');
        return false;
    }
    
    // Check if selected indices match correct indices exactly
    if (currentCaptcha.selectedIndices.length !== currentCaptcha.correctIndices.length) {
        return false;
    }
    
    const selected = [...currentCaptcha.selectedIndices].sort((a, b) => a - b);
    const correct = [...currentCaptcha.correctIndices].sort((a, b) => a - b);
    
    // Must match exactly
    if (selected.length !== correct.length) {
        return false;
    }
    
    return selected.every((val, idx) => val === correct[idx]);
}

// Validate nickname appropriateness
function validateNickname(nickname) {
    if (!nickname || nickname.trim().length < 2) {
        return { valid: false, error: 'Nickname must be at least 2 characters long' };
    }
    
    if (nickname.length > 30) {
        return { valid: false, error: 'Nickname must be 30 characters or less' };
    }
    
    // Comprehensive list of offensive words
    const inappropriateWords = [
        // Swear words
        'arse', 'arsehead', 'arsehole', 'ass', 'asshole', 'ass hole',
        'bastard', 'bitch', 'bloody', 'bollocks', 'brotherfucker', 'bugger', 'bullshit',
        'child-fucker', 'cock', 'cocksucker', 'crap', 'cunt',
        'dammit', 'damn', 'damned', 'damn it', 'dick', 'dick-head', 'dickhead', 'dumb ass', 'dumb-ass', 'dumbass', 'dyke',
        'fag', 'faggot', 'father-fucker', 'fatherfucker', 'fuck', 'fucked', 'fucker', 'fucking',
        'god dammit', 'goddammit', 'god damn', 'goddamn', 'goddamned', 'goddamnit', 'godsdamn',
        'hell', 'holy shit', 'horseshit',
        'jackarse', 'jack-ass', 'jackass', 'jesus christ', 'jesus fuck', 'jesus harold christ', 'jesus h. christ', 'jesus wept',
        'kike',
        'mental',
        'mother fucker', 'mother-fucker', 'motherfucker',
        'nigger', 'nigga', 'nigra',  // n-word and variants
        'pigfucker', 'piss', 'prick', 'pussy',
        'shit', 'shit ass', 'shite', 'sibling fucker', 'sisterfuck', 'sisterfucker', 'slut', 'son of a bitch', 'son of a whore', 'spastic', 'sweet jesus',
        'tranny', 'twat',
        'wanker',
        // Additional offensive terms
        'admin', 'administrator', 'moderator', 'mod', 'root',
        'nazi', 'hitler', 'kill', 'death', 'murder', 'hate'
    ];
    
    const nicknameLower = nickname.toLowerCase();
    // Create a version with numbers removed to catch leetspeak variants
    const nicknameStripped = nicknameLower.replace(/[0-9]/g, '');
    
    // Check for inappropriate words
    for (const word of inappropriateWords) {
        // Check if word appears in nickname directly
        if (nicknameLower.includes(word)) {
            return { valid: false, error: 'Nickname contains inappropriate content' };
        }
        // Also check with numbers stripped (catches n1gger, n1gga, etc.)
        if (nicknameStripped.includes(word)) {
            return { valid: false, error: 'Nickname contains inappropriate content' };
        }
    }
    
    // Additional check for common leetspeak variants of offensive words
    // Replace numbers with letters that sound similar and check again
    let nicknameLeetspeak = nicknameLower
        .replace(/[1!]/g, 'i')
        .replace(/[3]/g, 'e')
        .replace(/[4]/g, 'a')
        .replace(/[5]/g, 's')
        .replace(/[7]/g, 't')
        .replace(/[0]/g, 'o');
    
    for (const word of inappropriateWords) {
        if (nicknameLeetspeak.includes(word)) {
            return { valid: false, error: 'Nickname contains inappropriate content' };
        }
    }
    
    // Check pattern (only letters, numbers, spaces, dots, dashes, underscores)
    const pattern = /^[A-Za-z0-9\s\.\-_]+$/;
    if (!pattern.test(nickname)) {
        return { valid: false, error: 'Nickname can only contain letters, numbers, spaces, dots, dashes, and underscores' };
    }
    
    return { valid: true };
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Initialize CAPTCHA when login modal opens
document.addEventListener('DOMContentLoaded', function() {
    // Generate CAPTCHA on page load
    if (document.getElementById('captchaChallenge')) {
        generateCaptcha();
    }
    
    
    // Handle login form submission
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const email = document.getElementById('loginEmail').value.trim();
            const nickname = document.getElementById('loginNickname').value.trim();
            const errorDiv = document.getElementById('loginError');
            
            // Clear previous errors
            if (errorDiv) {
                errorDiv.style.display = 'none';
                errorDiv.textContent = '';
            }
            
            // Validate email
            if (!email || !email.endsWith('@lehigh.edu')) {
                if (errorDiv) {
                    errorDiv.textContent = 'Please use a valid Lehigh email address (@lehigh.edu)';
                    errorDiv.style.display = 'block';
                }
                return;
            }
            
            // Validate nickname FIRST - show immediate feedback
            const nicknameValidation = validateNickname(nickname);
            if (!nicknameValidation.valid) {
                if (errorDiv) {
                    errorDiv.textContent = nicknameValidation.error;
                    errorDiv.style.display = 'block';
                }
                return;
            }
            
            // Validate CAPTCHA - STRICT: Must be correct to proceed
            if (!validateCaptcha()) {
                captchaAttempts++;
                
                if (errorDiv) {
                    errorDiv.textContent = 'CAPTCHA verification failed. Please select all correct images and try again.';
                    errorDiv.style.display = 'block';
                }
                // Reset selection but keep same challenge
                currentCaptcha.selectedIndices = [];
                renderCaptcha();
                return; // BLOCK LOGIN - Must solve correctly
            }
            
            // Reset attempts on successful validation
            captchaAttempts = 0;
            
            // Submit CAPTCHA to server first to store it in session
            try {
                const captchaStoreResponse = await fetch('/api/auth/captcha', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        challenge: currentCaptcha.challenge,
                        correctIndices: currentCaptcha.correctIndices
                    })
                });
                
                const captchaStoreData = await captchaStoreResponse.json();
                if (!captchaStoreData.success) {
                    if (errorDiv) {
                        errorDiv.textContent = 'Failed to store CAPTCHA. Please try again.';
                        errorDiv.style.display = 'block';
                    }
                    return;
                }
            } catch (error) {
                console.error('CAPTCHA store error:', error);
                if (errorDiv) {
                    errorDiv.textContent = 'Network error storing CAPTCHA. Please try again.';
                    errorDiv.style.display = 'block';
                }
                return;
            }
            
            // Submit login to server
            try {
                const response = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        email, 
                        nickname,
                        captcha_question: currentCaptcha.challenge,
                        captcha_answer: currentCaptcha.selectedIndices.join(',')
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    // Store user info
                    localStorage.setItem('userEmail', email);
                    localStorage.setItem('userNickname', nickname);
                    
                    // Close modal
                    const modal = document.getElementById('loginModal');
                    if (modal) {
                        modal.style.display = 'none';
                    }
                    
                    // Update UI
                    const loginBtn = document.querySelector('.btn-login');
                    if (loginBtn) {
                        loginBtn.textContent = nickname;
                    }
                    
                    // Show success message
                    if (typeof showNotification === 'function') {
                        showNotification('Login successful!', 'success');
                    }
                    
                    // Reload page to update state
                    setTimeout(() => {
                        window.location.reload();
                    }, 500);
                } else {
                    if (errorDiv) {
                        errorDiv.textContent = data.error || 'Login failed. Please try again.';
                        errorDiv.style.display = 'block';
                    } else {
                        alert(data.error || 'Login failed. Please try again.');
                    }
                }
            } catch (error) {
                console.error('Login error:', error);
                if (errorDiv) {
                    errorDiv.textContent = 'Network error. Please try again.';
                    errorDiv.style.display = 'block';
                } else {
                    alert('Network error. Please try again.');
                }
            }
        });
    }
});

// Utility function to show notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'error' ? '#1a1a1a' : type === 'success' ? '#1a1a1a' : '#1a1a1a'};
        color: #ffffff;
        padding: 1rem 1.5rem;
        border: 1px solid #1a1a1a;
        font-size: 14px;
        z-index: 3000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Modal functions
function showLoginModal() {
    const modal = document.getElementById('loginModal');
    if (modal) {
        modal.style.display = 'flex';
        // Reset form
        const form = document.getElementById('loginForm');
        if (form) {
            form.reset();
        }
        const errorDiv = document.getElementById('loginError');
        if (errorDiv) {
            errorDiv.style.display = 'none';
            errorDiv.textContent = '';
        }
        // Reset CAPTCHA attempts
        captchaAttempts = 0;
        const refreshBtn = document.querySelector('.btn-refresh-captcha');
        if (refreshBtn) {
            refreshBtn.disabled = false;
            refreshBtn.textContent = '↻';
            refreshBtn.style.opacity = '1';
            refreshBtn.style.cursor = 'pointer';
        }
        const submitBtn = form ? form.querySelector('button[type="submit"]') : null;
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Login / Sign Up';
            submitBtn.style.opacity = '1';
            submitBtn.style.cursor = 'pointer';
        }
        // Generate fresh CAPTCHA
        generateCaptcha(false);
    }
}

function closeLoginModal() {
    const modal = document.getElementById('loginModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Other modal functions
function showAddClassModal() {
    const modal = document.getElementById('addClassModal');
    if (modal) {
        modal.style.display = 'flex';
        const form = document.getElementById('addClassForm');
        if (form) {
            form.reset();
        }
    }
}

function closeModal() {
    const modal = document.getElementById('addClassModal');
    if (modal) {
        modal.style.display = 'none';
    }
}
