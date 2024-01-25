import sangfroid

def main():
    sif = sangfroid.Animation('colours.sif')

    for item in sif.find_all(text='blue'):
        item['color'] = '#FF00FF'

    sif.save(filename='stroop.sif')

if __name__=='__main__':
    main()
