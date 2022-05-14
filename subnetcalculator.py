#Following lists and dictionaries will be used to classify subnet masks and convert integers into binary strings
class_A = ['255.0.0.0', '255.128.0.0', '255.192.0.0', '255.224.0.0', '255.240.0.0', '255.248.0.0', '255.252.0.0', '255.254.0.0']
class_B = ['255.255.0.0', '255.255.128.0', '255.255.192.0', '255.255.224.0', '255.255.240.0', '255.255.248.0', '255.255.252.0', '255.255.254.0']
class_C = ['255.255.255.0', '255.255.255.128', '255.255.255.192', '255.255.255.224', '255.255.255.240', '255.255.255.248', '255.255.255.252']
cidr = {'A': [8, 9, 10, 11, 12, 13, 14, 15], 'B': [16, 17, 18, 19, 20, 21, 22, 23], 'C': [24, 25, 26, 27, 28, 29, 30]}
byteList = [128, 64, 32, 16, 8, 4, 2, 1]


#Following variables are preventing false inputs into the IP address
alphabet = 'abcdefghijklmnopqrstuvwxyzåäö'
negativeValue = '-'
incorrectOctet = False
reason = ''
while True:
    ipAdd = input('Enter an IP address: ')

    #For loop is removing dots from string and defines the octets
    ipList = []
    dotRm = ''
    for i in ipAdd:
        if i.isdigit():
            dotRm += i
            
        else:
            ipList.append(dotRm)
            dotRm = ''

        if i.lower() in alphabet:
            incorrectOctet = True
            reason = 'letter'
        if i in negativeValue:
            incorrectOctet = True
            reason = 'negative value'

    ipList.append(dotRm)

    if incorrectOctet == True:
        print(f'Found {reason} in IP address!')

    else:    
        for i in ipList:
            i = int(i)
            if i < 0 or i > 255:
                incorrectOctet = True

        #If statement is checking that there are four octets in the IP and that the values are in an IP range
        if len(ipList) == 4 and incorrectOctet == False:
            break
        else:
            print('Octet value must be between 0-255 and 4 octets!')


while True:
    subnet = input('Enter a Subnet Mask: ')

    #Comparing and validating the subnet mask entered by the user. Afterwards it is defining the key, class, and which octet is going to be modified later on
    if subnet in class_A:
        print('\nSubnet Mask is a Network Class A')
        key = 'A'
        subnetClass = class_A
        classIndex = 1
        break
    elif subnet in class_B:
        print('\nSubnet Mask is a Network Class B')
        key = 'B'
        subnetClass = class_B
        classIndex = 2
        break
    elif subnet in class_C:
        print('\nSubnet Mask is a Network Class C') 
        key = 'C'
        subnetClass = class_C
        classIndex = 3
        break
    else:
        print('Invalid Subnet Mask!')


#Collecting the correct CIDR from cidr dictionary
position = -1
for i in subnetClass:
    position += 1
    if i in subnet:
        subnetCidr = cidr[key][position]
        print(f'CIDR: /{subnetCidr}')


#Removing dots from subnet mask
subnetList = []
dotRemover = ''
for i in subnet:
    if i.isdigit():
        dotRemover += i
    else:
        subnetList.append(int(dotRemover))
        dotRemover = ''

subnetList.append(int(dotRemover))


#Converts octets into binary strings and appends in maskInBinaryList
maskInbinaryList = []
for octet in subnetList:
    maskInbinary = ''
    for bit in byteList:
        if octet - bit >= 0:
            octet -= bit
            maskInbinary += '1'
        
        else:
            maskInbinary += '0'

    maskInbinaryList.append(maskInbinary)


#Calculating available subnets and rewriting the integer in subnetsAvailable
if maskInbinaryList[classIndex] == '00000000':
    print(f'Subnets available in /{subnetCidr}: 1')
else:
    currentOctet = maskInbinaryList[classIndex]
    for i in range(8):
        if currentOctet[i] == '1':
            subnetsAvailable = 256 // byteList[i]
    
    print(f'Subnets available: {subnetsAvailable}')


#Calculating available host addresses in the subnet
hostBits = 32 - subnetCidr
availableHosts = (2 ** hostBits) - 2
print(f'Available host addresses: {availableHosts}')


#For loop is generating a dictionary containing all network addresses by generating the CIDR key and adding the values as integers
netAddressDic = {}
for y in range(8, 31):
    netAddresses = []
    if y == 8 or y == 16 or y == 24:
        x = 256  
    if y == 9 or y == 17 or y == 25:
        x = 128
    if y == 10 or y == 18 or y == 26:
        x = 64
    if y == 11 or y == 19 or y == 27:
        x = 32
    if y == 12 or y == 20 or y == 28:
        x = 16
    if y == 13 or y == 21 or y == 29:
        x = 8
    if y == 14 or y == 22 or y == 30:
        x = 4
    if y == 15 or y == 23:
        x = 2

    for i in range(0, 256, x):
        netAddresses.append(i)

    netAddressDic[y] = netAddresses


#Comparing if the picked octet value is higher or lower than the current i (network address in netAddressDic), if higher, netAddOctet inherit the value of i
pickedOctet = ipList[classIndex]
for i in netAddressDic[subnetCidr]:
    if int(pickedOctet) > i:
        netAddOctet = i

#Rewriting the IP address to the network address
ipList[classIndex] = str(netAddOctet)
if classIndex == 1:
    ipList[classIndex+1] = '0'
    ipList[classIndex+2] = '0'
if classIndex == 2:
    ipList[classIndex+1] = '0'

#Making the network address as a f-string
a1 = ipList[0]
a2 = ipList[1]
a3 = ipList[2]
a4 = ipList[3]
networkAddress = f'{a1}.{a2}.{a3}.{a4}'

#Converts network address into a binary list
networkAddressBinary = []
for octet in ipList:
    octet = int(octet)
    currentByte = ''
    for bit in byteList:
        if octet - bit >= 0:
            octet -= bit
            currentByte += '1'
        else:
            currentByte += '0'

    networkAddressBinary.append(currentByte)


#Creates a binary broadcast address
broadcastAddressBinary = []
for octet in range(4):
    currentMaskOctet = maskInbinaryList[octet]
    currentNetworkOctet = networkAddressBinary[octet]
    broadcastBinary = ''
    for i in range(8):
        if currentMaskOctet[i] == '1':
            broadcastBinary += currentNetworkOctet[i]
        else:
            broadcastBinary += '1'
    
    broadcastAddressBinary.append(broadcastBinary)


#Writing the broadcast octets as integers instead of binaries
broadcast1 = 0
broadcast2 = 0
broadcast3 = 0
broadcast4 = 0
for octet in range(4):
    currentBroadcastOctet = broadcastAddressBinary[octet]
    for i in range(8):
        if octet == 0:
            if currentBroadcastOctet[i] == '1':
                broadcast1 += byteList[i]

        if octet == 1:
            if currentBroadcastOctet[i] == '1':
                broadcast2 += byteList[i]

        if octet == 2:
            if currentBroadcastOctet[i] == '1':
                broadcast3 += byteList[i]
        
        if octet == 3:
            if currentBroadcastOctet[i] == '1':
                broadcast4 += byteList[i]

    b1 = str(broadcast1)
    b2 = str(broadcast2)
    b3 = str(broadcast3)
    b4 = str(broadcast4)
    broadcastAddress = f'{b1}.{b2}.{b3}.{b4}'

print(f'Network Address: {networkAddress}')
print(f'Broadcast Address: {broadcastAddress}')
