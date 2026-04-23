const API_BASE = 'http://localhost:8000/api';

Page({
  data: {
    payments: [],
    pendingTotal: '0.00',
    paidTotal: '0.00'
  },

  onShow() {
    this.loadPayments();
  },

  loadPayments() {
    const studentId = wx.getStorageSync('student_id');
    if (!studentId) {
      wx.navigateTo({ url: '/pages/login/login' });
      return;
    }

    wx.request({
      url: `${API_BASE}/payments/?student_id=${studentId}`,
      success: res => {
        const payments = res.data.results || res.data;
        
        let pending = 0;
        let paid = 0;
        
        payments.forEach(p => {
          if (p.status === 'pending') {
            pending += parseFloat(p.amount);
          } else if (p.status === 'paid') {
            paid += parseFloat(p.amount);
          }
        });

        this.setData({
          payments: payments,
          pendingTotal: pending.toFixed(2),
          paidTotal: paid.toFixed(2)
        });
      }
    });
  },

  handlePay(e) {
    const paymentId = e.currentTarget.dataset.id;
    
    wx.showModal({
      title: '确认支付',
      content: '确定要支付该费用吗？',
      success: res => {
        if (res.confirm) {
          wx.showToast({ title: '支付功能待集成', icon: 'none' });
        }
      }
    });
  }
});
