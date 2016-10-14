#--*--coding:utf8--*--

from lxml import etree

html="""
    <body>
        <div id="aa">aa</div>
        <div id="bb">bb</div>
        <div id="ac">cc</div>
    </body>
    """
selector=etree.HTML(html)
content=selector.xpath('//div[starts-with(@id,"a")]/text()')
#这里使用starts-with方法提取div的id标签属性值开头为a的div标签
for each in content:
    print each