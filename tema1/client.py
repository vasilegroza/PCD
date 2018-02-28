import socket
import argparse
import struct
import time
import os
import random
import string

STREAMING_MODE = 0
SEND_AND_WAIT_MODE = 1
BLOCK_SIZE = 1024


# def random_generator(size, chars=string.ascii_uppercase + string.digits):
#     return ''.join(random.choice(chars) for x in range(size))


def stream_file(client_socket: socket.socket, file_path: str):
    transfer_mode_bytes = struct.pack('i', STREAMING_MODE)
    print("send to server tranfer_mode --> stream (0 --> stream; 1--> send_and_wait)")
    client_socket.send(transfer_mode_bytes)


    file_name = os.path.basename(file_path)
    file_name_size_bytes = struct.pack('i',len(file_name))
    client_socket.send(file_name_size_bytes)
    client_socket.send(file_name.encode('utf-8'))

    total_bytes_sent = 0
    total_messages_sent = 0
    start_time = ctime_millis()

    file_size = os.path.getsize(file_path)
    try:
        f = open(file_path, 'rb')
        while file_size > 0:
            if BLOCK_SIZE < file_size:
                sent_size = BLOCK_SIZE
            else:
                sent_size = file_size
            message = f.read(sent_size)
            client_socket.send(message)
            file_size -= sent_size

            total_bytes_sent += sent_size
            total_messages_sent += 1


    except:
        pass

    print("Done sending file {} ".format(file_path))
    client_socket.shutdown(socket.SHUT_RDWR)
    client_socket.close()


    end_time = ctime_millis()
    time_diff = end_time-start_time

    print("File was sent in:              {}".format(nice_time(time_diff)))
    print("Total number of messages sent: {}".format(total_messages_sent))
    print("Total number of bytes sent:    {}".format(total_bytes_sent))


def send_and_wait_file(client_socket: socket.socket):
    transfer_mode_bytes = struct.pack('i', SEND_AND_WAIT_MODE)
    print("send to server tranfer_mode -->send_and_wait (0 --> stream; 1--> send_and_wait)")
    client_socket.send(transfer_mode_bytes)

    file_name = os.path.basename(file_path)
    file_name_size_bytes = struct.pack('i',len(file_name))
    client_socket.send(file_name_size_bytes)
    client_socket.send(file_name.encode('utf-8'))

    total_bytes_sent = 0
    total_messages_sent = 0
    start_time = ctime_millis()

    file_size = os.path.getsize(file_path)
    try:
        f = open(file_path, 'rb')
        while file_size > 0:
            if BLOCK_SIZE < file_size:
                sent_size = BLOCK_SIZE
            else:
                sent_size = file_size
            message = f.read(sent_size)
            client_socket.send(message)

            while True:
                #     waiting for ack from server
                try:
                    # unsigmned long long is on 8 bytes Q
                    ACK = client_socket.recv(8)
                    ACK = struct.unpack('Q', ACK)[0]
                    print("ACK is: {}".format(ACK))
                except Exception as e:
                    print(e)
            #         ACK is lost
                    client_socket.send(message)
                else:
                    break;



            file_size -= sent_size

            total_bytes_sent += sent_size
            total_messages_sent += 1


    except:
        pass

    print("Done sending file {} ".format(file_path))
    client_socket.shutdown(socket.SHUT_RDWR)
    client_socket.close()


    end_time = ctime_millis()
    time_diff = end_time-start_time

    print("File was sent in:              {}".format(nice_time(time_diff)))
    print("Total number of messages sent: {}".format(total_messages_sent))
    print("Total number of bytes sent:    {}".format(total_bytes_sent))




def ctime_millis():
    """:returns: Current time in milliseconds."""
    return int(round(time.time() * 1000))


def nice_time(millis):
    """:returns: Nice displaying of time."""
    return "{m} mins, {s} seconds, {mm} millis".format(
        m=str(millis // 1000 // 60),
        s=str(millis // 1000 % 60),
        mm=str(millis % 1000))




if __name__ == "__main__":
    file_path = "/home/vasile/Desktop/javascript_book.tar.xz"
    parser = argparse.ArgumentParser(description='Client homework1.')
    parser.add_argument("-c", "--conn_type", type=str, help="connection type can be TCP or UDP", required=True)
    parser.add_argument("-ip", "--ip_address", type=str, help="ip adress of server", required=True)
    parser.add_argument("-p", "--port", type=int, help="ip adress of server", required=True)
    parser.add_argument("-t", "--transfer_mode", type=int, help="0 --> stream; 1 --> send_and_wait", required=True)
    args = parser.parse_args()

    print(args)
    if args.conn_type == "TCP":
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    elif args.conn_type == "UDP":
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        print("{} unknown or unsupported connection type".format(args.conn_type))
        exit(1)

    server_address = (args.ip_address, args.port)
    print('connecting to {} port {}'.format(server_address[0], server_address[1]))

    client_socket.connect(server_address)

    if args.transfer_mode == STREAMING_MODE:
        print("Start to comunicate in {} mode".format("streaming"))
        stream_file(client_socket, file_path)
    elif args.transfer_mode == SEND_AND_WAIT_MODE:
        print("Start to comunicate in {} mode".format("send_and_wait"))
        send_and_wait_file(client_socket)
    else:
        print("{} uknowk or unsupported send-receive protocol".format(args.transfer_mode));
    pass




