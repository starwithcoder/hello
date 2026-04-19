const API_BASE_URL = 'http://192.168.1.2:5000/api';

const http = {
  async request(url, options = {}) {
    const token = localStorage.getItem('token');
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(`${API_BASE_URL}${url}`, {
        ...options,
        headers
      });

      if (response.status === 401) {
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('token');
        window.location.href = 'login.html';
        throw new Error('Unauthorized');
      }

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Request failed');
      }

      return data;
    } catch (error) {
      console.error('HTTP Error:', error);
      throw error;
    }
  },

  get(url, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const fullUrl = queryString ? `${url}?${queryString}` : url;
    return this.request(fullUrl, { method: 'GET' });
  },

  post(url, data = {}) {
    return this.request(url, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  },

  put(url, data = {}) {
    return this.request(url, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  },

  delete(url) {
    return this.request(url, { method: 'DELETE' });
  }
};

function showMessage(message, type = 'info') {
  let msgClass = 'info';
  if (type === 'success') msgClass = 'success';
  else if (type === 'error') msgClass = 'error';
  else if (type === 'warning') msgClass = 'warning';

  const msgDiv = document.createElement('div');
  msgDiv.className = `message message-${msgClass}`;
  msgDiv.textContent = message;
  msgDiv.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 10px 20px;
    background-color: ${type === 'success' ? '#67c23a' : type === 'error' ? '#f56c6c' : type === 'warning' ? '#e6a23c' : '#909399'};
    color: #fff;
    border-radius: 4px;
    z-index: 9999;
    animation: slideIn 0.3s ease;
  `;

  document.body.appendChild(msgDiv);

  setTimeout(() => {
    msgDiv.style.animation = 'slideOut 0.3s ease';
    setTimeout(() => msgDiv.remove(), 300);
  }, 3000);
}

function showConfirm(message, title = '确认') {
  return new Promise((resolve) => {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: rgba(0, 0, 0, 0.5);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 1000;
    `;

    overlay.innerHTML = `
      <div class="modal" style="min-width: 300px;">
        <div class="modal-header">
          <h3>${title}</h3>
          <button class="modal-close" onclick="this.closest('.modal-overlay').remove(); window._confirmResolve(false);">&times;</button>
        </div>
        <div class="modal-body">
          <p>${message}</p>
        </div>
        <div class="modal-footer">
          <button class="btn" id="cancelBtn">取消</button>
          <button class="btn btn-primary" id="confirmBtn">确定</button>
        </div>
      </div>
    `;

    document.body.appendChild(overlay);

    overlay.querySelector('#confirmBtn').onclick = () => {
      overlay.remove();
      resolve(true);
    };

    overlay.querySelector('#cancelBtn').onclick = () => {
      overlay.remove();
      resolve(false);
    };

    window._confirmResolve = resolve;
  });
}

function openModal(title, content, onSave, onClose) {
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  overlay.id = 'dynamicModal';

  overlay.innerHTML = `
    <div class="modal" style="width: 500px; max-width: 90vw;">
      <div class="modal-header">
        <h3>${title}</h3>
        <button class="modal-close" id="modalCloseBtn">&times;</button>
      </div>
      <div class="modal-body">
        ${content}
      </div>
      <div class="modal-footer">
        <button class="btn" id="modalCancelBtn">取消</button>
        <button class="btn btn-primary" id="modalSaveBtn">保存</button>
      </div>
    </div>
  `;

  document.body.appendChild(overlay);

  overlay.querySelector('#modalCloseBtn').onclick = () => {
    closeModal();
    if (onClose) onClose();
  };

  overlay.querySelector('#modalCancelBtn').onclick = () => {
    closeModal();
    if (onClose) onClose();
  };

  overlay.querySelector('#modalSaveBtn').onclick = () => {
    if (onSave) onSave();
  };

  overlay.onclick = (e) => {
    if (e.target === overlay) {
      closeModal();
      if (onClose) onClose();
    }
  };

  function closeModal() {
    const modal = document.getElementById('dynamicModal');
    if (modal) modal.remove();
  }

  return { close: closeModal };
}

function closeModal() {
  const modal = document.getElementById('dynamicModal');
  if (modal) modal.remove();
}

function formatDate(date) {
  if (!date) return '';
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hours = String(d.getHours()).padStart(2, '0');
  const minutes = String(d.getMinutes()).padStart(2, '0');
  const seconds = String(d.getSeconds()).padStart(2, '0');
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

function formatDateShort(date) {
  if (!date) return '';
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

function isLoggedIn() {
  return localStorage.getItem('isLoggedIn') === 'true';
}

function logout() {
  localStorage.removeItem('isLoggedIn');
  localStorage.removeItem('token');
  window.location.href = 'login.html';
}

function getToken() {
  return localStorage.getItem('token');
}

function jwtDecode(token) {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(function(c) {
          return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        })
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch (error) {
    console.error('JWT decode error:', error);
    return null;
  }
}

function getUserPermissions() {
  const token = getToken();
  if (!token) return [];
  const payload = jwtDecode(token);
  return payload ? (payload.permissions || []) : [];
}

function hasPermission(permissionId) {
  const permissions = getUserPermissions();
  return permissions.includes(permissionId);
}

function initPage() {
  if (!isLoggedIn() && !window.location.href.includes('login.html') && !window.location.href.includes('register.html')) {
    window.location.href = 'login.html';
  }
}

const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }
  @keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
  }
`;
document.head.appendChild(style);
