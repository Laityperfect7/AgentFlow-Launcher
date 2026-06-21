/**
 * AgentFlow-Launcher Web Console
 * ================================
 * Interactive frontend for running agents, workflows, and skills
 * via the FastAPI backend.
 */

(function () {
    'use strict';

    // --- State ---
    const state = {
        activeType: 'agent',
        selectedModule: '',
        modules: { agent: [], workflow: [], skill: [] },
    };

    // --- DOM refs ---
    const $ = (sel) => document.querySelector(sel);
    const typeBtns = document.querySelectorAll('.type-btn');
    const moduleSelect = $('#moduleSelect');
    const userInput = $('#userInput');
    const runBtn = $('#runBtn');
    const outputArea = $('#outputArea');
    const outputContent = $('#outputContent');
    const loading = $('#loading');
    const errorBox = $('#errorBox');
    const copyBtn = $('#copyBtn');
    const statusBadge = $('#statusBadge');
    const statusDot = statusBadge.querySelector('.status-dot');
    const statusText = $('#statusText');
    const modeIndicator = $('#modeIndicator');

    const API_BASE = '';

    // --- Init ---
    async function init() {
        await checkHealth();
        await loadModules('agent');
        bindEvents();
    }

    // --- API helpers ---
    async function apiGet(path) {
        const resp = await fetch(API_BASE + path);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        return resp.json();
    }

    async function apiPost(path, body) {
        const resp = await fetch(API_BASE + path, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || `HTTP ${resp.status}`);
        return data;
    }

    // --- Health check ---
    async function checkHealth() {
        try {
            const data = await apiGet('/health');
            statusDot.className = 'status-dot online';
            statusText.textContent = data.mock_mode ? 'Mock 模式' : '在线';
            modeIndicator.textContent = data.mock_mode ? 'Mock' : 'Live';
            modeIndicator.style.color = data.mock_mode ? 'var(--warning)' : 'var(--success)';
        } catch {
            statusDot.className = 'status-dot offline';
            statusText.textContent = '离线';
            modeIndicator.textContent = '离线';
        }
    }

    // --- Load modules ---
    async function loadModules(type) {
        const endpoint = type === 'agent' ? '/api/agents'
            : type === 'workflow' ? '/api/workflows'
            : '/api/skills';

        try {
            const data = await apiGet(endpoint);
            state.modules[type] = data;
            renderModuleOptions(type);
        } catch (err) {
            state.modules[type] = [];
            renderModuleOptions(type);
        }
    }

    function renderModuleOptions(type) {
        const modules = state.modules[type];
        moduleSelect.innerHTML = '<option value="">-- 请选择模块 --</option>';

        if (modules.length === 0) {
            moduleSelect.innerHTML += '<option value="" disabled>暂无可用模块</option>';
        } else {
            modules.forEach((m) => {
                const opt = document.createElement('option');
                opt.value = m.name;
                opt.textContent = `${m.name} — ${m.description || ''}`;
                moduleSelect.appendChild(opt);
            });
        }

        state.selectedModule = '';
        updateRunButton();
    }

    // --- Event binding ---
    function bindEvents() {
        // Type selector
        typeBtns.forEach((btn) => {
            btn.addEventListener('click', () => {
                typeBtns.forEach((b) => b.classList.remove('active'));
                btn.classList.add('active');
                state.activeType = btn.dataset.type;
                loadModules(state.activeType);
                hideOutput();
                hideError();
            });
        });

        // Module selector
        moduleSelect.addEventListener('change', () => {
            state.selectedModule = moduleSelect.value;
            updateRunButton();
            hideOutput();
            hideError();
        });

        // Run button
        runBtn.addEventListener('click', handleRun);

        // Copy button
        copyBtn.addEventListener('click', () => {
            const text = outputContent.textContent;
            navigator.clipboard.writeText(text).then(() => {
                copyBtn.style.color = 'var(--success)';
                setTimeout(() => { copyBtn.style.color = ''; }, 1500);
            });
        });

        // Enter key in textarea (Ctrl+Enter to run)
        userInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                e.preventDefault();
                if (!runBtn.disabled) handleRun();
            }
        });
    }

    function updateRunButton() {
        runBtn.disabled = !(state.selectedModule && userInput.value.trim());
    }

    // --- Run handler ---
    async function handleRun() {
        if (runBtn.disabled) return;

        const type = state.activeType;
        const module = state.selectedModule;
        const input = userInput.value.trim();

        if (!module || !input) return;

        hideOutput();
        hideError();
        showLoading();

        const endpoint = type === 'agent' ? `/api/agents/${module}/run`
            : type === 'workflow' ? `/api/workflows/${module}/run`
            : `/api/skills/${module}/run`;

        try {
            const data = await apiPost(endpoint, { input, params: {} });
            hideLoading();

            if (data.success) {
                showOutput(data);
            } else {
                showError(data.error || 'Unknown error');
            }
        } catch (err) {
            hideLoading();
            showError(err.message || 'Request failed');
        }
    }

    // --- UI helpers ---
    function showOutput(data) {
        outputArea.style.display = 'block';
        // Pretty-print if the output is a JSON string
        let display = data.output;
        if (typeof display === 'string') {
            try {
                const parsed = JSON.parse(display);
                display = JSON.stringify(parsed, null, 2);
            } catch {
                // Not JSON, keep as is
            }
        } else if (typeof display === 'object') {
            display = JSON.stringify(display, null, 2);
        }
        outputContent.textContent = display;
        outputArea.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function hideOutput() {
        outputArea.style.display = 'none';
    }

    function showLoading() {
        loading.style.display = 'flex';
        runBtn.disabled = true;
    }

    function hideLoading() {
        loading.style.display = 'none';
        updateRunButton();
    }

    function showError(msg) {
        errorBox.style.display = 'block';
        errorBox.textContent = '❌ ' + msg;
        errorBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function hideError() {
        errorBox.style.display = 'none';
    }

    // Watch input changes
    userInput.addEventListener('input', updateRunButton);

    // --- Start ---
    init();
})();
