import pandas as pd
import nltk


class Encryption:

    def __init__(self):
        self._mostFreqWord = ' '

    def Decrypt(self, byte, amount):
        mask = 2 ** amount - 1
        lowshift = byte >> (8 - amount)
        highbyte = byte << amount & 255
        lowbyte = lowshift & mask
        self._decrypted = highbyte + lowbyte
        return self._decrypted

    def FileDecrypt(self, filename, amount):
        with open(filename, 'rb') as file:
            read = bytearray(file.read())

        processed_data = bytearray()
        for byte in read:
            decryptedByte = self.Decrypt(byte, amount)
            processed_data.append(decryptedByte)


        freqD = nltk.FreqDist(processed_data)
        print("Most Common", freqD.most_common(1)[0][0])

        if freqD.most_common(1)[0][0] == self._mostFreqWord:
            print("Correct rotation:", amount)
            print(processed_data)
            with open("Decrypted.txt", 'wb') as output:
                output.write(processed_data)

        print()    
    def ReadFrequency(self, filename):

        charList = list()
        freqList = list()

        with open(filename, 'r') as file:
            lines = file.readlines()

            for line in lines:
                charList.append(line[12:13])
                freqList.append(int(line[30:34].rstrip().lstrip()))

        freqPD = pd.DataFrame(list(zip(charList, freqList)), columns=['word', 'freq'])

        maxPD = freqPD[['word', 'freq']][freqPD.freq == freqPD['freq'].max()]

        self._mostFreqWord = ord(maxPD.iloc[0]['word'])

        print(25 * '*')
        print("Max Word - Exercises/ExerciseAI/Frequencies.txt:", self._mostFreqWord, bin(self._mostFreqWord), "'" + chr(self._mostFreqWord) + "'")

    def Encrypt(self, byte, amount):
        mask = 2 ** amount - 1
        print("Mask", mask)
        print("Bin Mask", bin(mask))
        lowbyte = byte & mask
        
        print("lowbyte", lowbyte)
        print("lowbyte bin", bin(lowbyte))
        highshift = byte >> amount
        
        print("highshift", highshift)
        lowshift = lowbyte << (8 - amount)
        print("lowshift", lowshift)
        
        wholebyte = lowshift + highshift
        return wholebyte


myEncrypt = Encryption()

myEncrypt.ReadFrequency("Exercises/ExerciseAI/Frequencies.txt")
for i in range(1,8):
    myEncrypt.FileDecrypt("Exercises/ExerciseAI/Encrypted.bin", i)