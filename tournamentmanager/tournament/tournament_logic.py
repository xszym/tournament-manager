from .helpers import is_power_of_2
from .models import Game, Team, JoinRequestStatusType, TeamJoinRequest, Tournament, TeamTournamentRequest, EliminationType, Match
from random import shuffle
from math import sqrt

def generate_matches_for_tournament(tournament: Tournament):
    if tournament.type_of_elimination == EliminationType.GROUP.value:
        return generate_matches_for_group_elimination(tournament)
    elif tournament.type_of_elimination == EliminationType.KNOCKOUT.value:
        return generate_matches_for_knockout_elemination(tournament)
    else:
        raise ValueError("Unknown elimination type")


def generate_matches_for_group_elimination(tournament: Tournament):
    '''
    Generate matches for group elimination
    return list of matches
    '''
    raise NotImplementedError("Not implemented yet")
    matches = []
    teams = tournament.team_list.objects.all()

    print(teams)
    return
    if len(teams) % 4 != 0:
        raise ValueError("Number of teams in group must be multiple of 4")

    number_of_rounds = len(teams) // 4
    for round_number in range(number_of_rounds):
        for match_number in range(number_of_rounds):
            match = Match(tournament=tournament,
                         match_number=round_number * number_of_rounds + match_number)

            match.team_1_id = teams[round_number * 4 + match_number]
            match.team_2_id = teams[round_number * 4 + match_number + 1]
            matches.append(match)

    return matches


def generate_matches_for_knockout_elemination(tournament: Tournament):
    matches = []
    team_list = list(tournament.team_list.all())
    print(team_list)

    if len(team_list) < 2:
        raise ValueError("Number of teams in tournament must be greater than 2")
    if not is_power_of_2(len(team_list)):
        raise ValueError("Number of teams in tournament must be power of 2")
    shuffle(team_list)
    nof_matches = len(team_list) - 1
    nof_following_matches = int(len(team_list) / 2) - 1

    for i in range(0, nof_following_matches):
        # Matches without teams
        match = Match(tournament=tournament, match_number=i)
        matches.append(match)
    for i in range(nof_following_matches, nof_matches):
        # Matches with teams

        team1id = (i - nof_following_matches) * 2
        team2id = team1id + 1
        team1 = team_list[team1id]
        team2 = team_list[team2id]

        match = Match(tournament=tournament, match_number=i, team_A=team1, team_B=team2)
        matches.append(match)
    return matches
