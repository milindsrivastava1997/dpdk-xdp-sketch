import xxhash

input1 = 'a\n'
input2 = 'abc\n'

print(hex(xxhash.xxh32_intdigest(input1)), xxhash.xxh32_hexdigest(input1))
print(hex(xxhash.xxh32_intdigest(input2)), xxhash.xxh32_hexdigest(input2))
