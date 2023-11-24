import xml.etree.ElementTree as ET

# 功能描述
# 1. 通过读取EPUB3.0的toc.xhtml文件，生成EPUB2.0的toc.ncx文件
# 2. 通过解析ol和li标签，生成ncx文件的navMap部分

nameSpace = "{http://www.w3.org/1999/xhtml}"
# 文件前缀
prefix = "contents/"
# 源文件目录
tree = ET.parse('/xx/toc.xhtml')
root = tree.getroot()
body = root.find(nameSpace+'body')
nav = body.find(nameSpace+'nav')
ol = nav.find(nameSpace+'ol')

# 待生成的ncx文件的根节点
navMap = ET.Element("navMap")
tTree = ET.ElementTree(navMap)

# 循环所有的标签，同时生成一个新的目录树
def getNavPoint(ol, pNavPoint):
    for child in ol:
        # print(child.tag, ":", child.attrib)
        # 如果是li标签，生成navPoint标签
        if child.tag == nameSpace+'li':
            navPoint = None
            if pNavPoint != None:
                navPoint = ET.SubElement(pNavPoint, 'navPoint')
            else:
                navPoint = ET.Element('navPoint')
            navPoint.set('id', child.attrib['id'])
            # 生成navLabel标签
            navLabel = ET.SubElement(navPoint, 'navLabel')
            text = ET.SubElement(navLabel, 'text')
            text.text = child.find(nameSpace+'a').text
            # 生成content标签
            content = ET.SubElement(navPoint, 'content')
            content.set('src', prefix+child.find(nameSpace+'a').attrib['href'])
            # 递归生成子节点
            # 判断是否有ol标签，如果有，递归生成子节点
            if len(child.findall(nameSpace+'ol')) > 0:
                for ol2 in child.findall(nameSpace+'ol'):
                    print("二级", ol2.tag, ":", ol2.attrib)
                    getNavPoint(ol2, navPoint)

            # 将生成的navPoint标签添加到navMap标签中
            if pNavPoint == None:
                navMap.append(navPoint)
                print("添加navPoint标签")


getNavPoint(ol, None)
# 输出文件目录
tTree.write('/xx/test.xml', encoding='utf-8', xml_declaration=True)