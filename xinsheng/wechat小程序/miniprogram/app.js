const API_BASE = 'http://localhost:8000/api';

App({
  globalData: {
    userInfo: null,
    studentId: null,
    token: null
  },

  onLaunch() {
    const studentId = wx.getStorageSync('student_id');
    if (studentId) {
      this.globalData.studentId = studentId;
    }
  },

  getUserInfo() {
    return new Promise((resolve, reject) => {
      if (this.globalData.userInfo) {
        resolve(this.globalData.userInfo);
        return;
      }

      wx.getUserProfile({
        desc: '用于完善用户资料',
        success: res => {
          this.globalData.userInfo = res.userInfo;
          resolve(res.userInfo);
        },
        fail: err => {
          reject(err);
        }
      });
    });
  },

  checkLogin() {
    return new Promise((resolve, reject) => {
      const studentId = wx.getStorageSync('student_id');
      if (studentId) {
        this.globalData.studentId = studentId;
        resolve(true);
      } else {
        resolve(false);
      }
    });
  },

  login(code) {
    return new Promise((resolve, reject) => {
      wx.request({
        url: `${API_BASE}/wechat/login/`,
        method: 'POST',
        data: { code },
        success: res => {
          if (res.data.success) {
            resolve(res.data);
          } else {
            reject(res.data);
          }
        },
        fail: err => {
          reject(err);
        }
      });
    });
  },

  bindStudent(studentId, password) {
    return new Promise((resolve, reject) => {
      wx.request({
        url: `${API_BASE}/wechat/bind/`,
        method: 'POST',
        data: { student_id: studentId, password },
        success: res => {
          if (res.data.success) {
            wx.setStorageSync('student_id', res.data.student.id);
            this.globalData.studentId = res.data.student.id;
            resolve(res.data);
          } else {
            reject(res.data);
          }
        },
        fail: err => {
          reject(err);
        }
      });
    });
  },

  getDashboard() {
    return new Promise((resolve, reject) => {
      wx.request({
        url: `${API_BASE}/wechat/dashboard/`,
        success: res => {
          if (res.data.success) {
            resolve(res.data.data);
          } else {
            reject(res.data);
          }
        },
        fail: err => {
          reject(err);
        }
      });
    });
  },

  generateCode() {
    return new Promise((resolve, reject) => {
      wx.request({
        url: `${API_BASE}/wechat/generate_code/`,
        method: 'POST',
        success: res => {
          if (res.data.success) {
            resolve(res.data);
          } else {
            reject(res.data);
          }
        },
        fail: err => {
          reject(err);
        }
      });
    });
  },

  logout() {
    return new Promise((resolve, reject) => {
      wx.request({
        url: `${API_BASE}/wechat/logout/`,
        method: 'POST',
        success: res => {
          wx.removeStorageSync('student_id');
          this.globalData.studentId = null;
          this.globalData.userInfo = null;
          resolve(res.data);
        },
        fail: err => {
          reject(err);
        }
      });
    });
  }
});
