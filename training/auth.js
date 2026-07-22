/*
  auth.js — cổng đăng nhập đơn giản cho trang đào tạo Micro:bit.

  LƯU Ý QUAN TRỌNG (đã thống nhất với người dùng):
  Đây KHÔNG PHẢI là xác thực bảo mật thật sự. GitHub Pages chỉ phục vụ file
  tĩnh (HTML/JS), không có máy chủ backend, nên:
    - Toàn bộ danh sách tài khoản (users.json) đều có thể xem được nếu ai đó
      mở DevTools hoặc tải trực tiếp file này.
    - Mật khẩu được băm bằng SHA-256 trước khi lưu, nhưng ai cố ý bỏ qua
      bước kiểm tra (sửa JS trong trình duyệt) vẫn có thể vào thẳng trang.
  Mục đích của cổng này chỉ là NGĂN NGƯỜI XEM NGẪU NHIÊN, phù hợp cho một
  lớp học nội bộ — không dùng để bảo vệ thông tin thực sự quan trọng.
*/

async function sha256Hex(text) {
  const enc = new TextEncoder().encode(text);
  const buf = await crypto.subtle.digest('SHA-256', enc);
  return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
}

async function loadUsers() {
  const res = await fetch('users.json', { cache: 'no-store' });
  if (!res.ok) throw new Error('Không tải được users.json');
  return res.json();
}

async function tryLogin(username, password) {
  username = (username || '').trim();
  const users = await loadUsers();
  if (!users[username]) return false;
  const hash = await sha256Hex(password || '');
  return users[username].toLowerCase() === hash.toLowerCase();
}

function setSession(username) {
  sessionStorage.setItem('mb_auth_user', username);
}

function isLoggedIn() {
  return sessionStorage.getItem('mb_auth_user') !== null;
}

function requireAuth() {
  if (!isLoggedIn()) {
    const here = encodeURIComponent(location.pathname.split('/').pop());
    location.href = 'login.html?next=' + here;
  }
}

function logout() {
  sessionStorage.removeItem('mb_auth_user');
  location.href = 'login.html';
}
