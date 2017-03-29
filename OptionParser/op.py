from optparse import OptionParser

parser = OptionParser()
###创建一个 OptionParser 对象


parser.add_option("-f", "--file",action="store", type="string", dest="filename")
parser.add_option("-t", "--true",action="store_true",  dest="true")
###定义命令行参数
args = ["-t","-f", "foo.txt"]

(options, args) = parser.parse_args(args)

print options.filename
print options.true
