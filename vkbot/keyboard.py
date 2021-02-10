import json

from enum import Enum

# NOTE: Keyboard does not support inline mode
#
# Spied on here:
# https://github.com/python273/vk_api/blob/master/vk_api/keyboard.py
# Thank you, guys :)


MAX_BUTTONS_ON_LINE = 5
MAX_DEFAULT_LINES = 10
MAX_INLINE_LINES = 6


class VkKeyboardColor(Enum):
    """ Возможные цвета кнопок """

    #: Синяя
    PRIMARY = 'primary'

    #: Белая
    SECONDARY = 'secondary'

    #: Красная
    NEGATIVE = 'negative'

    #: Зелёная
    POSITIVE = 'positive'


class VkKeyboardButton(Enum):
    """ Возможные типы кнопки """

    #: Кнопка с текстом
    TEXT = "text"


class VkKeyboard(object):
    """ Класс для создания клавиатуры для бота (https://vk.com/dev/bots_docs_3)
    :param one_time: Если True, клавиатура исчезнет после нажатия на кнопку
    :type one_time: bool
    """

    __slots__ = ('one_time', 'lines', 'keyboard', 'inline')

    def __init__(self, one_time=False):
        self.one_time = one_time
        self.lines = [[]]

        self.keyboard = {
            'one_time': self.one_time,
            'inline': False,
            'buttons': self.lines
        }

    def get_keyboard(self):
        """ Получить json клавиатуры """
        return json.dumps(self.keyboard)

    @classmethod
    def get_empty_keyboard(cls):
        """ Получить json пустой клавиатуры.
        Если отправить пустую клавиатуру, текущая у пользователя исчезнет.
        """
        keyboard = cls()
        keyboard.keyboard['buttons'] = []
        return keyboard.get_keyboard()

    def add_button(self, label, color=VkKeyboardColor.SECONDARY, payload=None):
        """ Добавить кнопку с текстом.
            Максимальное количество кнопок на строке - MAX_BUTTONS_ON_LINE
        :param label: Надпись на кнопке и текст, отправляющийся при её нажатии.
        :type label: str
        :param color: цвет кнопки.
        :type color: VkKeyboardColor or str
        :param payload: Параметр для callback api
        :type payload: str or list or dict
        """

        current_line = self.lines[-1]

        if len(current_line) >= MAX_BUTTONS_ON_LINE:
            raise ValueError(f'Max {MAX_BUTTONS_ON_LINE} buttons on a line')

        color_value = color

        if isinstance(color, VkKeyboardColor):
            color_value = color_value.value

        if payload is not None:
            payload = json.dumps(payload)

        button_type = VkKeyboardButton.TEXT.value

        current_line.append({
            'color': color_value,
            'action': {
                'type': button_type,
                'payload': payload,
                'label': label,
            }
        })


def get_command_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Help', color=VkKeyboardColor.SECONDARY, payload='/help')
    keyboard.add_button('Best players', color=VkKeyboardColor.SECONDARY, payload='/top')
    keyboard.add_button(
        'Start the game', color=VkKeyboardColor.NEGATIVE, payload='/new'
    )
    return keyboard
