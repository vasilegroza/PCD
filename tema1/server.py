import socket
import threading
import struct
import argparse
import os

STREAMING_MODE=0
SEND_AND_WAIT_MODE=1
BLOCK_SIZE = 1024


bind_ip = '0.0.0.0'
bind_port = 8080

def receive_file_stream_mode(client_socket:socket.socket, args):
    total_bytes_received = 0
    total_messages_received = 0

    file_name_size = client_socket.recv(4)
    file_name_size = struct.unpack('i', file_name_size)[0]

    file_name = client_socket.recv(file_name_size)
    file_name = file_name.decode("utf-8")
    print("start receiving {}".format(file_name))

    with open(os.path.join(os.curdir,file_name),'wb')as f:
        while True:
            message = client_socket.recv(BLOCK_SIZE)
            if not message:
                break

            f.write(message)
            print("Received {} bytes".format(len(message)))

            total_messages_received += 1
            total_bytes_received += len(message)
            # time.sleep(1)

    print("Done receiving file")
    client_socket.close()

    print("Protocol: {}".format(args.conn_type))
    print("Total number of messages received: {}".format(total_messages_received))
    print("Total number of bytes received: {}".format(total_bytes_received))



def receive_file_send_and_wait_mode(client_socket:socket.socket, args):
    total_bytes_received = 0
    total_messages_received = 0

    file_name_size = client_socket.recv(4)
    file_name_size = struct.unpack('i', file_name_size)[0]

    file_name = client_socket.recv(file_name_size)
    file_name = file_name.decode("utf-8")
    print("start receiving {}".format(file_name))

    with open(os.path.join(os.curdir, file_name), 'wb')as f:
        while True:
            message = client_socket.recv(BLOCK_SIZE)
            if not message:
                break

            f.write(message)
            print("Received {} bytes".format(len(message)))

            total_messages_received += 1
            total_bytes_received += len(message)

    #         Send Ack
            ACK = total_bytes_received + 1
            ACK_bytes = struct.pack("Q", ACK)
            client_socket.send(ACK_bytes)
            print("sent ack {}".format(ACK))

    print("Done receiving file")
    client_socket.close()

    print("Protocol: {}".format(args.conn_type))
    print("Total number of messages received: {}".format(total_messages_received))
    print("Total number of bytes received: {}".format(total_bytes_received))

    pass




def handle_client_connection(client_socket:socket.socket, args):
    # To Do :
    # 1 read client transfer mode : - streaming - send&wait
    transfer_mode = client_socket.recv(4)
    # print(transfer_mode)
    transfer_mode = struct.unpack('i',transfer_mode)[0]
    print(transfer_mode)

    if transfer_mode == STREAMING_MODE:
        print("Start to receive in {} mode".format("streaming"))
        receive_file_stream_mode(client_socket, args)
    elif transfer_mode == SEND_AND_WAIT_MODE:
        print("Start to receive in {} mode".format("send_and_wait"))
        receive_file_send_and_wait_mode(client_socket, args)
    else:
        print("{} uknowk or unsupported send-receive protocol".format(transfer_mode));
        pass





if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Server homework1')
    parser.add_argument('-c',"--conn_type", type=str, help="connection type can be TCP or UDP", required=True)
    args = parser.parse_args()

    print(args)
    if  args.conn_type == "TCP":
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif args.conn_type =="UDP":
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        print("{} unknown or unsupported connection type".format(args.conn_type))
        exit(1)
    server.bind((bind_ip,bind_port))

    #maximum 5 client connected at the same time
    server.listen(5)

    print("Listening on {}:{} {} connection".format(bind_ip, bind_port, args.conn_type))

    while True:
        client_socket, address  = server.accept()
        print("Accepted connection from {}:{}".format(address[0], address[1]))
        client_handler = threading.Thread(
            target= handle_client_connection,
            args=(client_socket,args,)
        )
        client_handler.start()
