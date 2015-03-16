from django import template


register = template.Library()


@register.filter(name='label_color')
def label_color(value, arg):
    if arg == 'away_team':
        if value['away_team'] > value['home_team']:
            return 'label-success'
        else:
            return 'label-danger'
    elif arg == 'home_team':
        if value['home_team'] > value['away_team']:
            return 'label-success'
        else:
            return 'label-danger'


@register.filter(name='text_color')
def text_color(value, arg):
    if arg == 'away_team':
        if value['away_team'] > value['home_team']:
            return 'text-success'
        else:
            return 'text-danger'
    elif arg == 'home_team':
        if value['home_team'] > value['away_team']:
            return 'text-success'
        else:
            return 'text-danger'