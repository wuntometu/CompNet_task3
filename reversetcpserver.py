import socket
import struct
import threading

# Type
INITIALIZATION = 1
AGREE = 2
REVERSE_REQUEST = 3
REVERSE_ANSWER = 4


# 处理客户端请求的函数
def handle_client(client_socket):
    try:
        while True:
            # 接收报文头部
            header = client_socket.recv(6)
            if not header:
                break

            msg_type, num = struct.unpack('!HI', header)

            if msg_type == INITIALIZATION:
                print(f"接收到Initialization报文: N={num}")

                # 发送Agree报文
                agree_message = struct.pack('!H', AGREE)
                client_socket.sendall(agree_message)

            elif msg_type == REVERSE_REQUEST:
                data_length = num
                data = client_socket.recv(data_length).decode('ascii')
                reversed_data = data[::-1]

                # 发送Reverse Answer报文
                reversed_length = len(reversed_data)
                answer_message = struct.pack('!HI', REVERSE_ANSWER,
                                             reversed_length) + reversed_data.encode('ascii')
                client_socket.sendall(answer_message)

                print(f"处理数据的反转请求: {data}")

    except Exception as e:
        print(f"异常: {e}")
    finally:
        client_socket.close()


# 主函数
def main():
    # 服务器地址和端口
    server_ip = '127.0.0.1'  # 替换为实际服务器IP
    server_port = 12345  # 替换为实际服务器端口

    # 创建套接字
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_ip, server_port))
        server_socket.listen(5)
        print(f"服务器正在监听 {server_ip}:{server_port}")

        try:
            while True:
                client_socket, client_addr = server_socket.accept()
                print(f"连接到客户端: {client_addr}")

                # 在单独的线程中处理客户端
                client_thread = threading.Thread(target=handle_client, args=(client_socket,))
                client_thread.start()

        except KeyboardInterrupt:
            print("服务器已停止。")
        finally:
            server_socket.close()


if __name__ == "__main__":
    main()
