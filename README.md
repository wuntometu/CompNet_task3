# 反向TCP客户端-服务器示例

## 简介

本项目实现了一个简单的TCP客户端-服务器应用程序，其中客户端将ASCII文本块发送给服务器，服务器将每个块反转并返回。此外，客户端还将反转后的整个内容保存到文本文件中。

该项目演示了使用Python进行基本的TCP套接字客户端-服务器通信。

### 运行环境

- Python 版本：Python 3.10
- 操作系统：任何支持 Python 的操作系统（Windows、Linux、macOS）

## 功能特点

- **TCP通信**：客户端和服务器通过TCP套接字进行通信。
- **分块数据处理**：客户端将不定长的ASCII文本块发送给服务器。
- **文本反转**：服务器反转收到的每个文本块。
- **文件输出**：客户端将整个反转后的文本保存到文件中。

## 安装

1. 克隆仓库：

   ```bash
   git clone https://github.com/your_username/reverse-tcp-client-server.git
   cd reverse-tcp-client-server
