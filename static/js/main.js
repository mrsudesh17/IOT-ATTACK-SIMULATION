/* ============================================================
   IoT Phishing Attack Simulation — Client-Side JavaScript
   Handles countdown timers, form validation, and password toggle
   ============================================================ */

/**
 * Start a countdown timer and display it in the target element.
 * @param {string} elementId - ID of the element to display the countdown
 * @param {number} totalSeconds - Total seconds to count down from
 */
function startCountdown(elementId, totalSeconds) {
    const el = document.getElementById(elementId);
    if (!el) return;

    function updateDisplay() {
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        el.textContent =
            String(hours).padStart(2, '0') + ':' +
            String(minutes).padStart(2, '0') + ':' +
            String(seconds).padStart(2, '0');

        if (totalSeconds > 0) {
            totalSeconds--;
            setTimeout(updateDisplay, 1000);
        } else {
            el.textContent = 'EXPIRED';
            el.style.color = '#dc2626';
        }
    }

    updateDisplay();
}

/**
 * Toggle password field visibility.
 */
function togglePasswordVisibility() {
    const passwordField = document.getElementById('password');
    const toggleBtn = document.getElementById('toggle-password');

    if (!passwordField || !toggleBtn) return;

    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleBtn.textContent = '🙈';
    } else {
        passwordField.type = 'password';
        toggleBtn.textContent = '👁️';
    }
}

/* ─── Auto-dismiss flash messages after 4 seconds ──────── */
document.addEventListener('DOMContentLoaded', function () {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function (msg) {
        setTimeout(function () {
            msg.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px)';
            setTimeout(function () { msg.remove(); }, 500);
        }, 4000);
    });
});
