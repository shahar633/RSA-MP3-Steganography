SIZE_HEADER_FORMAT = "000000000|"
size_header_size = len(SIZE_HEADER_FORMAT)


def recv_by_size(sock):
    str_size = b""
    data_len = 0
    while len(str_size) < size_header_size:
        str_size += sock.recv(size_header_size - len(str_size))
        if str_size == b"":
            break
    data = b""
    if str_size != b"":
        data_len = int(str_size[:size_header_size - 1])
        while len(data) < data_len:
            data += sock.recv(data_len - len(data))
            if data == b"":
                break

    if data_len != len(data):
        data = ""
    return data


def send_with_size(sock, data):
    header = str(len(data)).zfill(size_header_size - 1).encode() + b"|"
    sock.sendall(header + data)
