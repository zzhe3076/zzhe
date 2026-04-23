const API_BASE = 'http://localhost:8000/api';

Page({
  data: {
    dynamicCode: '',
    expiresTime: '',
    checkinResult: false
  },

  onShow() {
    this.loadCode();
  },

  loadCode() {
    const studentId = wx.getStorageSync('student_id');
    if (!studentId) {
      wx.navigateTo({ url: '/pages/login/login' });
      return;
    }
  },

  generateCode() {
    const studentId = wx.getStorageSync('student_id');
    if (!studentId) {
      wx.navigateTo({ url: '/pages/login/login' });
      return;
    }

    wx.showLoading({ title: '生成中...' });

    wx.request({
      url: `${API_BASE}/students/${studentId}/generate_dynamic_code/`,
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

  handleScan() {
    wx.scanCode({
      success: res => {
        this.processQRCode(res.result);
      }
    });
  },

  processQRCode(result) {
    try {
      const data = JSON.parse(result);
      
      wx.showLoading({ title: '验证中...' });

      wx.request({
        url: `${API_BASE}/wechat/verify_checkin/`,
        method: 'POST',
        data: {
          student_id: data.student_id,
          dynamic_code: data.code,
          location: '小程序扫码',
          check_in_method: 'qrcode'
        },
        success: res => {
          wx.hideLoading();

          if (res.data.success) {
            this.setData({ checkinResult: true });
            wx.showToast({ title: '报到成功', icon: 'success' });
          } else {
            wx.showToast({ title: res.data.error, icon: 'none' });
          }
        },
        fail: () => {
          wx.hideLoading();
          wx.showToast({ title: '验证失败', icon: 'none' });
        }
      });
    } catch (e) {
      wx.showToast({ title: '无效二维码', icon: 'none' });
    }
  }
});
