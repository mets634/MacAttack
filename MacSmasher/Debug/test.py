import md5

target = '\x00' * 15 + '\x03'
m = md5.new()
m.update(target)

print m.digest()
print 0
