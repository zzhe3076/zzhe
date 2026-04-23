const API_BASE = 'http://localhost:8000/api';

Page({
  data: {
    hasDormitory: false,
    dormitory: {}
  },

  onShow() {
    this.loadDormitory();
  },

  loadDormitory() {
    const studentId = wx.getStorageSync('student_id');
    if (!studentId) {
      wx.navigateTo({ url: '/pages/login/login' });
      return;
    }

    wx.request({
      url: `${API_BASE}/dormitory-assignments/?student=${studentId}`,
      success: res => {
        const assignments = res.data.results || res.data;
        
        if (assignments.length > 0) {
          const assignment = assignments[0];
          this.setData({
            hasDormitory: true,
            dormitory: {
              building: assignment.room_info,
              room_number: assignment.room.room_number,
              bed_number: assignment.bed_number,
              room_type: assignment.room.room_type === 'standard' ? '标准间' : '升级间',
              price: assignment.room.price,
              current_occupancy: assignment.room.current_occupancy,
              capacity: assignment.room.capacity
            }
          });
        } else {
          this.setData({ hasDormitory: false });
        }
      }
    });
  }
});
