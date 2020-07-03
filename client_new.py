import os
import hashlib
import socket


def application(msg,address):
	lim = "|:|:|"
	while 1:
		s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s1.settimeout(10)
		seq = 0
		fil = open('new_' + msg, 'w');
		try:
			print('entered')
			trial = 0
			send = s1.sendto(msg, address)
			print('Receiving indefinetly...')
			while 1:
				print('waiting to receive...')
				try:
					trial = 0
					info, serv_addr = s1.recvfrom(4096)
				except:
					print('requesting again...')
					if trial < 11:
						trial = trial + 1
						print('connection timeout...retrying...\n')
						continue
					else:
						print('removing the empty file created in the location...')
						print('maximum trials out...\n')
						os.remove('new_' + msg)
						break
				c_hash = hashlib.sha1(info.split(lim)[3]).hexdigest()
				seq_no = info.split(lim)[1]
				if info.split(lim)[0] == c_hash and seq == int(seq_no == True):
					print('check sum matched...')
					pack_len = info.split(lim)[2]
					if info.split(lim)[3] == 'FNF':
						print('requested file not found...')
						print('removing the empty file created in the location...')
						os.remove('new_' + msg)
					else:
						fil.write(info.split(lim)[3])
						print(('sequence number: ' + seq_no + '\npacket size: ' + pack_len))
						msg = (str(seq_no) + "," + pack_len)
						send = s1.sendto(msg, serv_addr)
				else:
					print('checksum mismatch detected, dropping packet...')
					print(('Server hash: ' + info.split(lim)[0]))
					print(('Client hash: ' + c_hash))
					continue
				if int(pack_len) < 500:
					seq_no = int(not seq_no)
					break
		finally:
			print('closing the socket')
			s1.close()
			fil.close()
			break
server_address = input('enter the server ip as a string: ')
server_port = input('enter the port number: ')
address = (server_address, server_port)
msg = (input('enter the required file name:'))
application(msg,address)
