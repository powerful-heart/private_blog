

def paging(contents):
    paginator = Paginator(article_list, 10)
    count = paginator.count
    num_pages = paginator.num_pages
    # 页码列表
    page_range = paginator.page_range  # type:int

    try:
        current_num = int(request.GET.get('page', 1))
    except:
        current_num = 1
    print('当前页数', current_num)
    # 不在页面范围内的安全处理
    if current_num < 1:
        current_num = 1
        return redirect('/home/?page=%s' % current_num)
    elif current_num > num_pages:
        current_num = num_pages
        return redirect('/home/?page=%s' % current_num)

    current_page = paginator.page(current_num)
    print('>>>', current_page)

    # 通过page_range来控制页面版面
    if num_pages > 10:
        if current_num < 4:
            page_range = range(2, 5)
        elif current_num > num_pages - 3:
            page_range = range(num_pages - 3, num_pages)
        else:
            page_range = range(current_num - 1, current_num + 2)
