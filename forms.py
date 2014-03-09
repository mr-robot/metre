__author__ = 'beast'

from datetime import timedelta
import datetime
import time

from wtforms.fields import TextField, SelectField
from wtforms.widgets import Input, HTMLString, html_params
from wtforms.ext.csrf.session import SessionSecureForm
from wtforms import fields as wtf_fields
from wtforms import widgets, validators
from constants.timezone import named



timezones = named
#abbreviations

class TimeField(wtf_fields.Field):
    """A text field which stores a `time.time` matching a format."""
    widget = widgets.TextInput()

    def __init__(self, label=None, validators=None,
                 format='%H:%M:%S', **kwargs):
        super(TimeField, self).__init__(label, validators, **kwargs)
        self.format = format

    def _value(self):
        if self.raw_data:
            return u' '.join(self.raw_data)
        else:
            return self.data and self.data.strftime(self.format) or u''

    def process_formdata(self, valuelist):
        if valuelist:
            time_str = u' '.join(valuelist)
            try:
                timetuple = time.strptime(time_str, self.format)
                self.data = datetime.time(*timetuple[3:6])
            except ValueError:
                self.data = None
                raise


class DatePickerWidget(widgets.TextInput):
    """
TextInput widget that adds a 'datepicker' class to the html input
element; this makes it easy to write a jQuery selector that adds a
UI widget for date picking.
"""

    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'datepicker %s' % c
        return super(DatePickerWidget, self).__call__(field, **kwargs)


class DateTimePickerWidget(widgets.TextInput):
    """TextInput widget that adds a 'datetimepicker' class to the html
adds a UI widget for datetime picking.
"""

    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'datetimepicker %s' % c
        return super(DateTimePickerWidget, self).__call__(field, **kwargs)


class TimePickerWidget(widgets.TextInput):
    """TextInput widget that adds a 'timepicker' class to the html
input element; this makes it easy to write a jQuery selector that
adds a UI widget for time picking.
"""

    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'timepicker %s' % c
        return super(TimePickerWidget, self).__call__(field, **kwargs)


class BootstrapTextInput(Input):
    def __init__(self, regular_class="form-control", error_class=u'has_errors', input_type='text'):
        super(BootstrapTextInput, self).__init__(input_type)
        self.error_class = error_class
        self.regular_class = regular_class

    def __call__(self, field, **kwargs):
        if field.errors:
            c = kwargs.pop('class', '') or kwargs.pop('class_', '')
            kwargs['class'] = u'%s %s' % (self.error_class, c)
        else:
            c = kwargs.pop('class', '') or kwargs.pop('class_', '')
            kwargs['class'] = u'%s %s' % (self.regular_class, c)
        return super(BootstrapTextInput, self).__call__(field, **kwargs)


class BootstrapIgnoreTableWidget(object):
    """
    Renders a list of fields as a set of table rows with th/td pairs.

    If `with_table_tag` is True, then an enclosing <table> is placed around the
    rows.

    Hidden fields will not be displayed with a row, instead the field will be
    pushed into a subsequent table row to ensure XHTML validity. Hidden fields
    at the end of the field list will appear outside the table.
    """

    def __init__(self, with_row_tag=True, column_width=4):
        self.with_row_tag = with_row_tag
        self.column_size = column_width

    def __call__(self, field, **kwargs):
        html = []
        if self.with_row_tag:
            kwargs.setdefault('id', field.id)
            html.append('<div class="row" %s>' % html_params(**kwargs))
        hidden = ''

        for subfield in field:
            if subfield.type == 'HiddenField':
                hidden += unicode(subfield)
            else:

                html.append('<div class="col-xs-%s"><label class="control-label" for="%s">%s</label>%s%s</div>' % (
                    self.column_size, subfield.id, unicode(subfield.label), hidden, unicode(subfield)))
                hidden = ''
        if self.with_row_tag:
            html.append('</div>')
        if hidden:
            html.append(hidden)
        return HTMLString(''.join(html))


class MyBaseCSRFForm(SessionSecureForm):
    SECRET_KEY = 'EPj00jpfj8Gx1SjnyLa23BBSQfnQ9DJYe0Ym'
    TIME_LIMIT = timedelta(minutes=20)


class SearchForm(MyBaseCSRFForm):
    search = TextField(u'', validators=[validators.input_required()])

    collection = SelectField(u'Collection', choices={}, validators=[validators.input_required()], default="")


class AdvancedSearchForm(MyBaseCSRFForm):
    search = TextField(u'', validators=[validators.input_required()])

    collection = SelectField(u'Collection', choices={}, validators=[validators.input_required()], default="")


class AddCollectionForm(MyBaseCSRFForm):
    label = TextField(u'', validators=[validators.input_required()])

    collection = SelectField(u'Collection', choices={}, coerce=str, validators=[validators.input_required()])

