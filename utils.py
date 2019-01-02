def make_file(name, size):
    buf_fd = open(name, 'w+b')
    buf_fd.seek(size - 1)
    buf_fd.write(b'\0')
    buf_fd.close()
