from extensions.segmentation import Segmentation

if __name__ == "__main__":
    for i in range(5):
        seg = Segmentation()

    while True:
        query = input('Please type in fund name, type in "q" to quit\n')
        if query == 'q':
            break
        candidates = seg.match(query)
        print(f'candidates: {candidates}')
