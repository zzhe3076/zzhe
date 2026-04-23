const API_BASE = 'http://localhost:8000/api';

Page({
  data: {
    stats: {},
    announcements: [],
    faqs: [],
    isLoggedIn: false
  },

  onLoad() {
    this.loadData();
  },

  onShow() {
    this.checkLoginStatus();
  },

  checkLoginStatus() {
    const studentId = wx.getStorageSync('student_id');
    this.setData({ isLoggedIn: !!studentId });
  },

  loadData() {
    wx.request({
      url: `${API_BASE}/dashboard/stats/`,
      success: res => {
        if (res.data.student_stats) {
          this.setData({ stats: res.data.student_stats });
        }
      }
    });

    wx.request({
      url: `${API_BASE}/announcements/`,
      success: res => {
        if (res.data.results) {
          this.setData({ announcements: res.data.results.slice(0, 3) });
        }
      }
    });

    wx.request({
      url: `${API_BASE}/faqs/`,
      success: res => {
        if (res.data.results) {
          this.setData({ faqs: res.data.results.slice(0, 3) });
        }
      }
    });
  },

  goToCheckin() {
    if (!this.data.isLoggedIn) {
      wx.navigateTo({ url: '/pages/login/login' });
      return;
    }
    wx.navigateTo({ url: '/pages/qrcode/qrcode' });
  },

  goToPayment() {
    if (!this.data.isLoggedIn) {
      wx.navigateTo({ url: '/pages/login/login' });
      return;
    }
    wx.navigateTo({ url: '/pages/payment/payment' });
  },

  goToDormitory() {
    if (!this.data.isLoggedIn) {
      wx.navigateTo({ url: '/pages/login/login' });
      return;
    }
    wx.navigateTo({ url: '/pages/dormitory/dormitory' });
  }
});
