import conn
from packet_data import packets
import re

def parse_num(strs):
    pattern = r'\d+'
    return re.search(pattern, strs).group()

def check_packet_timeout(pending_packets, tick, timeout):
    resend_packets = []
    for key in pending_packets.keys():
        if tick - pending_packets[key] > timeout:
            resend_packets.append(key)
    for key in resend_packets:
        del pending_packets[key]

    return resend_packets

if __name__=='__main__':
    pconn = conn.PacketLossConnection(min_RTT=1, max_RTT=10, packet_loss_prob=0.1)
    ack_packets = set()
    send_idx = 0
    pending_packets = {}
    resend_packets = []

    while len(ack_packets) < len(packets):
        # print connection state
        print(pconn)

        # send one new packet per tick (while there are packets to send)
        if send_idx < len(packets) and len(resend_packets) == 0:
            pconn.send(packets[send_idx])
            pending_packets[parse_num(packets[send_idx])] = pconn.get_time()
            send_idx += 1
        elif len(resend_packets) > 0:
            idx = int(resend_packets[0]) - 1
            pconn.send(packets[idx])
            pending_packets[parse_num(packets[idx])] = pconn.get_time()
            del resend_packets[0]
        
        print(pending_packets)

        # get the acks
        acks = pconn.get_acks()
        for ack in acks:
            ack_packets.add(ack)
            del pending_packets[parse_num(ack)]

        # print the acks
        if len(acks) > 0:
            print("ACKs")
            for ack in acks:
                print("- " + ack)

        resend_packets = check_packet_timeout(pending_packets, pconn.get_time(), pconn.get_RTT())
        print(resend_packets)
        print()

        print()

        # tick simulates one unit of time passing
        pconn.tick()

    # TODO: implement this!
    # 1. need to track when packets are sent (use conn.get_time() to get the current tick)
    # 2. need to estimate the timeout. Think about what extra parameters you will need here.
    # 3. what do you need to do to handle timeouts?
