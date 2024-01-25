import sangfroid

TRANSLATION = {
        'blue': 'bleu',
        'red':  'rouge',
        }

def main():
    sif = sangfroid.Animation('colours.sif')

    for item in sif.find_all('text'):
        translation = TRANSLATION.get(
                str(item['text']),
                "je ne sais pas quoi")
        item['text'] = translation

    sif.save(filename='french.sif')

if __name__=='__main__':
    main()
