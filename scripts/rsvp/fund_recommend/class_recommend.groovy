class_recommend_type = 0

if ( !etf ) {
    if ( 股票 || 业绩指标 ) {
        if ( 业绩指标 && !股票 ) {
            if ( !数字 ) { class_recommend_type = 1 }  // 1.收益指标
            else { class_recommend_type = 2 }  // 2.业绩指标
        } else if ( !业绩指标 && 股票 ) { class_recommend_type = 3 }  // 3.重仓股
    } else {
        if ( 行业板块 || 筛选条件 || 指数 || 投资偏好 ) {
            if ( 行业板块 ) { class_recommend_type = 4 }  // 4.行业板块
            else if ( 筛选条件 ) { class_recommend_type = 5 }  // 5.筛选条件
            else if ( 投资偏好 ) { class_recommend_type = 6 }  // 6.投资偏好
            else if ( etf || ETF类型 ) { class_recommend_type = 7 }  // 7.ETF基金
            else { class_recommend_type = 8 }  // 8.精选指数
        } else if ( 基金类型 ) { class_recommend_type = 9 }  // 9.基金类型
        else { class_recommend_type = 10 }  // 10.追求更高收益
    }
}

recommend_type = null
prefix_message = null
jump_url = null
quick_reply = []