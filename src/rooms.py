from main import SCREEN_WIDTH
from main import SCREEN_HEIGHT
from main import PADDING
from main import CENTER_W
from main import CENTER_H

empty_room = [[0 + PADDING, 0 + PADDING, SCREEN_WIDTH - PADDING, 0 + PADDING],
                                    [SCREEN_WIDTH - PADDING, 0 + PADDING, SCREEN_WIDTH - PADDING,
                                     SCREEN_HEIGHT - PADDING],
                                    [SCREEN_WIDTH - PADDING, SCREEN_HEIGHT - PADDING, 0 + PADDING,
                                     SCREEN_HEIGHT - PADDING],
                                    [0 + PADDING, SCREEN_HEIGHT - PADDING, 0 + PADDING, 0 + PADDING]
                                    ]

room_1 = [[0 + PADDING, 0 + PADDING, SCREEN_WIDTH - PADDING, 0 + PADDING],
                                    [SCREEN_WIDTH - PADDING, 0 + PADDING, SCREEN_WIDTH - PADDING,
                                     SCREEN_HEIGHT - PADDING],
                                    [SCREEN_WIDTH - PADDING, SCREEN_HEIGHT - PADDING, 0 + PADDING,
                                     SCREEN_HEIGHT - PADDING],
                                    [0 + PADDING, SCREEN_HEIGHT - PADDING, 0 + PADDING, 0 + PADDING],
                                    [CENTER_W - 100, CENTER_H - 100, CENTER_W + 100, CENTER_H - 100],
                                    [CENTER_W + 100, CENTER_H - 100, CENTER_W + 100, CENTER_H + 100],
                                    [CENTER_W + 100, CENTER_H + 100, CENTER_W - 100, CENTER_H + 100],
                                    [CENTER_W - 100, CENTER_H + 100, CENTER_W - 100, CENTER_H - 100]]
