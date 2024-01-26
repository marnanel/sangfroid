# Examples

Suppose you have this canvas, [colours.sif](examples/colours.sif):

![Basic colours.sif](colours.png)

Using `Animation.find_all()`, you can set the word "blue" to be
magenta anywhere it occurs:

```{python}
import sangfroid

def main():
    sif = sangfroid.Animation('colours.sif')

    for item in sif.find_all(text='blue'):
        item['color'] = '#FF00FF'

    sif.save(filename='stroop.sif')

if __name__=='__main__':
    main()
```
![Stroop result](stroop.png)
(Code: [stroop.py](examples/stroop.py))

Alternatively, we can filter *all* text in the canvas through a
rather dubious translation into French:

```{python}
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
```

![French result](french.png)
(Code: [french.py](examples/french.py))

Next, let's look at how to add keyframes... (to be continued)
