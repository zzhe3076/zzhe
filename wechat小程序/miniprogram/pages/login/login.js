const API_BASE = 'http://localhost:8000/api';

Page({
  data: {
    studentId: '',
    password: ''
  },

  onStudentIdInput(e) {
    this.setData({ studentId: e.detail.value });
  },

  onPasswordInput(e) {
    this.setData({ password: e.detail.value });
  },

  handleLogin() {
    const { studentId, password } = this.data;
    
    if (!studentId || !password) {
      wx.showToast({ title: '请填写完整信息', icon: 'none' });
      return;
    }

    wx.showLoading({ title: '登录中...' });

    wx.request({
      url: `${API_BASE}/students/`,
      success: res => {
        wx.hideLoading();
        
        const students = res.data.results || res.data;
        const student = students.find(s => s.student_id === studentId);
        
        if (student) {
          wx.setStorageSync('student_id', student.id);
          wx.setStorageSync('student_name', student.name);
          wx.showToast({ title: '登录成功', icon: 'success' });
          setTimeout(() => {
            wx.switchTab({ url: '/pages/dashboard/dashboard' });
          }, 1500);
        } else {
          wx.showToast({ title: '学号不存在', icon: 'none' });
        }
      },
      fail: err => {
        wx.hideLoading();
        wx.showToast({ title: '登录失败', icon: 'none' });
      }
    });
  },

  handleWechatLogin() {
    wx.showLoading({ title: '登录中...' });
    
    wx.login({
      success: res => {
        wx.request({
          url: `${API_BASE}/wechat/login/`,
          method: 'POST',
          data: { code: res.code },
          success: loginRes => {
            wx.hideLoading();
            
            if (loginRes.data.success) {
              wx.setStorageSync('openid', loginRes.data.openid);
              wx.navigateTo({ url: '/pages/bind/bind' });
            } else {
              wx.showToast({ title: '微信登录失败', icon: 'none' });
            }
          },
          fail: () => {
            wx.hideLoading();
            wx.showToast({ title: '微信登录失败', icon: 'none' });
          }
        });
      },
      fail: () => {
        wx.hideLoading();
        wx.showToast({ title: '微信登录失败', icon: 'none' });
      }
    });
  }
});
