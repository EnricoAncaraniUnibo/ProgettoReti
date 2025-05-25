import socket
import time
import random

SERVER_IP = 'localhost'
SERVER_PORT = 10000
BUFFER_SIZE = 4096
WINDOW_SIZE = 3
TIMEOUT = 0.5
PACKET_LOSS_RATE = 0.2
TOTAL_PACKETS = 10

def main():
    sent=0
    ack_received=0
    retransmissions=0
    simulated_losses=0

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(TIMEOUT)
    
    print(f"[CLIENT] {time.strftime('%H:%M:%S')} - {"Client started"}")
    
    base = 0 
    next_seq_num = 0 
    
    while base < TOTAL_PACKETS:
        time.sleep(3)
        while next_seq_num < base + WINDOW_SIZE and next_seq_num < TOTAL_PACKETS:
            packet = f"PKT:{next_seq_num}".encode()
            
            if random.random()<PACKET_LOSS_RATE:
                print(f"Package lost simulation: {next_seq_num}")
                simulated_losses += 1
            else:
                client_socket.sendto(packet, (SERVER_IP, SERVER_PORT))
                print(f"send package:{next_seq_num}")
                sent += 1
            
            next_seq_num += 1
        
        try:
            data,addr = client_socket.recvfrom(BUFFER_SIZE)
            try:
                ackNum= int(data.decode().split(':')[1])
            except (IndexError):
                ackNum = -1
            
            if ackNum >= base:
                print(f"Recived ACK for package: {ackNum}")
                ack_received += 1
                base = ackNum + 1
            else:
                print(f"Recived ACK duplicated: {ackNum}")
        
        except socket.timeout:
            print(f"Timeout! Resend package from {base} to {next_seq_num-1}")
            retransmissions += next_seq_num - base
            next_seq_num = base 
    
    client_socket.sendto("END".encode(), (SERVER_IP, SERVER_PORT))
    print("Finish trasmission")
    
    print("\n--- STATISTICS ---")
    print(f"Package sent: {sent}")
    print(f"ACK recived: {ack_received}")
    print(f"Retrasmissions: {retransmissions}")
    print(f"Simulated losses: {simulated_losses}")
    
    client_socket.close()

main()