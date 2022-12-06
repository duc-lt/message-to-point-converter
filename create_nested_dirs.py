import os


def main():
    plain = """National Institute of Technology, Manipur, 795001 (English)

राष्ट्रीय प्रौद्योगिकी संस्थान, मणिपुर, ७९५००१ (Hindi)

প্রযু্তি ন্যাশনাল ইনস্টিটিউট, মণিপুর, ৭৯৫০০১ (Bengali)

தேசிய தொழில்நுட்பக்‌ கழகம்‌, மணிப்பூர்‌, ௭௯௫௦௦௧ (Tamil)

技術総合研究所，マニプール, 七九五零零一 (Japanese)

技術研究院，曼尼普爾邦, 柒玖伍零零壹  (Chinese)
"""
    root = os.getcwd()
    new_dir = os.path.join(root, 'nested')
    os.mkdir(new_dir)
    for i in range(5):
        os.chdir(new_dir)
        os.mkdir(f'dir_{i}')
        with open(f'file_{i}.txt', 'w') as test:
            test.write(plain*1000)
        test.close()
        current = os.path.join(new_dir, f'dir_{i}')
        os.chdir(current)
        for j in range(5):
            os.mkdir(f'dir_{j}')
            with open(f'file_{j}.txt', 'w') as test:
                test.write(plain)
            test.close()


if __name__ == '__main__':
    main()