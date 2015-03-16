from django import template


register = template.Library()


@register.filter(name='opp')
def opp(value, arg):
    if value.home_team == arg:
        return 'vs <a href="{link}"> {team}</a>'.format(link=value.away_team.get_absolute_url(),
                                                        team=value.away_team.short_name)
    else:
        return 'at <a href="{link}"> {team}</a>'.format(link=value.home_team.get_absolute_url(),
                                                        team=value.home_team.short_name)


@register.filter(name='score')
def score(value, arg):
    if value.home_team == arg:
        if value.final_score['home_team'] > value.final_score['away_team']:
            return ('W <a href="{link}" class="text-success">'
                    '{home_score} - {away_score}</a>').format(link=value.get_absolute_url(),
                                                              home_score=value.final_score['home_team'],
                                                              away_score=value.final_score['away_team'])
        else:
            return ('L <a href="{link}" class="text-danger">'
                    '{home_score} - {away_score}</a>').format(link=value.get_absolute_url(),
                                                              home_score=value.final_score['home_team'],
                                                              away_score=value.final_score['away_team'])
    else:
        if value.final_score['away_team'] > value.final_score['home_team']:
            return ('W <a href="{link}" class="text-success">'
                    '{away_score} - {home_score}</a>').format(link=value.get_absolute_url(),
                                                              home_score=value.final_score['home_team'],
                                                              away_score=value.final_score['away_team'])
        else:
            return ('L <a href="{link}" class="text-danger">'
                    '{away_score} - {home_score}</a>').format(link=value.get_absolute_url(),
                                                              home_score=value.final_score['home_team'],
                                                              away_score=value.final_score['away_team'])