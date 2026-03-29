/**
 * IoT Phishing Simulation — Client-side Enhancements
 * ===================================================
 * Handles scenario card selection, form validation,
 * password masking toggle, and phishing indicator highlights.
 */

document.addEventListener("DOMContentLoaded", () => {
    // -----------------------------------------------------------------
    // 1. Scenario card selection on the /panel page
    // -----------------------------------------------------------------
    const scenarioCards = document.querySelectorAll(".scenario-card");
    const hiddenInput = document.getElementById("scenario-type");
    const startBtn = document.getElementById("start-btn");

    if (scenarioCards.length > 0 && hiddenInput) {
        // Pre-select the first card
        scenarioCards[0].classList.add("selected");
        hiddenInput.value = scenarioCards[0].dataset.type;

        scenarioCards.forEach((card) => {
            card.addEventListener("click", () => {
                // Remove selection from all
                scenarioCards.forEach((c) => c.classList.remove("selected"));
                // Select clicked card
                card.classList.add("selected");
                hiddenInput.value = card.dataset.type;
            });
        });
    }

    // Start Simulation button
    if (startBtn) {
        startBtn.addEventListener("click", () => {
            const type = hiddenInput ? hiddenInput.value : "storage";
            window.location.href = `/?type=${type}`;
        });
    }

    // -----------------------------------------------------------------
    // 2. Login form — basic client-side validation + confirm dialog
    // -----------------------------------------------------------------
    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", (e) => {
            const username = document.getElementById("username");
            const password = document.getElementById("password");

            if (!username.value.trim() || !password.value.trim()) {
                e.preventDefault();
                alert("Please enter both username and password.");
                return;
            }

            // The form will submit normally — credentials are captured server-side
        });
    }

    // -----------------------------------------------------------------
    // 3. Password visibility toggle
    // -----------------------------------------------------------------
    const toggleBtn = document.getElementById("toggle-password");
    if (toggleBtn) {
        toggleBtn.addEventListener("click", () => {
            const pwdField = document.getElementById("password");
            if (pwdField.type === "password") {
                pwdField.type = "text";
                toggleBtn.textContent = "🙈";
            } else {
                pwdField.type = "password";
                toggleBtn.textContent = "👁️";
            }
        });
    }

    // -----------------------------------------------------------------
    // 4. Admin table — toggle password visibility per row
    // -----------------------------------------------------------------
    document.querySelectorAll(".reveal-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
            const cell = btn.closest("td").querySelector(".masked");
            if (cell) {
                const real = cell.dataset.real;
                if (cell.textContent === "••••••••") {
                    cell.textContent = real;
                    btn.textContent = "Hide";
                } else {
                    cell.textContent = "••••••••";
                    btn.textContent = "Show";
                }
            }
        });
    });

    // -----------------------------------------------------------------
    // 5. Phishing indicator highlight animation on awareness page
    // -----------------------------------------------------------------
    const indicators = document.querySelectorAll(".phishing-indicator");
    if (indicators.length > 0) {
        indicators.forEach((el, i) => {
            el.style.opacity = "0";
            el.style.transform = "translateY(12px)";
            el.style.transition = `opacity 0.5s ease ${i * 0.15}s, transform 0.5s ease ${i * 0.15}s`;
            // Trigger animation
            requestAnimationFrame(() => {
                el.style.opacity = "1";
                el.style.transform = "translateY(0)";
            });
        });
    }
});
