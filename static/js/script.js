// ==========================================================
// Pavithira J — Portfolio frontend logic
// ==========================================================

document.addEventListener("DOMContentLoaded", () => {
  initTypingEffect();
  initMobileNav();
  initScrollReveal();
  initContactForm();
  document.getElementById("year").textContent = new Date().getFullYear();
});

// ---------- Typing effect ----------

function initTypingEffect() {
  const el = document.getElementById("typedRole");
  if (!el) return;

  const roles = [
    "Full Stack Developer",
    "Python & Flask Developer",
    "Building Modern Web Apps",
  ];

  const TYPE_SPEED = 65;
  const DELETE_SPEED = 35;
  const PAUSE_AFTER_TYPE = 1500;
  const PAUSE_AFTER_DELETE = 300;

  let roleIndex = 0;
  let charIndex = 0;
  let deleting = false;

  function tick() {
    const current = roles[roleIndex];

    if (!deleting) {
      charIndex++;
      el.textContent = current.slice(0, charIndex);
      if (charIndex === current.length) {
        deleting = true;
        return setTimeout(tick, PAUSE_AFTER_TYPE);
      }
      return setTimeout(tick, TYPE_SPEED);
    }

    charIndex--;
    el.textContent = current.slice(0, charIndex);
    if (charIndex === 0) {
      deleting = false;
      roleIndex = (roleIndex + 1) % roles.length;
      return setTimeout(tick, PAUSE_AFTER_DELETE);
    }
    return setTimeout(tick, DELETE_SPEED);
  }

  tick();
}

// ---------- Mobile nav ----------

function initMobileNav() {
  const toggle = document.getElementById("navToggle");
  const links = document.getElementById("navLinks");
  if (!toggle || !links) return;

  toggle.addEventListener("click", () => {
    const isOpen = links.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", String(isOpen));
  });

  links.querySelectorAll("a").forEach((a) => {
    a.addEventListener("click", () => {
      links.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    });
  });
}

// ---------- Scroll reveal ----------

function initScrollReveal() {
  const targets = document.querySelectorAll(
    ".section-eyebrow, .section-title, .glass-card, .about-text, .timeline-item"
  );

  targets.forEach((t) => t.classList.add("reveal"));

  if (!("IntersectionObserver" in window)) {
    targets.forEach((t) => t.classList.add("is-visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -60px 0px" }
  );

  targets.forEach((t) => observer.observe(t));
}

// ---------- Contact form ----------

function initContactForm() {
  const form = document.getElementById("contactForm");
  if (!form) return;

  const statusEl = document.getElementById("formStatus");
  const submitBtn = form.querySelector(".form-submit");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    clearErrors(form);
    statusEl.textContent = "";
    statusEl.className = "form-status";

    const payload = {
      name: form.name.value.trim(),
      email: form.email.value.trim(),
      subject: form.subject.value.trim(),
      message: form.message.value.trim(),
    };

    submitBtn.disabled = true;
    submitBtn.querySelector(".btn-text").textContent = "Sending...";

    try {
      const res = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();

      if (res.ok && data.success) {
        statusEl.textContent = data.message || "Message sent successfully.";
        statusEl.className = "form-status success";
        form.reset();
      } else if (data.errors) {
        showErrors(form, data.errors);
        statusEl.textContent = "Please fix the highlighted fields.";
        statusEl.className = "form-status error";
      } else {
        statusEl.textContent = "Something went wrong. Please try again.";
        statusEl.className = "form-status error";
      }
    } catch (err) {
      statusEl.textContent = "Network error — please try again.";
      statusEl.className = "form-status error";
    } finally {
      submitBtn.disabled = false;
      submitBtn.querySelector(".btn-text").textContent = "Send Message";
    }
  });
}

function showErrors(form, errors) {
  Object.entries(errors).forEach(([field, message]) => {
    const errorEl = document.getElementById(`err-${field}`);
    const input = form[field];
    if (errorEl) errorEl.textContent = message;
    if (input && input.closest(".form-row")) {
      input.closest(".form-row").classList.add("has-error");
    }
  });
}

function clearErrors(form) {
  form.querySelectorAll(".form-error").forEach((el) => (el.textContent = ""));
  form.querySelectorAll(".form-row").forEach((el) => el.classList.remove("has-error"));
}
