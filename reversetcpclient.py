import socket
import os
import struct
import random

# Type
INITIALIZATION = 1
AGREE = 2
REVERSE_REQUEST = 3
REVERSE_ANSWER = 4

# 读取ASCII文件并分出随机块
def read_ascii_file(file_path, Lmin, Lmax):
    with open(file_path, 'r', encoding='ascii') as file:
        data = file.read()
        chunks = []
        total_length = len(data)
        current_idx = 0

        while current_idx < total_length:
            chunk_size = random.randint(Lmin, Lmax)
            if current_idx + chunk_size <= total_length:
                chunks.append(data[current_idx:current_idx + chunk_size])
                current_idx += chunk_size
            else:
                chunks.append(data[current_idx:])
                current_idx = total_length

    return chunks

# 写入到文件中
def write_string_to_file(content, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"字符串内容成功写入文件 {file_path}")
    except IOError:
        print(f"写入文件 {file_path} 时出现错误")

# 发送Initialization报文
def send_initialization(sock, N):
    msg_type = struct.pack('!H', INITIALIZATION)    # !H返回2字节对象
    num_chunks_bytes = struct.pack('!I', N)         # !I返回4字节对象
    message = msg_type + num_chunks_bytes
    sock.sendall(message)


# 发送Reverse Request报文
def send_reverse_request(sock, data, data_length):
    msg_type = struct.pack('!H', REVERSE_REQUEST)
    length_bytes = struct.pack('!I', data_length)
    message = msg_type + length_bytes + data.encode('ascii')
    sock.sendall(message)


# 接收Reverse Answer报文
def receive_reverse_answer(sock):
    header = sock.recv(6)
    msg_type, length = struct.unpack('!HI', header)
    data = sock.recv(length).decode('ascii')
    return data



# 主函数
def main():
    # 服务器地址和端口（命令行参数）
    server_ip = input("请输入服务器IP地址：")
    server_port = int(input("请输入服务器端口号："))

    # 文件路径和块大小（用于测试目的）
    file_path = 'test.txt'  # 替换为实际ASCII文件路径
    Lmin = 100  # 替换为期望的最小块大小
    Lmax = 500  # 替换为期望的最大块大小

    # 读取ASCII文件并分块
    chunks = read_ascii_file(file_path, Lmin, Lmax)
    N = len(chunks)

    # 连接到服务器
    out_put = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_ip, server_port))

        # 发送Initialization报文
        send_initialization(client_socket, N)

        # 接收服务器的Agree报文
        agree_message = client_socket.recv(2)
        print(f"接收到Agree报文: 类型={struct.unpack('!H', agree_message)[0]}")

        # 逐个发送每个块作为Reverse Request并接收Reverse Answer
        for idx, chunk in enumerate(chunks):
            data_length = len(chunk)
            send_reverse_request(client_socket, chunk, data_length)
            reversed_text = receive_reverse_answer(client_socket)
            out_put += reversed_text
            print(f"{idx + 1} : {reversed_text}")

        # 输出到结果文件
        write_string_to_file(out_put, "reverse.txt")

    print("客户端完成所有块的接收和处理。")


if __name__ == "__main__":
    main()
