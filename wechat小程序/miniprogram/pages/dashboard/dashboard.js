const API_BASE = 'http://localhost:8000/api';

Page({
  data: {
    student: {},
    dynamicCode: '',
    expiresTime: ''
  },

  onShow() {
    this.loadDashboard();
  },

  loadDashboard() {
    const studentId = wx.getStorageSync('student_id');
    if (!studentId) {
      wx.navigateTo({ url: '/pages/login/login' });
      return;
    }

    wx.request({
      url: `${API_BASE}/students/${studentId}/`,
      success: res => {
        if (res.data) {
          this.setData({ student: res.data });
        }
      }
    });
  },

  generateCode() {
    wx.showLoading({ title: '生成中...' });
    
    wx.request({
      url: `${API_BASE}/students/${this.data.student.id}/generate_dynamic_code/`,
      method: 'POST',
      success: res => {
        wx.hideLoading();
        
        if (res.data.dynamic_code) {
          this.setData({
            dynamicCode: res.data.dynamic_code,
            expiresTime: new Date(res.data.expires_at).toLocaleString()
          });
        }
      },
      fail: () => {
        wx.hideLoading();
        wx.showToast({ title: '获取失败', icon: 'none' });
      }
    });
  },

  goToPayment() {
    wx.navigateTo({ url: '/pages/payment/payment' });
  },

  goToDormitory() {
    wx.navigateTo({ url: '/pages/dormitory/dormitory' });
  },

  goToAnnouncement() {
    wx.navigateTo({ url: '/pages/announcement/announcement' });
  },

  handleLogout() {
    wx.showModal({
      title: '提示',
      content: '确定要退出登录吗？',
      success: res => {
        if (res.confirm) {
          wx.clearStorageSync();
          wx.navigateTo({ url: '/pages/login/login' });
        }
      }
    });
  }
});
