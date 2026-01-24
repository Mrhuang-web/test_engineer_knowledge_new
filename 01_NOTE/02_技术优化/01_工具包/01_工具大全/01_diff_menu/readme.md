一、文件标识判断【根据pk_difference的file2对应文件进行判断 -- file1的文件是没有颜色的  --> file2是传现网的、因此看现网文件】
    以下文件是以生产文件来判断【如果file2为测试环境、那么红和白就是反过来的】
    绿色：测试环境和现网都存在的会标记绿色---一般升级后应该是一致的
    白色：没有颜色标识的是测试环境没有但是现网确有的---测试环境缺的菜单或者按钮  [需要肉眼去对比以下]
    红色：测试环境有但是现网不存在的---应该是新增或者修改的菜单或者按钮

二、所有省份的菜单和按钮都直接调用即可【主要是Showitems库里面的get_items和pk_difference函数】
    Showitems.get_items(r'./XlsxFile/dcim_prod.xlsx', r'./JsonFile/dcim_prod.json')
    Showitems.get_items(r'./XlsxFile/dcim_test.xlsx', r'./JsonFile/dcim_test.json')
    pk_difference(file1=r'./XlsxFile/dcim_prod.xlsx', file2=r'./XlsxFile/dcim_test.xlsx')

三、重复执行会覆盖原有的xlsx文件【】
    生成的xlsx文件在XlsxFile目录下

四、功能完善
    目前版本支持对勾选的按钮进行判断【通过json文件的checked字段判断】
        修改定位：
            get_items函数下
                if 'children' in node and 'text' in node and 'id' in node and 'checked' in node:  # 控制是否选中

五、问题描述
    目前有些json下来只有是缺少"data": {}上级、需要手动添加上去【可以写个判断直接从treeNodes开始】