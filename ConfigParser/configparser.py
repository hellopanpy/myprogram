#!/usr/bin/env python
# --*--coding=utf-8--*--

import ConfigParser

# create a ConfigParser instance
cf=ConfigParser.ConfigParser()

# read a config file
cf.read('test.conf')

# return sections
sect=cf.sections()
print "section: ",sect

# return options
opt=cf.options("sec_a")
print "options: ",opt

# return items
items=cf.items("sec_a")
print "items: ",items

# read values
str_v=cf.get("sec_a", "a_key1")
int_v=cf.getint("sec_a", "a_key1")
print "string value :",str_v
print "int value: ",int_v

# set new value
cf.set("sec_b", "b_key3", "new-$r")
# set new key
cf.set("sec_b", "new_key", "new_value")
# create new section
cf.add_section('a_new_section')
# write to file 
cf.write(open("test.conf", "w"))

