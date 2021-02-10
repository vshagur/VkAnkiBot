import json


class VkKeyboard(object):
    MAX_BUTTONS = 10

    def __init__(self, one_time=True):
        self.one_time = one_time
        self.buttons = []

        self.keyboard = {
            'one_time': self.one_time,
            'buttons': self.buttons
        }

    def get_keyboard(self):
        return json.dumps(self.keyboard)

    def add_text_button(self, color, label, payload):
        if len(self.buttons) >= self.MAX_BUTTONS:
            raise ValueError(
                f'The number of buttons should not exceed {self.MAX_BUTTONS}.'
            )

        self.buttons.append([{
            'color': color,
            'action': {
                'type': 'text',
                'payload': payload,
                'label': label,
            }
        }, ])



