document.addEventListener('DOMContentLoaded', () => {
    // Navbar Toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    const navOptions = document.querySelector('.nav-options');

    menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        navOptions.classList.toggle('active');
    });

    // Dark Mode Toggle
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    darkModeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        darkModeToggle.textContent = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
    });

    // Language Selector (Placeholder)
    const languageSelector = document.getElementById('language-selector');
    languageSelector.addEventListener('change', (e) => {
        console.log(`Language changed to: ${e.target.value}`);
        // Add language change logic here
    });

    // Modal Handling
    const modals = document.querySelectorAll('.modal');
    const closeModalButtons = document.querySelectorAll('.close-modal');

    function openModal(modalId) {
        document.getElementById(modalId).style.display = 'flex';
    }

    function closeModal(modalId) {
        document.getElementById(modalId).style.display = 'none';
    }

    // Open modals
    document.getElementById('login-btn').addEventListener('click', () => openModal('login-modal'));
    document.getElementById('signup-btn').addEventListener('click', () => openModal('signup-modal'));
    document.getElementById('add-farm-btn').addEventListener('click', () => openModal('farm-modal'));
    document.getElementById('add-livestock-btn').addEventListener('click', () => openModal('livestock-modal'));
    document.getElementById('add-feed-plan-btn').addEventListener('click', () => openModal('feed-plan-modal'));
    document.getElementById('add-health-record-btn').addEventListener('click', () => openModal('health-record-modal'));

    // Feature details modal
    document.querySelectorAll('.feature-details').forEach(button => {
        button.addEventListener('click', () => {
            const featureTitle = button.parentElement.querySelector('h3').textContent;
            const featureDetails = document.getElementById('feature-details');
            featureDetails.innerHTML = `<h3>${featureTitle}</h3><p>Learn more about ${featureTitle} and how it can benefit your farm.</p>`;
            openModal('feature-modal');
        });
    });

    // Close modals
    closeModalButtons.forEach(button => {
        button.addEventListener('click', () => {
            modals.forEach(modal => modal.style.display = 'none');
        });
    });

    // Close modal on outside click
    window.addEventListener('click', (e) => {
        modals.forEach(modal => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    });

    // Form Submissions (Placeholder for backend integration)
    const forms = ['login-form', 'signup-form', 'contact-form', 'farm-form', 'livestock-form', 'feed-plan-form', 'health-record-form'];
    forms.forEach(formId => {
        const form = document.getElementById(formId);
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            console.log(`Form submitted: ${formId}`, new FormData(form));
            closeModal(formId.split('-')[0] + '-modal');
            openModal('success-modal');
            // Add backend API call here
        });
    });

    // AI Recommendations (Mock Data)
    const livestockData = [
        { id: 1, name: 'Cow #1', type: 'Dairy Cow' },
        { id: 2, name: 'Cow #2', type: 'Beef Cow' }
    ];

    const livestockSelector = document.getElementById('livestock-selector');
    const feedPlanLivestock = document.getElementById('feed-plan-livestock');
    const healthRecordLivestock = document.getElementById('health-record-livestock');
    livestockData.forEach(livestock => {
        const option = document.createElement('option');
        option.value = livestock.id;
        option.textContent = livestock.name;
        livestockSelector.appendChild(option);
        feedPlanLivestock.appendChild(option.cloneNode(true));
        healthRecordLivestock.appendChild(option.cloneNode(true));
    });

    const getRecommendationBtn = document.getElementById('get-recommendation-btn');
    const recommendationResult = document.getElementById('recommendation-result');
    const recommendationTableBody = document.getElementById('recommendation-table-body');

    getRecommendationBtn.addEventListener('click', () => {
        const livestockId = livestockSelector.value;
        if (!livestockId) {
            alert('Please select a livestock.');
            return;
        }

        const livestock = livestockData.find(l => l.id == livestockId);
        const recommendation = {
            livestock: livestock.name,
            type: livestock.type,
            recommendation: 'Increase protein intake by 10%',
            confidence: '95%',
            date: new Date().toLocaleDateString()
        };

        recommendationResult.innerHTML = `
            <p><strong>Livestock:</strong> ${recommendation.livestock}</p>
            <p><strong>Type:</strong> ${recommendation.type}</p>
            <p><strong>Recommendation:</strong> ${recommendation.recommendation}</p>
            <p><strong>Confidence:</strong> ${recommendation.confidence}</p>
        `;

        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${recommendation.livestock}</td>
            <td>${recommendation.type}</td>
            <td>${recommendation.recommendation}</td>
            <td>${recommendation.confidence}</td>
            <td>${recommendation.date}</td>
        `;
        recommendationTableBody.prepend(row);
    });

    // Pricing Toggle
    const toggleButtons = document.querySelectorAll('.toggle-btn');
    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            toggleButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            const plan = button.getAttribute('data-plan');
            document.querySelectorAll('.monthly-price').forEach(price => {
                price.style.display = plan === 'monthly' ? 'block' : 'none';
            });
            document.querySelectorAll('.yearly-price').forEach(price => {
                price.style.display = plan === 'yearly' ? 'block' : 'none';
            });
        });
    });

    // Blog Filter
    const filterButtons = document.querySelectorAll('.filter-btn');
    const blogCards = document.querySelectorAll('.blog-card');

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            const filter = button.getAttribute('data-filter');
            blogCards.forEach(card => {
                const category = card.getAttribute('data-category');
                card.style.display = (filter === 'all' || filter === category) ? 'block' : 'none';
            });
        });
    });

    // Scroll to Top
    const scrollToTop = document.getElementById('scroll-to-top');
    window.addEventListener('scroll', () => {
        scrollToTop.style.display = window.scrollY > 300 ? 'block' : 'none';
    });

    scrollToTop.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Chat Functionality
    const chatButton = document.querySelector('.chat-button');
    const chatBox = document.querySelector('.chat-box');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');

    chatButton.addEventListener('click', () => {
        chatBox.style.display = chatBox.style.display === 'block' ? 'none' : 'block';
    });

    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && chatInput.value.trim()) {
            const message = document.createElement('div');
            message.textContent = `You: ${chatInput.value}`;
            chatMessages.appendChild(message);
            chatMessages.scrollTop = chatMessages.scrollHeight;

            setTimeout(() => {
                const reply = document.createElement('div');
                reply.textContent = `CattlefeedAI: Thanks for your message! How can I assist you today?`;
                chatMessages.appendChild(reply);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 1000);

            chatInput.value = '';
        }
    });
});