// ===========================
// State Management
// ===========================
const state = {
    currentProfile: null,
    currentView: 'dashboardView',
    currentPeriod: 'month',
    currentLanguage: 'en',
    theme: 'light',
    profiles: [],
    categories: [],
    expenses: [],
    creditCards: [],
    currentCard: null,
    charts: {}
};

// ===========================
// i18n - Internationalization
// ===========================
const translations = {
    en: {
        app_title: 'FamilySpend',
        select_profile: 'Select Profile:',
        total_spent: 'Total Spent',
        categories: 'Categories',
        week: 'Week',
        month: 'Month',
        year: 'Year',
        category_breakdown: 'Category Breakdown',
        weekly_trend: 'Weekly Trend',
        top_categories: 'Top 3 Categories',
        family_overview: 'View Family Overview',
        add_expense: 'Add Expense',
        profile: 'Profile',
        category: 'Category',
        amount: 'Amount (₹)',
        date: 'Date',
        note: 'Note (Optional)',
        save_expense: 'Save Expense',
        reports: 'Reports',
        filter_profile: 'Filter by Profile',
        start_date: 'Start Date',
        end_date: 'End Date',
        apply_filters: 'Apply Filters',
        export_csv: '📥 Export to CSV',
        settings: 'Settings',
        appearance: 'Appearance',
        dark_mode: 'Dark Mode',
        language: 'Language',
        current_language: 'Current Language',
        about: 'About',
        about_desc: 'A simple, beautiful expense tracker for families',
        dashboard: 'Dashboard',
        add: 'Add',
        total_family_spending: 'Total Family Spending',
        spending_by_member: 'Spending by Member',
        top_family_categories: 'Top Family Categories',
        expense_added: 'Expense added successfully!',
        expense_deleted: 'Expense deleted',
        error_occurred: 'An error occurred',
        no_expenses: 'No expenses found',
        loading: 'Loading...',
        credit_cards: 'Credit Cards',
        cards: 'Cards',
        add_card: 'Add New Card',
        add_new_card: 'Add New Credit Card',
        card_profile: 'Profile',
        card_name: 'Card Name',
        card_last_four: 'Last 4 Digits',
        credit_limit: 'Credit Limit',
        billing_day: 'Billing Day',
        card_color: 'Card Color',
        save_card: 'Save Card',
        cancel: 'Cancel',
        credit_card: 'Credit Card',
        spent: 'Spent',
        available: 'Available',
        utilization: 'Utilization',
        recent_transactions: 'Recent Transactions',
        delete_card: 'Delete Card',
        card_added: 'Card added successfully!',
        card_deleted: 'Card deleted successfully!'
    },
    te: {
        app_title: 'ఫ్యామిలీస్పెండ్',
        select_profile: 'ప్రొఫైల్ ఎంచుకోండి:',
        total_spent: 'మొత్తం ఖర్చు',
        categories: 'వర్గాలు',
        week: 'వారం',
        month: 'నెల',
        year: 'సంవత్సరం',
        category_breakdown: 'వర్గం వారీగా',
        weekly_trend: 'వారపు ధోరణి',
        top_categories: 'టాప్ 3 వర్గాలు',
        family_overview: 'కుటుంబ సమీక్ష చూడండి',
        add_expense: 'ఖర్చు జోడించండి',
        profile: 'ప్రొఫైల్',
        category: 'వర్గం',
        amount: 'మొత్తం (₹)',
        date: 'తేదీ',
        note: 'గమనిక (ఐచ్ఛికం)',
        save_expense: 'ఖర్చు సేవ్ చేయండి',
        reports: 'నివేదికలు',
        filter_profile: 'ప్రొఫైల్ ద్వారా ఫిల్టర్',
        start_date: 'ప్రారంభ తేదీ',
        end_date: 'ముగింపు తేదీ',
        apply_filters: 'ఫిల్టర్లు వర్తింపజేయండి',
        export_csv: '📥 CSV కి ఎగుమతి చేయండి',
        settings: 'సెట్టింగ్‌లు',
        appearance: 'రూపం',
        dark_mode: 'డార్క్ మోడ్',
        language: 'భాష',
        current_language: 'ప్రస్తుత భాష',
        about: 'గురించి',
        about_desc: 'కుటుంబాల కోసం సరళమైన, అందమైన ఖర్చు ట్రాకర్',
        dashboard: 'డాష్‌బోర్డ్',
        add: 'జోడించు',
        reports: 'నివేదికలు',
        settings: 'సెట్టింగ్‌లు',
        total_family_spending: 'మొత్తం కుటుంబ ఖర్చు',
        spending_by_member: 'సభ్యుల వారీగా ఖర్చు',
        top_family_categories: 'టాప్ కుటుంబ వర్గాలు',
        expense_added: 'ఖర్చు విజయవంతంగా జోడించబడింది!',
        expense_deleted: 'ఖర్చు తొలగించబడింది',
        error_occurred: 'లోపం సంభవించింది',
        no_expenses: 'ఖర్చులు కనుగొనబడలేదు',
        loading: 'లోడ్ అవుతోంది...',
        credit_cards: 'క్రెడిట్ కార్డులు',
        cards: 'కార్డులు',
        add_card: 'కొత్త కార్డ్ జోడించండి',
        add_new_card: 'కొత్త క్రెడిట్ కార్డ్ జోడించండి',
        card_profile: 'ప్రొఫైల్',
        card_name: 'కార్డ్ పేరు',
        card_last_four: 'చివరి 4 అంకెలు',
        credit_limit: 'క్రెడిట్ పరిమితి',
        billing_day: 'బిల్లింగ్ రోజు',
        card_color: 'కార్డ్ రంగు',
        save_card: 'కార్డ్ సేవ్ చేయండి',
        cancel: 'రద్దు చేయండి',
        credit_card: 'క్రెడిట్ కార్డ్',
        spent: 'ఖర్చు',
        available: 'అందుబాటులో',
        utilization: 'వినియోగం',
        recent_transactions: 'ఇటీవలి లావాదేవీలు',
        delete_card: 'కార్డ్ తొలగించండి',
        card_added: 'కార్డ్ విజయవంతంగా జోడించబడింది!',
        card_deleted: 'కార్డ్ విజయవంతంగా తొలగించబడింది!'
    }
};

function translate(key) {
    return translations[state.currentLanguage][key] || key;
}

function updatePageLanguage() {
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        element.textContent = translate(key);
    });

    // Update current language display
    const langDisplay = document.getElementById('currentLang');
    if (langDisplay) {
        langDisplay.textContent = state.currentLanguage === 'en' ? 'English' : 'తెలుగు';
    }
}

function toggleLanguage() {
    state.currentLanguage = state.currentLanguage === 'en' ? 'te' : 'en';
    localStorage.setItem('language', state.currentLanguage);
    updatePageLanguage();

    // Refresh dashboard to update chart labels
    if (state.currentProfile) {
        loadDashboard(state.currentProfile, state.currentPeriod);
    }
}

// ===========================
// API Functions
// ===========================
async function fetchAPI(endpoint, options = {}) {
    try {
        const response = await fetch(`/api${endpoint}`, options);
        if (!response.ok) throw new Error('API request failed');
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showToast(translate('error_occurred'));
        throw error;
    }
}

async function loadProfiles() {
    state.profiles = await fetchAPI('/profiles');
    populateProfileSelects();
}

async function loadCategories() {
    state.categories = await fetchAPI('/categories');
    populateCategorySelects();
}

async function loadDashboard(profileId, period = 'month') {
    const data = await fetchAPI(`/dashboard/${profileId}?period=${period}`);
    updateDashboardUI(data);
}

async function loadExpenses(filters = {}) {
    const params = new URLSearchParams(filters);
    state.expenses = await fetchAPI(`/expenses?${params}`);
    updateExpenseList();
}

async function addExpense(expenseData) {
    await fetchAPI('/expenses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(expenseData)
    });
}

async function deleteExpense(expenseId) {
    await fetchAPI(`/expenses/${expenseId}`, { method: 'DELETE' });
}

async function loadFamilyOverview(period = 'month') {
    const data = await fetchAPI(`/family-overview?period=${period}`);
    updateFamilyOverviewUI(data);
}

async function exportCSV(filters = {}) {
    const params = new URLSearchParams(filters);
    window.location.href = `/api/export/csv?${params}`;
}

// Credit Card API Functions
async function loadCreditCards() {
    state.creditCards = await fetchAPI('/credit-cards');
    updateCreditCardsUI();
    populateCardSelects();
}

async function addCreditCard(cardData) {
    await fetchAPI('/credit-cards', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(cardData)
    });
}

async function updateCreditCard(cardId, cardData) {
    await fetchAPI(`/credit-cards/${cardId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(cardData)
    });
}

async function deleteCreditCard(cardId) {
    await fetchAPI(`/credit-cards/${cardId}`, { method: 'DELETE' });
}

async function loadCardDashboard(cardId) {
    const data = await fetchAPI(`/credit-cards/${cardId}/dashboard`);
    updateCardDashboardUI(data);
}

// ===========================
// UI Update Functions
// ===========================
function populateProfileSelects() {
    const selects = [
        document.getElementById('profileSelect'),
        document.getElementById('expenseProfile'),
        document.getElementById('reportProfile')
    ];

    selects.forEach(select => {
        if (!select) return;
        select.innerHTML = '';

        if (select.id === 'reportProfile') {
            const allOption = document.createElement('option');
            allOption.value = '';
            allOption.textContent = 'All Profiles';
            select.appendChild(allOption);
        }

        state.profiles.forEach(profile => {
            const option = document.createElement('option');
            option.value = profile.id;
            option.textContent = profile.display_name;
            select.appendChild(option);
        });
    });

    // Set default profile
    if (state.profiles.length > 0 && !state.currentProfile) {
        state.currentProfile = state.profiles[0].id;
        document.getElementById('profileSelect').value = state.currentProfile;
        loadDashboard(state.currentProfile, state.currentPeriod);
    }
}

function populateCategorySelects() {
    const select = document.getElementById('expenseCategory');
    if (!select) return;

    select.innerHTML = '<option value="">Select Category</option>';

    state.categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category.id;
        const categoryName = state.currentLanguage === 'te' ? category.name_te : category.name;
        option.textContent = `${category.icon} ${categoryName}`;
        select.appendChild(option);
    });
}

function updateDashboardUI(data) {
    // Update stats
    document.getElementById('totalSpent').textContent = `₹${data.total_spent.toLocaleString('en-IN')}`;
    document.getElementById('categoryCount').textContent = data.category_breakdown.length;

    // Update category chart
    updateCategoryChart(data.category_breakdown);

    // Update trend chart
    updateTrendChart(data.weekly_trend);

    // Update top categories
    updateTopCategories(data.top_categories);
}

function updateCategoryChart(categoryData) {
    const ctx = document.getElementById('categoryChart');
    if (!ctx) return;

    // Destroy existing chart
    if (state.charts.categoryChart) {
        state.charts.categoryChart.destroy();
    }

    const labels = categoryData.map(item => {
        const name = state.currentLanguage === 'te' ? item.category_te : item.category;
        return `${item.icon} ${name}`;
    });
    const amounts = categoryData.map(item => item.amount);

    state.charts.categoryChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: amounts,
                backgroundColor: [
                    '#4A90E2', '#5DA3E8', '#7BB5ED', '#99C7F2',
                    '#5CB85C', '#6BC76B', '#7DD67D', '#90E590',
                    '#F0AD4E', '#F4BD6C', '#F8CD8A', '#FCDDA8'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: getComputedStyle(document.body).getPropertyValue('--text-primary'),
                        padding: 10,
                        font: { size: 11 }
                    }
                }
            }
        }
    });
}

function updateTrendChart(trendData) {
    const ctx = document.getElementById('trendChart');
    if (!ctx) return;

    if (state.charts.trendChart) {
        state.charts.trendChart.destroy();
    }

    const labels = trendData.map(item => {
        const date = new Date(item.date);
        return date.toLocaleDateString('en-IN', { weekday: 'short' });
    });
    const amounts = trendData.map(item => item.amount);

    state.charts.trendChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: translate('amount'),
                data: amounts,
                backgroundColor: '#4A90E2',
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: getComputedStyle(document.body).getPropertyValue('--text-secondary'),
                        callback: value => `₹${value}`
                    },
                    grid: {
                        color: getComputedStyle(document.body).getPropertyValue('--border-color')
                    }
                },
                x: {
                    ticks: {
                        color: getComputedStyle(document.body).getPropertyValue('--text-secondary')
                    },
                    grid: { display: false }
                }
            }
        }
    });
}

function updateTopCategories(topCategories) {
    const container = document.getElementById('topCategoriesList');
    if (!container) return;

    container.innerHTML = '';

    if (topCategories.length === 0) {
        container.innerHTML = `<p style="text-align: center; color: var(--text-secondary);">${translate('no_expenses')}</p>`;
        return;
    }

    topCategories.forEach(item => {
        const categoryName = state.currentLanguage === 'te' ? item.category_te : item.category;
        const div = document.createElement('div');
        div.className = 'category-item';
        div.innerHTML = `
            <div class="category-info">
                <span class="category-icon">${item.icon}</span>
                <span class="category-name">${categoryName}</span>
            </div>
            <span class="category-amount">₹${item.amount.toLocaleString('en-IN')}</span>
        `;
        container.appendChild(div);
    });
}

function updateExpenseList() {
    const container = document.getElementById('expenseList');
    if (!container) return;

    container.innerHTML = '';

    if (state.expenses.length === 0) {
        container.innerHTML = `<p style="text-align: center; color: var(--text-secondary); padding: 20px;">${translate('no_expenses')}</p>`;
        return;
    }

    state.expenses.forEach(expense => {
        const categoryName = state.currentLanguage === 'te' ? expense.category_name_te : expense.category_name;
        const div = document.createElement('div');
        div.className = 'expense-item';
        div.dataset.id = expense.id;
        div.innerHTML = `
            <div class="expense-details">
                <div class="expense-category">
                    <span>${expense.category_icon}</span>
                    <span>${categoryName}</span>
                </div>
                <div class="expense-meta">
                    ${expense.profile_name} • ${new Date(expense.date).toLocaleDateString('en-IN')}
                    ${expense.note ? `• ${expense.note}` : ''}
                </div>
            </div>
            <div class="expense-amount">₹${expense.amount.toLocaleString('en-IN')}</div>
            <button class="delete-btn" onclick="handleDeleteExpense(${expense.id})">🗑️</button>
        `;

        // Add swipe functionality
        let startX = 0;
        div.addEventListener('touchstart', e => {
            startX = e.touches[0].clientX;
        });

        div.addEventListener('touchmove', e => {
            const currentX = e.touches[0].clientX;
            const diff = startX - currentX;
            if (diff > 50) {
                div.classList.add('swipe-left');
            } else if (diff < -50) {
                div.classList.remove('swipe-left');
            }
        });

        container.appendChild(div);
    });
}

function updateFamilyOverviewUI(data) {
    document.getElementById('familyTotal').textContent = `₹${data.total_family.toLocaleString('en-IN')}`;

    // Family spending chart
    const ctx1 = document.getElementById('familyChart');
    if (state.charts.familyChart) {
        state.charts.familyChart.destroy();
    }

    state.charts.familyChart = new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: data.profile_spending.map(p => p.profile),
            datasets: [{
                label: translate('amount'),
                data: data.profile_spending.map(p => p.amount),
                backgroundColor: '#4A90E2',
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            indexAxis: 'y',
            plugins: { legend: { display: false } },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        color: getComputedStyle(document.body).getPropertyValue('--text-secondary'),
                        callback: value => `₹${value}`
                    }
                },
                y: {
                    ticks: {
                        color: getComputedStyle(document.body).getPropertyValue('--text-secondary')
                    }
                }
            }
        }
    });

    // Family category chart
    const ctx2 = document.getElementById('familyCategoryChart');
    if (state.charts.familyCategoryChart) {
        state.charts.familyCategoryChart.destroy();
    }

    const labels = data.top_categories.map(item => {
        const name = state.currentLanguage === 'te' ? item.category_te : item.category;
        return name;
    });

    state.charts.familyCategoryChart = new Chart(ctx2, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data.top_categories.map(c => c.amount),
                backgroundColor: [
                    '#4A90E2', '#5DA3E8', '#7BB5ED', '#99C7F2',
                    '#5CB85C', '#6BC76B', '#7DD67D', '#90E590'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: getComputedStyle(document.body).getPropertyValue('--text-primary')
                    }
                }
            }
        }
    });
}

// Credit Card UI Update Functions
function populateCardSelects() {
    const cardSelect = document.getElementById('expenseCard');
    const cardProfileSelect = document.getElementById('cardProfile');

    if (cardSelect) {
        cardSelect.innerHTML = '<option value="">Cash / No Card</option>';
        state.creditCards.forEach(card => {
            const option = document.createElement('option');
            option.value = card.id;
            option.textContent = `${card.card_name} ${card.card_last_four ? '••' + card.card_last_four : ''}`;
            cardSelect.appendChild(option);
        });
    }

    if (cardProfileSelect) {
        cardProfileSelect.innerHTML = '<option value="">Select Profile</option>';
        state.profiles.forEach(profile => {
            const option = document.createElement('option');
            option.value = profile.id;
            option.textContent = profile.display_name;
            cardProfileSelect.appendChild(option);
        });
    }
}

function updateCreditCardsUI() {
    const container = document.getElementById('creditCardsGrid');
    if (!container) return;

    container.innerHTML = '';

    if (state.creditCards.length === 0) {
        container.innerHTML = `
            <div class="add-card-btn" id="addCardBtnPlaceholder">
                <div class="icon">💳</div>
                <div>${translate('add_card')}</div>
            </div>
        `;
        document.getElementById('addCardBtnPlaceholder')?.addEventListener('click', () => {
            document.getElementById('addCardFormContainer').classList.remove('hidden');
        });
        return;
    }

    state.creditCards.forEach(card => {
        const div = document.createElement('div');
        const colorClass = card.card_color || 'gradient-primary';
        div.className = `credit-card-item ${colorClass}`;
        div.dataset.cardId = card.id;

        div.innerHTML = `
            <div class="card-header">
                <div>
                    <div class="card-name">${card.card_name}</div>
                    ${card.card_last_four ? `<div class="card-number">•••• ${card.card_last_four}</div>` : ''}
                </div>
                <div style="font-size: 1.5rem;">💳</div>
            </div>
            <div class="card-balance-section">
                <div class="card-balance-label">${translate('credit_limit')}</div>
                <div class="card-balance-amount">₹${card.credit_limit.toLocaleString('en-IN')}</div>
                <div class="card-limit">Billing: ${card.billing_day}${getOrdinalSuffix(card.billing_day)} of month</div>
            </div>
        `;

        div.addEventListener('click', () => {
            state.currentCard = card.id;
            loadCardDashboard(card.id);
            document.getElementById('cardDetailsModal').classList.add('active');
            document.getElementById('cardDetailsTitle').textContent = card.card_name;
        });

        container.appendChild(div);
    });
}

function getOrdinalSuffix(day) {
    if (day > 3 && day < 21) return 'th';
    switch (day % 10) {
        case 1: return 'st';
        case 2: return 'nd';
        case 3: return 'rd';
        default: return 'th';
    }
}

function updateCardDashboardUI(data) {
    // Update stats
    document.getElementById('cardSpent').textContent = `₹${data.total_spent.toLocaleString('en-IN')}`;
    document.getElementById('cardAvailable').textContent = `₹${data.available_balance.toLocaleString('en-IN')}`;
    document.getElementById('cardUtilization').textContent = `${data.utilization}%`;

    // Update utilization bar
    const utilizationFill = document.getElementById('cardUtilizationFill');
    utilizationFill.style.width = `${data.utilization}%`;
    utilizationFill.className = 'card-utilization-fill';
    if (data.utilization > 70) utilizationFill.classList.add('high');
    if (data.utilization > 90) utilizationFill.classList.add('critical');

    // Update cycle info
    const cycleStart = new Date(data.cycle_start).toLocaleDateString('en-IN', { month: 'short', day: 'numeric' });
    const cycleEnd = new Date(data.cycle_end).toLocaleDateString('en-IN', { month: 'short', day: 'numeric' });
    document.getElementById('cardCycle').textContent = `${cycleStart} - ${cycleEnd}`;

    // Update category chart
    const ctx = document.getElementById('cardCategoryChart');
    if (state.charts.cardCategoryChart) {
        state.charts.cardCategoryChart.destroy();
    }

    if (data.category_breakdown.length > 0) {
        const labels = data.category_breakdown.map(item => {
            const name = state.currentLanguage === 'te' ? item.category_te : item.category;
            return `${item.icon} ${name}`;
        });

        state.charts.cardCategoryChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data.category_breakdown.map(c => c.amount),
                    backgroundColor: ['#667eea', '#f093fb', '#4facfe', '#fa709a', '#30cfd0']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: getComputedStyle(document.body).getPropertyValue('--text-primary')
                        }
                    }
                }
            }
        });
    }

    // Update transactions list
    const transactionsList = document.getElementById('cardTransactionsList');
    transactionsList.innerHTML = '';

    if (data.recent_transactions.length === 0) {
        transactionsList.innerHTML = `<p style="text-align: center; color: var(--text-secondary); padding: 20px;">${translate('no_expenses')}</p>`;
    } else {
        data.recent_transactions.forEach(txn => {
            const div = document.createElement('div');
            div.className = 'expense-item';
            div.innerHTML = `
                <div class="expense-details">
                    <div class="expense-category">
                        <span>${txn.icon}</span>
                        <span>${txn.category}</span>
                    </div>
                    <div class="expense-meta">
                        ${new Date(txn.date).toLocaleDateString('en-IN')}
                        ${txn.note ? `• ${txn.note}` : ''}
                    </div>
                </div>
                <div class="expense-amount">₹${txn.amount.toLocaleString('en-IN')}</div>
            `;
            transactionsList.appendChild(div);
        });
    }
}

// ===========================
// Event Handlers
// ===========================
async function handleDeleteExpense(expenseId) {
    if (confirm('Delete this expense?')) {
        await deleteExpense(expenseId);
        showToast(translate('expense_deleted'));

        // Refresh current view
        const reportProfile = document.getElementById('reportProfile').value;
        const startDate = document.getElementById('reportStartDate').value;
        const endDate = document.getElementById('reportEndDate').value;

        await loadExpenses({
            profile_id: reportProfile,
            start_date: startDate,
            end_date: endDate
        });

        // Refresh dashboard if needed
        if (state.currentProfile) {
            await loadDashboard(state.currentProfile, state.currentPeriod);
        }
    }
}

// ===========================
// Utility Functions
// ===========================
function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3000);
}

function switchView(viewId) {
    document.querySelectorAll('.view').forEach(view => view.classList.remove('active'));
    document.getElementById(viewId).classList.add('active');

    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
    document.querySelector(`[data-view="${viewId}"]`).classList.add('active');

    state.currentView = viewId;
}

function toggleTheme() {
    state.theme = state.theme === 'light' ? 'dark' : 'light';
    document.body.classList.toggle('dark-theme');
    localStorage.setItem('theme', state.theme);

    const icon = document.querySelector('.theme-icon');
    icon.textContent = state.theme === 'dark' ? '☀️' : '🌙';

    // Refresh charts to update colors
    if (state.currentProfile) {
        loadDashboard(state.currentProfile, state.currentPeriod);
    }
}

// ===========================
// Initialization
// ===========================
async function init() {
    // Load saved preferences
    const savedTheme = localStorage.getItem('theme') || 'light';
    const savedLanguage = localStorage.getItem('language') || 'en';

    state.theme = savedTheme;
    state.currentLanguage = savedLanguage;

    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        document.querySelector('.theme-icon').textContent = '☀️';
        document.getElementById('darkModeSwitch').checked = true;
    }

    updatePageLanguage();

    // Load data
    await loadProfiles();
    await loadCategories();

    // Set today's date as default
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('expenseDate').value = today;

    // Hide loading
    document.getElementById('loading').classList.add('hidden');

    // Event Listeners
    document.getElementById('profileSelect').addEventListener('change', e => {
        state.currentProfile = parseInt(e.target.value);
        loadDashboard(state.currentProfile, state.currentPeriod);
    });

    document.querySelectorAll('.period-btn').forEach(btn => {
        btn.addEventListener('click', e => {
            document.querySelectorAll('.period-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            state.currentPeriod = e.target.dataset.period;
            loadDashboard(state.currentProfile, state.currentPeriod);
        });
    });

    document.getElementById('expenseForm').addEventListener('submit', async e => {
        e.preventDefault();

        const cardId = document.getElementById('expenseCard').value;
        const expenseData = {
            profile_id: parseInt(document.getElementById('expenseProfile').value),
            category_id: parseInt(document.getElementById('expenseCategory').value),
            amount: parseFloat(document.getElementById('expenseAmount').value),
            date: document.getElementById('expenseDate').value,
            note: document.getElementById('expenseNote').value
        };

        if (cardId) {
            expenseData.card_id = parseInt(cardId);
        }

        await addExpense(expenseData);
        showToast(translate('expense_added'));

        e.target.reset();
        document.getElementById('expenseDate').value = today;

        // Refresh dashboard
        if (state.currentProfile) {
            await loadDashboard(state.currentProfile, state.currentPeriod);
        }

        // Switch to dashboard
        switchView('dashboardView');
    });

    document.getElementById('applyFilters').addEventListener('click', async () => {
        const filters = {
            profile_id: document.getElementById('reportProfile').value,
            start_date: document.getElementById('reportStartDate').value,
            end_date: document.getElementById('reportEndDate').value
        };
        await loadExpenses(filters);
    });

    document.getElementById('exportCSV').addEventListener('click', () => {
        const filters = {
            profile_id: document.getElementById('reportProfile').value,
            start_date: document.getElementById('reportStartDate').value,
            end_date: document.getElementById('reportEndDate').value
        };
        exportCSV(filters);
    });

    document.getElementById('familyOverviewBtn').addEventListener('click', async () => {
        document.getElementById('familyModal').classList.add('active');
        await loadFamilyOverview(state.currentPeriod);
    });

    document.getElementById('closeModal').addEventListener('click', () => {
        document.getElementById('familyModal').classList.remove('active');
    });

    document.getElementById('themeToggle').addEventListener('click', toggleTheme);
    document.getElementById('langToggle').addEventListener('click', toggleLanguage);
    document.getElementById('languageSwitch').addEventListener('click', toggleLanguage);

    document.getElementById('darkModeSwitch').addEventListener('change', toggleTheme);

    // Bottom navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', e => {
            const viewId = e.currentTarget.dataset.view;
            switchView(viewId);

            // Load data for reports view
            if (viewId === 'reportsView') {
                loadExpenses();
            }
        });
    });

    // Close modal on outside click
    document.getElementById('familyModal').addEventListener('click', e => {
        if (e.target.id === 'familyModal') {
            e.target.classList.remove('active');
        }
    });

    // Credit Card Event Handlers
    document.getElementById('showAddCardForm')?.addEventListener('click', () => {
        document.getElementById('addCardFormContainer').classList.remove('hidden');
        document.getElementById('addCardFormContainer').scrollIntoView({ behavior: 'smooth' });
    });

    document.getElementById('cancelAddCard')?.addEventListener('click', () => {
        document.getElementById('addCardFormContainer').classList.add('hidden');
        document.getElementById('addCardForm').reset();
    });

    document.getElementById('addCardForm')?.addEventListener('submit', async e => {
        e.preventDefault();

        const cardData = {
            profile_id: parseInt(document.getElementById('cardProfile').value),
            card_name: document.getElementById('cardName').value,
            card_last_four: document.getElementById('cardLastFour').value,
            credit_limit: parseFloat(document.getElementById('cardLimit').value),
            billing_day: parseInt(document.getElementById('billingDay').value),
            card_color: document.getElementById('cardColor').value
        };

        await addCreditCard(cardData);
        showToast(translate('card_added'));

        e.target.reset();
        document.getElementById('addCardFormContainer').classList.add('hidden');

        await loadCreditCards();
    });

    document.getElementById('closeCardModal')?.addEventListener('click', () => {
        document.getElementById('cardDetailsModal').classList.remove('active');
    });

    document.getElementById('cardDetailsModal')?.addEventListener('click', e => {
        if (e.target.id === 'cardDetailsModal') {
            e.target.classList.remove('active');
        }
    });

    document.getElementById('deleteCardBtn')?.addEventListener('click', async () => {
        if (confirm('Are you sure you want to delete this card? Expenses linked to this card will not be deleted.')) {
            await deleteCreditCard(state.currentCard);
            showToast(translate('card_deleted'));
            document.getElementById('cardDetailsModal').classList.remove('active');
            await loadCreditCards();
        }
    });

    // Load credit cards on init
    await loadCreditCards();
}

// Start the app
document.addEventListener('DOMContentLoaded', init);
