from wtforms import Form, IntegerField, StringField
from wtforms.validators import Required, Length

from connectfour.model import DEFAULT_ROWS, DEFAULT_COLUMNS, DEFAULT_TO_WIN


class NewGameForm(Form):
    num_rows = IntegerField(u'Number of rows', default=DEFAULT_ROWS)
    num_columns = IntegerField(u'Number of columns', default=DEFAULT_COLUMNS)
    num_to_win = IntegerField(u'Number to win', default=DEFAULT_TO_WIN)
    username = StringField(u'Your username',
                           [Required(), Length(min=4, max=25)])


class ExistingGameForm(Form):
    pk = StringField(u'Game ID')
    username = StringField(u'Your username',
                           [Required(), Length(min=4, max=25)])
