const API_BASE = 'http://localhost:8000/api';

Page({
  data: {
    studentId: '',
    password: ''
  },

  onLoad() {
    const openid = wx.getStorageSync('openid');
    if (!openid) {
      wx.navigateBack();
    }
  },

  onStudentIdInput(e) {
    this.setData({ studentId: e.detail.value });
  },

  onPasswordInput(e) {
    this.setData({ password: e.detail.value });
  },

  handleBind() {
    const { studentId, password } = this.data;

    if (!studentId || !password) {
      wx.showToast({ title: '请填写完整信息', icon: 'none' });
      return;
    }

    wx.showLoading({ title: '绑定中...' });

    wx.request({
      url: `${API_BASE}/wechat/bind/`,
      method: 'POST',
      data: {
        student_id: studentId,
        password: password
      },
      success: res => {
        wx.hideLoading();

        if (res.data.success) {
          wx.setStorageSync('student_id', res.data.student.id);
          wx.showToast({ title: '绑定成功', icon: 'success' });
          setTimeout(() => {
            wx.switchTab({ url: '/pages/dashboard/dashboard' });
          }, 1500);
        } else {
          wx.showToast({ title: res.data.error, icon: 'none' });
        }
      },
      fail: () => {
        wx.hideLoading();
        wx.showToast({ title: '绑定失败', icon: 'none' });
      }
    });
  }
});
