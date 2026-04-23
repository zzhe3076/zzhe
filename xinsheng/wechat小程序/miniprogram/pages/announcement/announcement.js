const API_BASE = 'http://localhost:8000/api';

Page({
  data: {
    announcements: []
  },

  onLoad() {
    this.loadAnnouncements();
  },

  loadAnnouncements() {
    wx.request({
      url: `${API_BASE}/announcements/`,
      success: res => {
        if (res.data.results) {
          this.setData({ announcements: res.data.results });
        }
      }
    });
  }
});
