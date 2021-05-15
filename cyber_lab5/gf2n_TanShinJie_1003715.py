# 50.042 FCS Lab 5 Modular Arithmetics
# Year 2020

""" 
Tan Shin Jie
1003715
"""

import copy

sbox = [
    0x63,
    0x7C,
    0x77,
    0x7B,
    0xF2,
    0x6B,
    0x6F,
    0xC5,
    0x30,
    0x01,
    0x67,
    0x2B,
    0xFE,
    0xD7,
    0xAB,
    0x76,
    0xCA,
    0x82,
    0xC9,
    0x7D,
    0xFA,
    0x59,
    0x47,
    0xF0,
    0xAD,
    0xD4,
    0xA2,
    0xAF,
    0x9C,
    0xA4,
    0x72,
    0xC0,
    0xB7,
    0xFD,
    0x93,
    0x26,
    0x36,
    0x3F,
    0xF7,
    0xCC,
    0x34,
    0xA5,
    0xE5,
    0xF1,
    0x71,
    0xD8,
    0x31,
    0x15,
    0x04,
    0xC7,
    0x23,
    0xC3,
    0x18,
    0x96,
    0x05,
    0x9A,
    0x07,
    0x12,
    0x80,
    0xE2,
    0xEB,
    0x27,
    0xB2,
    0x75,
    0x09,
    0x83,
    0x2C,
    0x1A,
    0x1B,
    0x6E,
    0x5A,
    0xA0,
    0x52,
    0x3B,
    0xD6,
    0xB3,
    0x29,
    0xE3,
    0x2F,
    0x84,
    0x53,
    0xD1,
    0x00,
    0xED,
    0x20,
    0xFC,
    0xB1,
    0x5B,
    0x6A,
    0xCB,
    0xBE,
    0x39,
    0x4A,
    0x4C,
    0x58,
    0xCF,
    0xD0,
    0xEF,
    0xAA,
    0xFB,
    0x43,
    0x4D,
    0x33,
    0x85,
    0x45,
    0xF9,
    0x02,
    0x7F,
    0x50,
    0x3C,
    0x9F,
    0xA8,
    0x51,
    0xA3,
    0x40,
    0x8F,
    0x92,
    0x9D,
    0x38,
    0xF5,
    0xBC,
    0xB6,
    0xDA,
    0x21,
    0x10,
    0xFF,
    0xF3,
    0xD2,
    0xCD,
    0x0C,
    0x13,
    0xEC,
    0x5F,
    0x97,
    0x44,
    0x17,
    0xC4,
    0xA7,
    0x7E,
    0x3D,
    0x64,
    0x5D,
    0x19,
    0x73,
    0x60,
    0x81,
    0x4F,
    0xDC,
    0x22,
    0x2A,
    0x90,
    0x88,
    0x46,
    0xEE,
    0xB8,
    0x14,
    0xDE,
    0x5E,
    0x0B,
    0xDB,
    0xE0,
    0x32,
    0x3A,
    0x0A,
    0x49,
    0x06,
    0x24,
    0x5C,
    0xC2,
    0xD3,
    0xAC,
    0x62,
    0x91,
    0x95,
    0xE4,
    0x79,
    0xE7,
    0xC8,
    0x37,
    0x6D,
    0x8D,
    0xD5,
    0x4E,
    0xA9,
    0x6C,
    0x56,
    0xF4,
    0xEA,
    0x65,
    0x7A,
    0xAE,
    0x08,
    0xBA,
    0x78,
    0x25,
    0x2E,
    0x1C,
    0xA6,
    0xB4,
    0xC6,
    0xE8,
    0xDD,
    0x74,
    0x1F,
    0x4B,
    0xBD,
    0x8B,
    0x8A,
    0x70,
    0x3E,
    0xB5,
    0x66,
    0x48,
    0x03,
    0xF6,
    0x0E,
    0x61,
    0x35,
    0x57,
    0xB9,
    0x86,
    0xC1,
    0x1D,
    0x9E,
    0xE1,
    0xF8,
    0x98,
    0x11,
    0x69,
    0xD9,
    0x8E,
    0x94,
    0x9B,
    0x1E,
    0x87,
    0xE9,
    0xCE,
    0x55,
    0x28,
    0xDF,
    0x8C,
    0xA1,
    0x89,
    0x0D,
    0xBF,
    0xE6,
    0x42,
    0x68,
    0x41,
    0x99,
    0x2D,
    0x0F,
    0xB0,
    0x54,
    0xBB,
    0x16,
]


class Polynomial2:
    def __init__(self, coeffs):
        self.coeffs = coeffs

    def add(self, p2):
        new_coeffs = [None] * min(len(self.coeffs), len(p2.coeffs))
        for i in range(len(new_coeffs)):
            new_coeffs[i] = self.coeffs[i] ^ p2.coeffs[i]
        if len(self.coeffs) > len(p2.coeffs):
            new_coeffs.extend(self.coeffs[len(new_coeffs) :])
        elif len(self.coeffs) < len(p2.coeffs):
            new_coeffs.extend(p2.coeffs[len(new_coeffs) :])
        return Polynomial2(new_coeffs)

    def sub(self, p2):
        return self.add(p2)

    def mul(self, p2, modp=None):
        partial_polynomials = []
        if modp:
            partial_coeff = [self.coeffs]
            partial_polynomials.append(self)
            for i in range(1, len(p2.coeffs)):
                temp_coeff = [0] + partial_coeff[i - 1]
                msb_index = self.getMSBIndex(temp_coeff)
                temp_coeff = temp_coeff[:msb_index]
                if len(temp_coeff) >= len(modp.coeffs):
                    temp_poly = Polynomial2(temp_coeff).sub(modp)
                    temp_coeff = temp_poly.coeffs
                    msb_index = self.getMSBIndex(temp_coeff)
                    temp_coeff = temp_coeff[:msb_index]
                partial_coeff.append(temp_coeff)
                partial_polynomials.append(Polynomial2(temp_coeff))
            result = Polynomial2([0])
            for i in range(len(p2.coeffs)):
                if p2.coeffs[i]:
                    result = result.add(partial_polynomials[i])
            return result
        else:
            for i in range(len(p2.coeffs)):
                temp_coeff = [0 for i in range(i)] + self.coeffs
                partial_polynomials.append(Polynomial2(temp_coeff))
            result = Polynomial2([0])
            for i in range(len(p2.coeffs)):
                if p2.coeffs[i]:
                    result = result.add(partial_polynomials[i])
            return result

    def getMSBIndex(self, coeff):
        msb_index = len(coeff)
        for j in range(len(coeff) - 1, -1, -1):
            if not coeff[j]:
                msb_index -= 1
            else:
                return msb_index

    def div(self, p2):
        q = Polynomial2([0])
        r = copy.deepcopy(self)
        d = len(p2.coeffs)
        c = p2.coeffs[d - 1]
        if p2.coeffs == [1]:
            return (r, Polynomial2([0]))
        while len(r.coeffs) >= d:
            s_coeff = [0 for i in range(len(r.coeffs) - d)] + [1]
            s_poly = Polynomial2(s_coeff)
            q = q.add(s_poly)
            r = r.sub(s_poly.mul(p2))
            msb_index = self.getMSBIndex(r.coeffs)
            r_coefff = r.coeffs[:msb_index]
            r = Polynomial2(r_coefff)
        return (q, r)

    def __str__(self):
        result = ""
        if 1 not in self.coeffs:
            return "0"
        for i in range(len(self.coeffs)):
            if self.coeffs[i]:
                result = "+x^" + str(i) + result
        result = result.replace("x^0", "1")
        return result[1:]

    def getInt(self):
        decimal = 0
        for i in range(len(self.coeffs)):
            decimal += self.coeffs[i] * (2 ** i)
        return decimal


class GF2N:
    affinemat = [
        [1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1],
    ]

    def __init__(self, x, n=8, ip=Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])):
        self.x = list(int(i) for i in bin(x)[2:])
        self.x.reverse()
        self.n = n
        self.ip = ip

    def add(self, g2):
        return self.getPolynomial2().add(g2.getPolynomial2())
        # return GF2N(self.getPolynomial2().add(g2.getPolynomial2()).getInt())

    def sub(self, g2):
        return self.add(g2)

    def mul(self, g2):
        return self.getPolynomial2().mul(g2.getPolynomial2(), self.ip)
        # return GF2N(self.getPolynomial2().mul(g2.getPolynomial2(), self.ip).getInt())

    def div(self, g2):
        q, r = self.getPolynomial2().div(g2.getPolynomial2())
        return GF2N(q.getInt()), GF2N(r.getInt())

    def getPolynomial2(self):
        return Polynomial2(self.x)

    def __str__(self):
        return self.getPolynomial2().__str__()

    def getInt(self):
        return self.getPolynomial2().getInt()

    def mulInv(self):
        r1 = self.ip
        r2 = self.getPolynomial2()
        t1 = Polynomial2([0])
        t2 = Polynomial2([1])
        if r2.getInt() == 0:
            return GF2N(0)
        while r2.getInt() > 0:
            q, remainder = r1.div(r2)
            r = r1.sub(q.mul(r2))
            r_msb = r.getMSBIndex(r.coeffs)
            r_coeff = r.coeffs[:r_msb]
            r = Polynomial2(r_coeff)
            r1 = r2
            r2 = r

            t = t1.sub(q.mul(t2))
            t1 = t2
            t2 = t
            if r1.getInt() == 1:
                return GF2N(t1.getInt())

    def affineMap(self):
        new_coeffs = []
        matrix = [
            [1, 0, 0, 0, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 1, 1, 1, 1],
        ]
        final_vector = [1, 1, 0, 0, 0, 1, 1, 0]
        padded_coeffs = self.getPolynomial2().coeffs
        if len(padded_coeffs) < len(final_vector):
            for i in range(len(final_vector) - len(padded_coeffs)):
                padded_coeffs.append(0)
        for row_num in range(len(matrix)):
            new_b = 0
            for i in range(len(matrix[row_num])):
                new_b ^= padded_coeffs[i] & matrix[row_num][i]
            new_b ^= final_vector[row_num]
            new_coeffs.append(new_b)
        return Polynomial2(new_coeffs)


# print("\nTest 1")
# print("======")
# print("p1=x^5+x^2+x")
# print("p2=x^3+x^2+1")
# p1 = Polynomial2([0, 1, 1, 0, 0, 1])
# p2 = Polynomial2([1, 0, 1, 1])
# p3 = p1.add(p2)
# print("p3= p1+p2 = ", p3)

# print("\nTest 2")
# print("======")
# print("p4=x^7+x^4+x^3+x^2+x")
# print("modp=x^8+x^7+x^5+x^4+1")
# p4 = Polynomial2([0, 1, 1, 1, 1, 0, 0, 1])
# # modp=Polynomial2([1,1,0,1,1,0,0,0,1]) # default modp
# modp = Polynomial2([1, 0, 0, 0, 1, 1, 0, 1, 1])
# p5 = p1.mul(p4, modp)
# print("p5=p1*p4 mod (modp)=", p5)
# p1 = Polynomial2([1, 1, 1])
# p2 = Polynomial2([1, 1, 1])
# p1.mul(p2)


# print("\nTest 3")
# print("======")
# print("p6=x^12+x^7+x^2")
# print("p7=x^8+x^4+x^3+x+1")
# p6 = Polynomial2([0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
# p7 = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])
# p8q, p8r = p6.div(p7)
# print("q for p6/p7=", p8q)
# print("r for p6/p7=", p8r)

# print("\nTest 4")
# print("======")
# g1 = GF2N(100)
# g2 = GF2N(5)
# print("g1 = ", g1.getPolynomial2())
# print("g2 = ", g2.getPolynomial2())
# g3 = g1.add(g2)
# print("g1+g2 = ", g3.getInt())

# print("\nTest 5")
# print("======")
# ip = Polynomial2([1, 1, 0, 0, 1])
# print("irreducible polynomial", ip)
# g4 = GF2N(0b1101, 4, ip)
# g5 = GF2N(0b110, 4, ip)
# print("g4 = ", g4.getPolynomial2())
# print("g5 = ", g5.getPolynomial2())
# g6 = g4.mul(g5)
# print("g4 x g5 = ", g6)

# print("\nTest 6")
# print("======")
# g7 = GF2N(0b1000010000100, 13, None)
# g8 = GF2N(0b100011011, 13, None)
# print("g7 = ", g7.getPolynomial2())
# print("g8 = ", g8.getPolynomial2())
# q, r = g7.div(g8)
# print("g7/g8 =")
# print("q = ", q.getPolynomial2())
# print("r = ", r.getPolynomial2())

# print("\nTest 7")
# print("======")
# ip = Polynomial2([1, 1, 0, 0, 1])
# print("irreducible polynomial", ip)
# g9 = GF2N(0b101, 4, ip)
# print("g9 = ", g9.getPolynomial2())
# print("inverse of g9 =", g9.mulInv().getPolynomial2())

# print("\nTest 8")
# print("======")
# ip = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])
# print("irreducible polynomial", ip)
# g10 = GF2N(0xC2, 8, ip)
# print("g10 = 0xc2")
# g11 = g10.mulInv()
# print("inverse of g10 = g11 =", g11, hex(g11.getInt()))
# g12 = g11.affineMap()
# print("affine map of g11 =", hex(g12.getInt()))

# print("\nGenerating elements for GF(2^4)...")
# ip = Polynomial2([1, 0, 0, 1, 1])
# gf2_power4_elements = []
# for i in range(2 ** 4):
#     gf2_power4_elements.append(GF2N(i, 4, ip))
# print("done")
# for i in gf2_power4_elements:
#     print(i)
# print("\nGenerating Addition Table for GF(2^4)")
# for i in range(2 ** 4):
#     print(
#         "\n=== Adding",
#         gf2_power4_elements[i].getPolynomial2(),
#         "to every elements in the field ===",
#     )
#     for j in range(2 ** 4):
#         p1 = gf2_power4_elements[i].getPolynomial2()
#         p2 = gf2_power4_elements[j].getPolynomial2()
#         p1addp2 = gf2_power4_elements[i].add(gf2_power4_elements[j])
#         result = "{} + {} = {}".format(p1, p2, p1addp2)
#         print(result)
# print("\nGenerating Multiplication Table for GF(2^4) with IP", ip)
# for i in range(2 ** 4):
# print(
#     "\n=== Multiplying",
#     gf2_power4_elements[i].getPolynomial2(),
#     "to every elements in the field ===",
# )
# for j in range(2 ** 4):
#     p1 = gf2_power4_elements[i].getPolynomial2()
#     p2 = gf2_power4_elements[j].getPolynomial2()
#     p1mulp2 = gf2_power4_elements[i].mul(gf2_power4_elements[j])
#     result = "{} * {} = {}".format(p1, p2, p1mulp2)
#     print(result)

# print("\nGenerating AES S-Box Table with ip", ip)
# ip = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])
# hex_string = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "a", "b", "c", "d", "e", "f"]
# generated_sbox = []
# for x in hex_string:
#     for y in hex_string:
#         xy = str(x) + str(y)
#         g = GF2N(int(xy, 16), 8)
#         generated_sbox.append(g.mulInv().affineMap().getInt())

# for i in range(len(generated_sbox)):
#     assert generated_sbox[i] == sbox[i]
