import sys
sys.path.append('.')

import unittest
import numpy as np
import time
from vpt.sources.video_file_source import VideoFileSource
from vpt.processors.gaze_detector import GazeDetector
from vpt.processors.gaze_engagement_estimator import GazeEngagementEstimator
from vpt.sinks.video_display import VideoDisplay

print(sys.path)

class TestGazeDetector(unittest.TestCase):

    def test_gazes(self):
        video_source = VideoFileSource('vpt/tests/gazes/p01.mp4')
        gaze_detector = GazeDetector(video_source)
        gaze_estimator = GazeEngagementEstimator(gaze_detector, 0.6)

        stat = []
        #gaze_detector.get_data_stream().subscribe(lambda verdict: print(np.linalg.norm(verdict)))
        gaze_estimator.get_data_stream().subscribe(lambda verdict: stat.append(verdict))

        #video_display = VideoDisplay(video_source, duration=5)

        video_source.start()

        #video_display.run()
        video_source.wait()

        percentage = 100.0 * np.count_nonzero(stat) / len(stat)
        print('Gaze detected for {}% of time'.format(percentage))

        self.assertGreater(percentage, 95.0, 'expected gaze to be detected most of the time')


if __name__ == '__main__':
    unittest.main()
