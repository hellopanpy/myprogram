#--*--coding:utf8--*--


from lxml import etree
html="""
    <div>hello<p>H</p>
        <p>J</p>
        <p>I</p>
</div>
<div>hehe</div>
"""
sel = etree.HTML(html)
con = sel.xpath('//div[text()="hello"]/p[posision()=2]/text()')
print con
