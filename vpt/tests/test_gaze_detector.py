import sys
import unittest

import numpy as np

from vpt.sources import MP4VideoSource
from vpt.processors.gaze_detector import GazeDetector
from vpt.processors.gaze_engagement_estimator import GazeEngagementEstimator

# If you know better way than using this sys.path thingy, tell me
#
# This is needed so that the vpt module would be recognized when
# running this file with `$ python path/to/test.py`
# from the root of the repository
sys.path.append('.')


class TestGazeDetector(unittest.TestCase):
    filename: str
    want: bool

    def test_gaze(self):
        video_source = MP4VideoSource(self.filename)
        gaze_detector = GazeDetector(video_source)
        gaze_estimator = GazeEngagementEstimator(gaze_detector, 0.6)

        stat = []
        gaze_estimator.output.subscribe(stat.append)
        # gaze_detector.output.subscribe(lambda verdict: print(np.linalg.norm(verdict)))
        # video_display = VideoDisplay(video_source, duration=5)

        video_source.start()
        # video_display.run()
        # video_source.wait()

        percentage = 100.0 * np.count_nonzero(stat) / len(stat)
        print('\n{}\t{}%\t'.format(self.filename, percentage), end='')
        sys.stdout.flush()

        if self.want:
            self.assertGreater(percentage, 75, 'expected gaze to be detected most of the time')
        else:
            self.assertLess(percentage, 25, 'expected no gaze to be detected most of the time')


def suite():
    tests = [
        ('vpt/tests/gazes/p01.mp4', True),
        ('vpt/tests/gazes/p02.mp4', True),
        ('vpt/tests/gazes/p03.mp4', True),
        ('vpt/tests/gazes/p04.mp4', True),
        ('vpt/tests/gazes/p05.mp4', True),
        ('vpt/tests/gazes/p06.mp4', True),
        ('vpt/tests/gazes/p07.mp4', True),
        ('vpt/tests/gazes/f01.mp4', False),
        ('vpt/tests/gazes/f02.mp4', False),
        ('vpt/tests/gazes/f03.mp4', False),
    ]

    suite = unittest.TestSuite()

    for test in tests:
        test_case = TestGazeDetector('test_gaze')
        test_case.filename, test_case.want = test[0], test[1]

        suite.addTest(test_case)

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
