class ConflictFree:
    dna = ""
    binary = ""
    x = ""
    y = ""

    def __init__(self, binary, dna):
        self.dna = dna
        self.binary = binary
        self.x = "CG"
        self.y = "AT"

    def getDNAComplement(self, string):
        res = ""
        for i in range(len(string)):
            if string[i] == 'A':
                res = res + "T"
            elif string[i] == 'C':
                res = res + "G"
            elif string[i] == 'G':
                res = res + "C"
            elif string[i] == 'T':
                res = res + "A"
        return res

    def encode(self):
        for i in range(len(self.binary)):
            if i == 0:
                if self.binary[0] == '0':
                    self.dna = self.dna + self.x
                else:
                    self.dna = self.dna + self.y
            prev_block = ""
            for j in reversed(range(1, 3)):
                prev_block = prev_block + self.dna[len(self.dna) - j]

            self.dna = self.dna + self.forwardMapping(self.binary[i], prev_block)

    def forwardMapping(self, binary, prev_block):
        mapping = {}
        mapping[('0', self.x)] = self.y
        mapping[('1', self.x)] = self.getDNAComplement(self.y)
        mapping[('0', self.getDNAComplement(self.x))] = self.getDNAComplement(self.y)
        mapping[('1', self.getDNAComplement(self.x))] = self.y
        mapping[('0', self.y)] = self.getDNAComplement(self.x)
        mapping[('1', self.y)] = self.x
        mapping[('0', self.getDNAComplement(self.y))] = self.x
        mapping[('1', self.getDNAComplement(self.y))] = self.getDNAComplement(self.x)
        return mapping[(binary, prev_block)]

    def backwardMapping(self, curr_block, prev_block):
        mapping = {}
        mapping[(self.x, self.getDNAComplement(self.y))] = 0
        mapping[(self.x, self.y)] = 1
        mapping[(self.getDNAComplement(self.x), self.y)] = 0
        mapping[(self.getDNAComplement(self.x), self.getDNAComplement(self.y))] = 1
        mapping[(self.getDNAComplement(self.y), self.x)] = 1
        mapping[(self.getDNAComplement(self.y), self.getDNAComplement(self.x))] = 0
        mapping[(self.y, self.x)] = 0
        mapping[(self.y, self.getDNAComplement(self.x))] = 1
        return mapping[(curr_block, prev_block)]

    def decode(self):
        var = 0
        binary = ""
        first_block = str(self.dna[0]) + str(self.dna[1])
        if first_block == self.x:
            var = 0
        else:
            var = 1

        # binary = binary + str(var)
        # print(binary)
        ind = 0
        for j in range(2, len(self.dna), 2):
            curr_block = str(self.dna[j]) + str(self.dna[j + 1])
            prev_block = str(self.dna[ind]) + str(self.dna[ind + 1])
            ind = j
            #print(str(self.backwardMapping(curr_block, prev_block)))
            binary = binary + str(self.backwardMapping(curr_block, prev_block))
        self.binary = binary

    def getBinary(self):
        return self.binary

    def getDNA(self):
        return self.dna
