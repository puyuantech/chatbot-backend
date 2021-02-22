if (行业板块 != null) {
    if (行业板块.contains('证券')) {
        行业板块 = '证券'
    } else if (行业板块.contains('银行')) {
        行业板块 = '银行'
    }
}
prefix_message = '筛选出以下基金：'