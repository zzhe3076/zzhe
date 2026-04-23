const API_BASE = 'http://localhost:8000/api';

Page({
  data: {
    faqs: []
  },

  onLoad() {
    this.loadFAQs();
  },

  loadFAQs() {
    wx.request({
      url: `${API_BASE}/faqs/`,
      success: res => {
        if (res.data.results) {
          this.setData({ faqs: res.data.results });
        }
      }
    });
  }
});
