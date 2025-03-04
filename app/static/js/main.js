/**
 * Main JavaScript for AI Regex Generator
 */

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    initCopyButtons();
    initModals();
    initDarkModeToggle();
    setupTooltips();
});

/**
 * Initialize copy buttons
 */
function initCopyButtons() {
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-copy-target');
            const target = document.getElementById(targetId);
            
            if (target) {
                // Select the content
                if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') {
                    target.select();
                } else {
                    // For other elements, create a range
                    const range = document.createRange();
                    range.selectNode(target);
                    window.getSelection().removeAllRanges();
                    window.getSelection().addRange(range);
                }
                
                // Copy to clipboard
                document.execCommand('copy');
                
                // Deselect
                window.getSelection().removeAllRanges();
                
                // Show feedback
                const originalHTML = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check"></i>';
                
                setTimeout(() => {
                    this.innerHTML = originalHTML;
                }, 2000);
            }
        });
    });
}

/**
 * Initialize modal behaviors
 */
function initModals() {
    // Clean up modals when hidden
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('hidden.bs.modal', function() {
            if (this.getAttribute('data-dynamic') === 'true') {
                this.remove();
            }
        });
    });
}

/**
 * Initialize dark mode toggle
 */
function initDarkModeToggle() {
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    
    if (darkModeToggle) {
        // Check for saved preference
        const darkMode = localStorage.getItem('darkMode') === 'true';
        
        // Apply dark mode if saved
        if (darkMode) {
            document.body.classList.add('dark-mode');
            darkModeToggle.checked = true;
        }
        
        // Handle toggle change
        darkModeToggle.addEventListener('change', function() {
            if (this.checked) {
                document.body.classList.add('dark-mode');
                localStorage.setItem('darkMode', 'true');
            } else {
                document.body.classList.remove('dark-mode');
                localStorage.setItem('darkMode', 'false');
            }
        });
    }
}

/**
 * Setup Bootstrap tooltips
 */
function setupTooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
}

/**
 * Create a matches table from regex test results
 * 
 * @param {Array} matches - Array of match objects
 * @returns {HTMLTableElement} - Table element with match data
 */
function createMatchesTable(matches) {
    const matchesTable = document.createElement('table');
    matchesTable.className = 'table table-striped';
    
    // Create table header
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    ['Match', 'Position', 'Groups'].forEach(text => {
        const th = document.createElement('th');
        th.textContent = text;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    matchesTable.appendChild(thead);
    
    // Create table body
    const tbody = document.createElement('tbody');
    matches.forEach((match, index) => {
        const row = document.createElement('tr');
        
        // Match cell
        const matchCell = document.createElement('td');
        const matchCode = document.createElement('code');
        matchCode.textContent = match.full_match;
        matchCell.appendChild(matchCode);
        row.appendChild(matchCell);
        
        // Position cell
        const posCell = document.createElement('td');
        posCell.textContent = `${match.start}-${match.end}`;
        row.appendChild(posCell);
        
        // Groups cell
        const groupsCell = document.createElement('td');
        if (match.groups && match.groups.length > 0) {
            const groupsList = document.createElement('ul');
            groupsList.className = 'mb-0';
            match.groups.forEach(group => {
                const groupItem = document.createElement('li');
                groupItem.innerHTML = `Group ${group.group_num}: <code>${group.content}</code>`;
                groupsList.appendChild(groupItem);
            });
            groupsCell.appendChild(groupsList);
        } else {
            groupsCell.textContent = 'No groups';
        }
        row.appendChild(groupsCell);
        
        tbody.appendChild(row);
    });
    matchesTable.appendChild(tbody);
    
    return matchesTable;
}

/**
 * Show an error toast
 * 
 * @param {string} message - Error message to display
 */
function showErrorToast(message) {
    const toastContainer = document.getElementById('toast-container');
    
    if (!toastContainer) {
        // Create toast container if it doesn't exist
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    // Set toast content
    toast.innerHTML = `
        <div class="toast-header bg-danger text-white">
            <strong class="me-auto">Error</strong>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    // Add toast to container
    document.getElementById('toast-container').appendChild(toast);
    
    // Initialize and show toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast when hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}