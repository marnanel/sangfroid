from bywords.adjust import adjust
from test import *
import pysrt
import sangfroid

SRT_FILENAME = 'test/bywords/sing-like-a-girl.srt'
SIF_FILENAME = 'test/bywords/sing-like-a-girl.sif'

STATE_INITIAL = {''}

STATE_WORDS = {
        '',
        'HOW',
        ' can can I can I sing can I sing like can I sing like a',
        ' GIRL?',
        ' and',
        ' not not be',
        ' stigmatised',
        ' by by the by the rest',
        ' of of the of the world?',
        }

STATE_LETTERS = {
        '',
        'H HO HOW',
        (
            ' c ca can can I can I s can I si can I sin '
            'can I sing can I sing l can I sing li can '
            'I sing lik can I sing like can I sing like a'
            ),
        ' G GI GIR GIRL GIRL?',
        ' a an and',
        ' n no not not b not be',
        (
            ' s st sti stig stigm stigma stigmat stigmati stigmatis '
            'stigmatise stigmatised'
            ),
        (
            ' b by by t by th by the by the r by the re '
            'by the res by the rest'
            ),
        (
            ' o of of t of th of the of the w of the wo '
            'of the wor of the worl of the world of the world?'
            ),
        }

def test_bywords_adjust_by_word():

    for letter_at_a_time, expected in [
            (False, STATE_WORDS),
            (True,  STATE_LETTERS),
            ]:

        srt = pysrt.open(SRT_FILENAME)
        animation = sangfroid.Animation(SIF_FILENAME)

        def text_waypoints():
            return set([
                ' '.join([str(waypoint.value)
                          for waypoint in text_layer.text.timeline])
                for text_layer in animation.find_all(type='text')
                ])

        assert text_waypoints()==STATE_INITIAL

        adjust(srt, animation,
               letter_at_a_time = letter_at_a_time,
               )

        assert text_waypoints()==expected, (
                f'letter at a time? {letter_at_a_time}'
                )
