// ===== GLOBAL SEARCH =====
const searchInput = document.getElementById('global-search');
const searchDropdown = document.getElementById('search-dropdown');
let searchTimer;

if (searchInput) {
  searchInput.addEventListener('input', () => {
    clearTimeout(searchTimer);
    const q = searchInput.value.trim();
    if (q.length < 2) {
      searchDropdown.classList.add('hidden');
      return;
    }
    searchTimer = setTimeout(async () => {
      const res = await fetch(`/api/search/?q=${encodeURIComponent(q)}`);
      const data = await res.json();
      if (data.results.length === 0) {
        searchDropdown.classList.add('hidden');
        return;
      }
      searchDropdown.innerHTML = data.results.map(r =>
        `<a href="/events/${r.id}/" class="search-item">
          <div>${r.title}</div>
          <div class="date">📅 ${r.date}</div>
        </a>`
      ).join('');
      searchDropdown.classList.remove('hidden');
    }, 300);
  });

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.nav-search')) searchDropdown.classList.add('hidden');
  });
}

// ===== AUTO-DISMISS ALERTS =====
document.querySelectorAll('.alert').forEach(el => {
  setTimeout(() => el.remove(), 4000);
});

// ===== TOAST HELPER =====
function showToast(msg, type = 'success') {
  const t = document.createElement('div');
  t.className = `toast ${type}`;
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 3000);
}

// ===== CSRF HELPER =====
function getCsrf() {
  return document.cookie.split('; ').find(c => c.startsWith('csrftoken='))?.split('=')[1] || '';
}

// ===== REGISTRATION BUTTON =====
const regBtn = document.getElementById('reg-btn');
const unregBtn = document.getElementById('unreg-btn');

if (regBtn) {
  regBtn.addEventListener('click', async () => {
    const eventId = regBtn.dataset.event;
    regBtn.disabled = true;
    const res = await fetch(`/events/${eventId}/register/`, {
      method: 'POST',
      headers: { 'X-CSRFToken': getCsrf(), 'Content-Type': 'application/json' }
    });
    const data = await res.json();
    showToast(data.message, data.status === 'ok' ? 'success' : 'error');
    if (data.status === 'ok') {
      regBtn.style.display = 'none';
      if (unregBtn) unregBtn.style.display = 'inline-block';
      updateParticipantCount(data.count);
    }
    regBtn.disabled = false;
  });
}

if (unregBtn) {
  unregBtn.addEventListener('click', async () => {
    const eventId = unregBtn.dataset.event;
    unregBtn.disabled = true;
    const res = await fetch(`/events/${eventId}/unregister/`, {
      method: 'POST',
      headers: { 'X-CSRFToken': getCsrf(), 'Content-Type': 'application/json' }
    });
    const data = await res.json();
    showToast(data.message, 'success');
    if (data.status === 'ok') {
      unregBtn.style.display = 'none';
      if (regBtn) regBtn.style.display = 'inline-block';
      updateParticipantCount(data.count);
    }
    unregBtn.disabled = false;
  });
}

function updateParticipantCount(count) {
  const el = document.getElementById('participant-count');
  const bar = document.getElementById('progress-bar');
  const max = parseInt(document.getElementById('max-participants')?.textContent || 0);
  if (el) el.textContent = count;
  if (bar && max) bar.style.width = `${Math.min((count / max) * 100, 100)}%`;
}

// ===== COMMENTS =====
document.querySelectorAll('.reply-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const form = btn.closest('.comment').querySelector('.reply-form');
    if (form) form.classList.toggle('open');
  });
});

async function submitComment(form, parentId = null) {
  const textarea = form.querySelector('textarea');
  const text = textarea.value.trim();
  if (!text) return;

  const eventId = form.dataset.event;
  const res = await fetch(`/events/${eventId}/comment/`, {
    method: 'POST',
    headers: { 'X-CSRFToken': getCsrf(), 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, parent_id: parentId })
  });
  const data = await res.json();
  if (data.status === 'ok') {
    textarea.value = '';
    addCommentToDOM(data, parentId);
    showToast('Комментарий добавлен!');
  }
}

function addCommentToDOM(data, parentId) {
  const html = `
    <div class="comment" id="comment-${data.id}">
      <div class="comment-header">
        <span class="comment-user">${data.user}</span>
        <span>${data.created_at}</span>
      </div>
      <div>${data.text}</div>
    </div>`;
  if (parentId) {
    const parent = document.getElementById(`comment-${parentId}`);
    if (parent) {
      const repliesDiv = parent.querySelector('.replies') || (() => {
        const d = document.createElement('div');
        d.className = 'comment-reply replies';
        parent.appendChild(d);
        return d;
      })();
      repliesDiv.insertAdjacentHTML('beforeend', html);
    }
  } else {
    const list = document.getElementById('comments-list');
    if (list) list.insertAdjacentHTML('beforeend', html);
  }
}

const mainCommentForm = document.getElementById('main-comment-form');
if (mainCommentForm) {
  mainCommentForm.querySelector('button[type=submit]')?.addEventListener('click', (e) => {
    e.preventDefault();
    submitComment(mainCommentForm);
  });
}

document.querySelectorAll('.reply-submit').forEach(btn => {
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    const form = btn.closest('form');
    const parentId = parseInt(form.dataset.parent);
    submitComment(form, parentId);
  });
});

// ===== FILTER TABS =====
document.querySelectorAll('.filter-btn[data-filter]').forEach(btn => {
  btn.addEventListener('click', () => {
    const url = new URL(window.location);
    url.searchParams.set('time', btn.dataset.filter);
    window.location = url;
  });
});
