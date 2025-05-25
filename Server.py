import socket
import time

PORT = 10000
HOSTADDR='localhost'
BUFFER_SIZE=4096

def main():
    packageRecived= 0
    ackSent= 0
    packageOutOfOrder= 0

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOSTADDR, PORT))
    
    print(f"[SERVER] {time.strftime('%H:%M:%S')} - {"Server Go-Back-N in ascolto su porta 10000"}")
    
    expectedPackageNumber = 0
    
    while True:
        time.sleep(3)
        data, addr = server_socket.recvfrom(BUFFER_SIZE)
        
        print(f"Data recived from address {addr[0]}:{addr[1]}")
        
        dataDecoded = data.decode()
        try:
            packageNumber = int(dataDecoded.split(':')[1])
        except (IndexError):
            packageNumber = -1
        
        if dataDecoded == "END":
            print("Ending package recived")
            break
        
        packageRecived+=1
        
        if packageNumber == expectedPackageNumber:
            print(f"Correct package recived: {packageNumber}")
            ack = f"ACK:{packageNumber}".encode()
            server_socket.sendto(ack, addr)
            print(f"Send ACK:{packageNumber}")
            ackSent+=1
            expectedPackageNumber += 1
        else:
            print(f"Recive package: {packageNumber} instead of {expectedPackageNumber}")
            packageOutOfOrder+=1

            if expectedPackageNumber > 0:
                ack = f"ACK:{expectedPackageNumber-1}".encode()
                server_socket.sendto(ack, addr)
                print(f"Resend ACK:{expectedPackageNumber - 1}")
    
    print("\n--- STATISTICS ---")
    print(f"Package recived: {packageRecived}")
    print(f"ACK send: {ackSent}")
    print(f"Package out of order: {packageOutOfOrder}")
    
    server_socket.close()

main()