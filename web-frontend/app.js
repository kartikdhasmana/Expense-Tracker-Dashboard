/**
 * Expense Tracker - Frontend Application
 * Professional ES6 JavaScript with proper routing and state management
 */

// ============================================
// CONFIGURATION
// ============================================
const API_BASE_URL = 'http://127.0.0.1:8000';

// ============================================
// STATE MANAGEMENT
// ============================================
const state = {
    token: localStorage.getItem('token'),
    user: null,
    expenses: [],
    analytics: null,
    signupEmail: null  // Store email during OTP flow
};

// ============================================
// DOM ELEMENTS
// ============================================
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

// ============================================
// UTILITY FUNCTIONS
// ============================================
function showLoading() {
    $('#loading-overlay').classList.add('active');
}

function hideLoading() {
    $('#loading-overlay').classList.remove('active');
}

function showToast(message, type = 'success') {
    const container = $('#toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        warning: 'fas fa-exclamation-triangle'
    };
    
    toast.innerHTML = `
        <i class="${icons[type] || icons.success}"></i>
        <span>${message}</span>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function getCategoryEmoji(category) {
    const emojis = {
        'Food': '🍔',
        'Transport': '🚗',
        'Entertainment': '🎬',
        'Shopping': '🛍️',
        'Bills': '📄',
        'Healthcare': '🏥',
        'Education': '📚',
        'Other': '📦'
    };
    return emojis[category] || '📦';
}

// ============================================
// API FUNCTIONS
// ============================================
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        ...options
    };
    
    if (state.token && !options.skipAuth) {
        config.headers['Authorization'] = `Bearer ${state.token}`;
    }
    
    try {
        const response = await fetch(url, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Request failed');
        }
        
        return { success: true, data };
    } catch (error) {
        console.error('API Error:', error);
        return { success: false, error: error.message };
    }
}

// ============================================
// AUTH FUNCTIONS
// ============================================
async function login(username, password) {
    showLoading();
    
    const result = await apiRequest('/users/login', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
        skipAuth: true
    });
    
    hideLoading();
    
    if (result.success) {
        state.token = result.data.access_token;
        localStorage.setItem('token', state.token);
        showToast('Login successful! Welcome back.');
        navigate('/dashboard');
    } else {
        showToast(result.error || 'Login failed', 'error');
    }
}

async function signup(username, password) {
    // This is now handled by the OTP flow
    showToast('Please use email verification to sign up', 'warning');
}

async function sendOTP(email) {
    showLoading();
    
    const result = await apiRequest('/users/send-otp', {
        method: 'POST',
        body: JSON.stringify({ email }),
        skipAuth: true
    });
    
    hideLoading();
    
    if (result.success) {
        state.signupEmail = email;
        showToast('Verification code sent to your email!');
        
        // Show step 2
        $('#signup-step-1').style.display = 'none';
        $('#signup-step-2').style.display = 'block';
        $('#otp-email-display').textContent = email;
        $('#signup-otp').focus();
        
        return true;
    } else {
        showToast(result.error || 'Failed to send verification code', 'error');
        return false;
    }
}

async function verifyOTPAndSignup(email, otp, username, password) {
    showLoading();
    
    const result = await apiRequest('/users/verify-otp-signup', {
        method: 'POST',
        body: JSON.stringify({ email, otp, username, password }),
        skipAuth: true
    });
    
    hideLoading();
    
    if (result.success) {
        state.token = result.data.access_token;
        localStorage.setItem('token', state.token);
        state.signupEmail = null;
        showToast('Account created successfully! Welcome!');
        navigate('/dashboard');
        return true;
    } else {
        showToast(result.error || 'Verification failed', 'error');
        return false;
    }
}

function resetSignupForm() {
    // Reset to step 1
    $('#signup-step-1').style.display = 'block';
    $('#signup-step-2').style.display = 'none';
    $('#signup-email').value = '';
    $('#signup-otp').value = '';
    $('#signup-username').value = '';
    $('#signup-password').value = '';
    $('#signup-confirm').value = '';
    state.signupEmail = null;
}

function logout() {
    state.token = null;
    state.user = null;
    state.expenses = [];
    state.analytics = null;
    localStorage.removeItem('token');
    showToast('Logged out successfully');
    navigate('/login');
}

// ============================================
// EXPENSE FUNCTIONS
// ============================================
async function fetchExpenses(filters = {}) {
    const params = new URLSearchParams();
    if (filters.category) params.set('category', filters.category);
    if (filters.start_date) params.set('start_date', filters.start_date);
    if (filters.end_date) params.set('end_date', filters.end_date);
    
    const queryString = params.toString();
    const endpoint = `/expenses/expenses${queryString ? '?' + queryString : ''}`;
    
    const result = await apiRequest(endpoint);
    
    if (result.success) {
        state.expenses = result.data;
        return result.data;
    }
    
    return [];
}

async function addExpense(expenseData) {
    showLoading();
    
    const result = await apiRequest('/expenses/expenses', {
        method: 'POST',
        body: JSON.stringify(expenseData)
    });
    
    hideLoading();
    
    if (result.success) {
        showToast('Expense added successfully!');
        return true;
    } else {
        showToast(result.error || 'Failed to add expense', 'error');
        return false;
    }
}

async function updateExpense(id, expenseData) {
    showLoading();
    
    const result = await apiRequest(`/expenses/expenses/${id}`, {
        method: 'PUT',
        body: JSON.stringify(expenseData)
    });
    
    hideLoading();
    
    if (result.success) {
        showToast('Expense updated successfully!');
        return true;
    } else {
        showToast(result.error || 'Failed to update expense', 'error');
        return false;
    }
}

async function deleteExpense(id) {
    if (!confirm('Are you sure you want to delete this expense?')) {
        return false;
    }
    
    showLoading();
    
    const result = await apiRequest(`/expenses/expenses/${id}`, {
        method: 'DELETE'
    });
    
    hideLoading();
    
    if (result.success) {
        showToast('Expense deleted successfully!');
        return true;
    } else {
        showToast(result.error || 'Failed to delete expense', 'error');
        return false;
    }
}

async function fetchAnalytics() {
    const result = await apiRequest('/analytics/analytics');
    
    if (result.success) {
        state.analytics = result.data;
        return result.data;
    }
    
    return null;
}

// ============================================
// ROUTING
// ============================================
const routes = {
    '/': 'login',
    '/login': 'login',
    '/signup': 'signup',
    '/dashboard': 'dashboard',
    '/add': 'add',
    '/expenses': 'expenses',
    '/analytics': 'analytics'
};

function navigate(path) {
    window.location.hash = path;
}

function handleRoute() {
    const hash = window.location.hash.slice(1) || '/';
    const route = routes[hash] || 'login';
    
    // Check authentication
    const publicRoutes = ['login', 'signup'];
    const isPublicRoute = publicRoutes.includes(route);
    
    if (!state.token && !isPublicRoute) {
        navigate('/login');
        return;
    }
    
    if (state.token && isPublicRoute) {
        navigate('/dashboard');
        return;
    }
    
    // Update UI
    updateNavigation(route);
    showPage(route);
    
    // Load page data
    if (route === 'dashboard') loadDashboard();
    if (route === 'add') initAddExpensePage();
    if (route === 'expenses') loadExpensesPage();
    if (route === 'analytics') loadAnalyticsPage();
    if (route === 'signup') resetSignupForm();
}

function updateNavigation(route) {
    const navbar = $('#navbar');
    const publicRoutes = ['login', 'signup'];
    
    if (publicRoutes.includes(route)) {
        navbar.style.display = 'none';
    } else {
        navbar.style.display = 'block';
        
        // Update active nav link
        $$('.nav-link').forEach(link => {
            link.classList.toggle('active', link.dataset.route === route);
        });
    }
}

function showPage(pageId) {
    $$('.page').forEach(page => {
        page.classList.toggle('active', page.id === `page-${pageId}`);
    });
}

// ============================================
// PAGE LOADERS
// ============================================
async function loadDashboard() {
    showLoading();
    
    const expenses = await fetchExpenses();
    
    hideLoading();
    
    // Calculate stats
    const total = expenses.reduce((sum, e) => sum + e.amount, 0);
    const count = expenses.length;
    const avg = count > 0 ? total / count : 0;
    
    // This month
    const now = new Date();
    const thisMonth = expenses.filter(e => {
        const d = new Date(e.date);
        return d.getMonth() === now.getMonth() && d.getFullYear() === now.getFullYear();
    });
    const monthTotal = thisMonth.reduce((sum, e) => sum + e.amount, 0);
    
    // Update stats
    $('#stat-total').textContent = formatCurrency(total);
    $('#stat-month').textContent = formatCurrency(monthTotal);
    $('#stat-avg').textContent = formatCurrency(avg);
    $('#stat-count').textContent = count;
    
    // Recent expenses
    const recent = [...expenses]
        .sort((a, b) => new Date(b.date) - new Date(a.date))
        .slice(0, 5);
    
    const recentHtml = recent.length > 0 
        ? recent.map(e => `
            <div class="expense-item">
                <div class="expense-info">
                    <div class="expense-icon">${getCategoryEmoji(e.category)}</div>
                    <div class="expense-details">
                        <h4>${e.note || e.category}</h4>
                        <p>${formatDate(e.date)} • ${e.category}</p>
                    </div>
                </div>
                <div class="expense-amount">${formatCurrency(e.amount)}</div>
            </div>
        `).join('')
        : '<div class="empty-state"><i class="fas fa-receipt"></i><p>No expenses yet. Start tracking!</p></div>';
    
    $('#recent-expenses').innerHTML = recentHtml;
}

function initAddExpensePage() {
    // Set today's date as default
    const today = new Date().toISOString().split('T')[0];
    $('#expense-date').value = today;
}

async function loadExpensesPage() {
    showLoading();
    
    // Get filter values
    const filters = {
        category: $('#filter-category').value,
        start_date: $('#filter-start').value,
        end_date: $('#filter-end').value
    };
    
    // Remove empty filters
    Object.keys(filters).forEach(key => {
        if (!filters[key]) delete filters[key];
    });
    
    const expenses = await fetchExpenses(filters);
    
    hideLoading();
    
    renderExpensesTable(expenses);
}

function renderExpensesTable(expenses) {
    const tbody = $('#expenses-tbody');
    const noExpenses = $('#no-expenses');
    const table = $('#expenses-table');
    const countBadge = $('#expense-count');
    
    countBadge.textContent = `${expenses.length} expense${expenses.length !== 1 ? 's' : ''}`;
    
    if (expenses.length === 0) {
        table.style.display = 'none';
        noExpenses.style.display = 'block';
        return;
    }
    
    table.style.display = 'table';
    noExpenses.style.display = 'none';
    
    // Sort by date (newest first)
    const sorted = [...expenses].sort((a, b) => new Date(b.date) - new Date(a.date));
    
    tbody.innerHTML = sorted.map(e => `
        <tr>
            <td>${formatDate(e.date)}</td>
            <td><span class="category-badge">${getCategoryEmoji(e.category)} ${e.category}</span></td>
            <td><strong>${formatCurrency(e.amount)}</strong></td>
            <td>${e.note || '-'}</td>
            <td class="actions">
                <button class="btn btn-sm btn-secondary" onclick="openEditModal(${e.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="handleDelete(${e.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

async function loadAnalyticsPage() {
    showLoading();
    
    const analytics = await fetchAnalytics();
    
    hideLoading();
    
    if (!analytics) {
        showToast('Failed to load analytics', 'error');
        return;
    }
    
    const { total_spend, category_summary } = analytics;
    
    // Update total
    $('#analytics-total').textContent = formatCurrency(total_spend || 0);
    
    // Render breakdown
    if (category_summary && category_summary.length > 0) {
        const breakdownHtml = category_summary.map(([cat, amount]) => {
            const percentage = total_spend > 0 ? ((amount / total_spend) * 100).toFixed(1) : 0;
            return `
                <div class="breakdown-item">
                    <div class="category">
                        <span>${getCategoryEmoji(cat)}</span>
                        <span>${cat}</span>
                    </div>
                    <div>
                        <span class="amount">${formatCurrency(amount)}</span>
                        <span class="percentage">(${percentage}%)</span>
                    </div>
                </div>
            `;
        }).join('');
        
        $('#category-breakdown').innerHTML = breakdownHtml;
        
        // Render charts
        renderCharts(category_summary);
    } else {
        $('#category-breakdown').innerHTML = '<div class="empty-state"><i class="fas fa-chart-pie"></i><p>No data to display</p></div>';
    }
}

// ============================================
// CHARTS
// ============================================
let pieChart = null;
let barChart = null;

function renderCharts(categoryData) {
    const labels = categoryData.map(([cat]) => cat);
    const data = categoryData.map(([, amount]) => amount);
    
    const colors = [
        '#6366f1', '#8b5cf6', '#ec4899', '#f43f5e',
        '#f97316', '#eab308', '#22c55e', '#14b8a6'
    ];
    
    // Destroy existing charts
    if (pieChart) pieChart.destroy();
    if (barChart) barChart.destroy();
    
    // Pie Chart
    const pieCtx = $('#category-pie-chart').getContext('2d');
    pieChart = new Chart(pieCtx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors.slice(0, data.length),
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        font: { family: 'Inter' }
                    }
                }
            }
        }
    });
    
    // Bar Chart
    const barCtx = $('#category-bar-chart').getContext('2d');
    barChart = new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Amount',
                data: data,
                backgroundColor: colors.slice(0, data.length),
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: value => '₹' + value
                    }
                }
            }
        }
    });
}

// ============================================
// MODAL FUNCTIONS
// ============================================
function openEditModal(expenseId) {
    const expense = state.expenses.find(e => e.id === expenseId);
    if (!expense) return;
    
    $('#edit-expense-id').value = expense.id;
    $('#edit-date').value = expense.date;
    $('#edit-category').value = expense.category;
    $('#edit-amount').value = expense.amount;
    $('#edit-note').value = expense.note || '';
    
    $('#edit-modal').classList.add('active');
}

function closeEditModal() {
    $('#edit-modal').classList.remove('active');
}

async function handleDelete(expenseId) {
    const success = await deleteExpense(expenseId);
    if (success) {
        loadExpensesPage();
    }
}

// ============================================
// EVENT LISTENERS
// ============================================
function initEventListeners() {
    // Hash change for routing
    window.addEventListener('hashchange', handleRoute);
    
    // Login form
    $('#login-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = $('#login-username').value.trim();
        const password = $('#login-password').value;
        
        if (!username || !password) {
            showToast('Please fill in all fields', 'warning');
            return;
        }
        
        await login(username, password);
    });
    
    // Send OTP form (Step 1)
    $('#send-otp-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = $('#signup-email').value.trim();
        
        if (!email) {
            showToast('Please enter your email', 'warning');
            return;
        }
        
        // Basic email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            showToast('Please enter a valid email address', 'error');
            return;
        }
        
        await sendOTP(email);
    });
    
    // Verify OTP and complete signup (Step 2)
    $('#verify-otp-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const otp = $('#signup-otp').value.trim();
        const username = $('#signup-username').value.trim();
        const password = $('#signup-password').value;
        const confirm = $('#signup-confirm').value;
        
        if (!otp || !username || !password || !confirm) {
            showToast('Please fill in all fields', 'warning');
            return;
        }
        
        if (otp.length !== 6 || !/^\d{6}$/.test(otp)) {
            showToast('Please enter a valid 6-digit code', 'error');
            return;
        }
        
        if (password !== confirm) {
            showToast('Passwords do not match', 'error');
            return;
        }
        
        if (password.length < 4) {
            showToast('Password must be at least 4 characters', 'error');
            return;
        }
        
        await verifyOTPAndSignup(state.signupEmail, otp, username, password);
    });
    
    // Back to step 1 button
    $('#back-to-step1').addEventListener('click', () => {
        resetSignupForm();
    });
    
    // Resend OTP button
    $('#resend-otp-btn').addEventListener('click', async () => {
        if (state.signupEmail) {
            await sendOTP(state.signupEmail);
        }
    });
    
    // Logout
    $('#logout-btn').addEventListener('click', logout);
    
    // Mobile nav toggle
    $('#nav-toggle').addEventListener('click', () => {
        $('#nav-menu').classList.toggle('active');
    });
    
    // Nav links (close mobile menu on click)
    $$('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            $('#nav-menu').classList.remove('active');
        });
    });
    
    // Add expense form
    $('#add-expense-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const expenseData = {
            date: $('#expense-date').value,
            category: $('#expense-category').value,
            amount: parseFloat($('#expense-amount').value),
            note: $('#expense-note').value || null
        };
        
        if (!expenseData.date || !expenseData.category || !expenseData.amount) {
            showToast('Please fill in all required fields', 'warning');
            return;
        }
        
        const success = await addExpense(expenseData);
        
        if (success) {
            $('#add-expense-form').reset();
            initAddExpensePage();
            // Optional: redirect to expenses list
            // navigate('/expenses');
        }
    });
    
    // Filter buttons
    $('#apply-filters').addEventListener('click', loadExpensesPage);
    
    $('#clear-filters').addEventListener('click', () => {
        $('#filter-start').value = '';
        $('#filter-end').value = '';
        $('#filter-category').value = '';
        loadExpensesPage();
    });
    
    // Edit modal
    $('#modal-close').addEventListener('click', closeEditModal);
    $('#modal-cancel').addEventListener('click', closeEditModal);
    $('.modal-overlay').addEventListener('click', closeEditModal);
    
    $('#edit-expense-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const id = parseInt($('#edit-expense-id').value);
        const expenseData = {
            date: $('#edit-date').value,
            category: $('#edit-category').value,
            amount: parseFloat($('#edit-amount').value),
            note: $('#edit-note').value || null
        };
        
        const success = await updateExpense(id, expenseData);
        
        if (success) {
            closeEditModal();
            loadExpensesPage();
        }
    });
}

// ============================================
// INITIALIZE APP
// ============================================
function init() {
    initEventListeners();
    handleRoute();
}

// Start app when DOM is ready
document.addEventListener('DOMContentLoaded', init);

// Make functions available globally for inline onclick handlers
window.openEditModal = openEditModal;
window.handleDelete = handleDelete;
