from core.point import Point

ELLIPTIC_CURVES = {
    'Custom': {
        'p': 820692272049904754268558404823550666902242581027,
        'a': 789527267482250023533321246187221928470553233573,
        'b': 631385804378468242810549727762799065593611977755,
        'g': Point(567897938643847309026511906264475250815917655751,
          389820891852823519475027830793533803851547699598)
    },
    'nistP192': {
        'p': 0xfffffffffffffffffffffffffffffffeffffffffffffffff,
        'a': 0xfffffffffffffffffffffffffffffffefffffffffffffffc,
        'b': 0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1,
        'g': Point(0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012,
          0x07192b95ffc8da78631011ed6b24cdd573f977a11e794811)
    },
    'nistP256': {
        'p': 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff,
        'a': 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc,
        'b': 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b,
        'g': Point(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
          0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
    },
    'brainpoolP192t1': {
        'p': 0xc302f41d932a36cda7a3463093d18db78fce476de1a86297,
        'a': 0xc302f41d932a36cda7a3463093d18db78fce476de1a86294,
        'b': 0x13d56ffaec78681e68f9deb43b35bec2fb68542e27897b79,
        'g': Point(0x3ae9e58c82f63c30282e1fe7bbf43fa72c446af6f4618129,
          0x97e2c5667c2223a902ab5ca449d0084b7e5b3de7ccc01c9)
    },
    'prime192v3': {
        'p': 0xfffffffffffffffffffffffffffffffeffffffffffffffff,
        'a': 0xfffffffffffffffffffffffffffffffefffffffffffffffc,
        'b': 0x22123dc2395a05caa7423daeccc94760a7d462256bd56916,
        'g': Point(0x7d29778100c65a1da1783716588dce2b8b4aee8e228f1896,
          0x38a90f22637337334b49dcb66a6dc8f9978aca7648a943b0)
    },
    'prime256v1': {
        'p': 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff,
        'a': 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc,
        'b': 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b,
        'g': Point(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
          0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
    }
}