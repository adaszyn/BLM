from django import template


register = template.Library()


@register.filter(name='past_game_name')
def past_game_name(value, arg):
    if value.home_team == arg:
        # Example: CHI 230 vs NYK 169
        return '{home_team} {home_score} vs {away_team} {away_score}'.format(home_team=value.home_team.short_name,
                                                                             home_score=value.final_score['home_team'],
                                                                             away_team=value.away_team.short_name,
                                                                             away_score=value.final_score['away_team'])
    else:
        # Example: NYK 230 at CHI 169
        return '{away_team} {away_score} at {home_team} {home_score}'.format(away_team=value.away_team.short_name,
                                                                             away_score=value.final_score['away_team'],
                                                                             home_team=value.home_team.short_name,
                                                                             home_score=value.final_score['home_team'])


@register.filter(name='color')
def color(value, arg):
    return 'text-success' if value.winner == arg else 'text-danger'


@register.filter(name='future_game_name')
def future_game_name(value, arg):
    if value.home_team == arg:
        # Example: CHI vs NYK
        return '{home_team} vs {away_team}'.format(home_team=value.home_team.short_name,
                                                   away_team=value.away_team.short_name)
    else:
        # Example: NYK at CHI
        return '{away_team} at {home_team}'.format(away_team=value.away_team.short_name,
                                                   home_team=value.home_team.short_name)