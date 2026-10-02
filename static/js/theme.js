// LostInCampus - Theme Switcher (Light & Dark Mode)
(function() {
  const savedTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
})();

document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('theme-toggle');
  if (!toggleBtn) return;

  const updateToggleUI = (theme) => {
    if (theme === 'dark') {
      toggleBtn.innerHTML = '<i class="fa-solid fa-sun" style="color: #f59e0b;"></i> <span class="theme-text">Light</span>';
      toggleBtn.setAttribute('title', 'Switch to Light Mode');
    } else {
      toggleBtn.innerHTML = '<i class="fa-solid fa-moon" style="color: #6366f1;"></i> <span class="theme-text">Dark</span>';
      toggleBtn.setAttribute('title', 'Switch to Dark Mode');
    }
  };

  let currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
  updateToggleUI(currentTheme);

  toggleBtn.addEventListener('click', () => {
    currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', currentTheme);
    localStorage.setItem('theme', currentTheme);
    updateToggleUI(currentTheme);
  });
});
