#!/usr/bin/env python
# encoding: utf-8
import sys, io, os, arcpy


if __name__ == '__main__':
    # GIS数据合并
    print '[==DoDo==]'
    print 'Bundle Maker.'
    print 'Encode: %s' %  sys.getdefaultencoding()

    indir = './'
    
    print 'scan files'
    dirs = []
    files = []
    # 遍历目录
    for parent,dirnames,filenames in os.walk(indir):
        for dirname in dirnames:
            dirs.append(os.path.join(parent, dirname))
        for filename in filenames:
            files.append(os.path.join(parent, filename))

    # 找出所有SHP文件
    shpfiles = {}
    for fname in files:
        if (fname.lower().endswith('.shp')):
            sdir, sname = os.path.split(fname)
            sfiles = []
            sname = sname.upper()
            if (sname in shpfiles): sfiles = shpfiles[sname]
            else: shpfiles[sname] = sfiles
            sfiles.append(fname)
    
    print 'file count: %s' % len(shpfiles)

    # 合并文件
    num = 0
    sum = len(shpfiles)
    for item in shpfiles:
        name = item.upper().replace('.SHP', '')
        inputs = shpfiles[item]
        output = './data.gdb/%s' % name

        # 处理字段 全部变成文本类型
        fieldMappings = arcpy.FieldMappings()
        for sfile in inputs:
            fieldMappings.addTable(sfile)
        # 修改字段对照表
        for i in range(fieldMappings.fieldCount):
            fm = fieldMappings.getFieldMap(i)
            of = fm.outputField
            of.length = 200
            of.type = u'String'
            fm.outputField = of
            fieldMappings.replaceFieldMap(i, fm)
        
        # 正式合并
        num = num + 1
        print '[%03d/%d]: %s' % (num, sum, name)
        arcpy.Merge_management(inputs, output, fieldMappings)

        

    

    
    print 'OK.'












