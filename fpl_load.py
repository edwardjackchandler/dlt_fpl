import abc

import pandas as pd
import requests


class FPLDataLoader:
    """
    Abstract base class for loading data from the Fantasy Premier League API.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.base_url = "https://fantasy.premierleague.com/api/"
        self.url = None
        self.json = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def json(self):
        return self._json

    @json.setter
    def json(self, json):
        self._json = json

    @abc.abstractmethod
    def request_data(self):
        self.json = requests.get(self.url).json()

    @abc.abstractmethod
    def format_request(self) -> str:
        self.data = pd.DataFrame(self.json)

    @abc.abstractmethod
    def format_data(self) -> pd.DataFrame:
        return pd.DataFrame(self.data)

    def get_data(self):
        self.request_data()
        self.format_request()
        return self.format_data()


class StandingsLoader(FPLDataLoader):
    """
    Class for loading league standings data from the Fantasy Premier League API.

    Attributes:
        league_id (int): The ID of the league.

    DataFrame Columns:
        - id
        - event_total
        - player_name
        - rank
        - last_rank
        - rank_sort
        - total
        - entry
        - entry_name
    """

    def __init__(self, league_id):
        super().__init__()
        self.league_id = league_id
        self.url = self.base_url + f"leagues-classic/{league_id}/standings/"

    def format_request(self):
        self.data = self.json["standings"]["results"]

    def format_data(self) -> pd.DataFrame:
        df = pd.DataFrame(self.data)
        df['league_id'] = self.league_id
        return df


class HistoryLoader(FPLDataLoader):
    """
    Class for loading entry history data from the Fantasy Premier League API.

    Attributes:
        entry_id (int): The ID of the entry.

    DataFrame Columns:
        - event
        - points
        - total_points
        - rank
        - rank_sort
        - overall_rank
        - bank
        - value
        - event_transfers
        - event_transfers_cost
        - points_on_bench
        - entry
    """

    def __init__(self, entry_id):
        super().__init__()
        self.entry_id = entry_id
        self.url = self.base_url + f"entry/{entry_id}/history/"

    def format_request(self):
        self.data = self.json["current"]

    def format_data(self):
        df = pd.DataFrame(self.data)
        df["entry"] = self.entry_id
        return df


class PicksLoader(FPLDataLoader):
    """
    Class for loading entry picks data from the Fantasy Premier League API.

    Attributes:
        entry_id (int): The ID of the entry.

    DataFrame Columns:
        - Various columns related to entry picks.
    """

    def __init__(self, entry_id, event_id):
        super().__init__()
        self.entry_id = entry_id
        self.event_id = event_id
        self.url = self.base_url + f"entry/{entry_id}/event/{event_id}/picks/"

    def format_request(self):
        self.data = self.json["picks"]

    def format_data(self):
        df = pd.DataFrame(self.data)
        df["entry"] = self.entry_id
        df["event"] = self.event_id
        return df


class ElementFixturesLoader(FPLDataLoader):
    """
    Class for loading player fixtures data from the Fantasy Premier League API.

    Attributes:
        element_id (int): The ID of the player.

    DataFrame Columns:
        - Various columns related to player fixtures.
    """

    def __init__(self, element_id):
        super().__init__()
        self.element_id = element_id
        self.url = self.base_url + f"element-summary/{element_id}/"

    def format_request(self):
        self.data = self.json["fixtures"]

    def format_data(self):
        df = pd.DataFrame(self.data)
        df["element_id"] = self.element_id
        return df


class ElementHistoryLoader(FPLDataLoader):
    """
    Class for loading player history data from the Fantasy Premier League API.

    Attributes:
        element_id (int): The ID of the player.

    DataFrame Columns:
        - Various columns related to player history.
    """

    def __init__(self, element_id):
        super().__init__()
        self.element_id = element_id
        self.url = self.base_url + f"element-summary/{element_id}/"

    def format_request(self):
        self.data = self.json["history"]

    def format_data(self):
        df = pd.DataFrame(self.data)
        df["element_id"] = self.element_id
        return df


class BootstrapLoader(FPLDataLoader):
    """
    Class for loading general player data from the Fantasy Premier League API.

    DataFrame Columns:
        - Various columns related to general player data.
    """

    def __init__(self):
        self.base_url = "https://fantasy.premierleague.com/api/"
        self.url = self.base_url + "bootstrap-static/"
        self.data = None
        self.json = self.fetch_data()

    def fetch_data(self):
        response = requests.get(self.url)
        return response.json()


class EventsLoader(BootstrapLoader):
    """
    Class for loading eve

    DataFrame Columns:
        - id
        - name
        - deadline_time
        - release_time
        - average_entry_score
        - finished
        - data_checked
        - highest_scoring_entry
        - deadline_time_epoch
        - deadline_time_game_offset
        - highest_score
        - is_previous
        - is_current
        - is_next
        - cup_leagues_created
        - h2h_ko_matches_created
        - ranked_count
        - chip_plays
        - most_selected
        - most_transferred_in
        - top_element
        - top_element_info
        - transfers_made
        - most_captained
        - most_vice_captained
    """

    def format_request(self):
        self.data = self.json["events"]


class PhasesLoader(BootstrapLoader):
    """
    Class for loading phase data from the Fantasy Premier League API.

    DataFrame Columns:
        - id
        - name
        - start_event
        - stop_event
        - highest_score
    """

    def format_request(self):
        self.data = self.json["phases"]


class TeamsLoader(BootstrapLoader):
    """
    Class for loading team data from the Fantasy Premier League API.

    DataFrame Columns:
        - code
        - draw
        - form
        - id
        - loss
        - name
        - played
        - points
        - position
        - short_name
        - strength
        - team_division
        - unavailable
        - win
        - strength_overall_home
        - strength_overall_away
        - strength_attack_home
        - strength_attack_away
        - strength_defence_home
        - strength_defence_away
        - pulse_id
    """

    def format_request(self):
        self.data = self.json["teams"]


class TotalPlayersLoader(BootstrapLoader):
    """
    Class for loading the total number of players from the Fantasy Premier League API.

    DataFrame Columns:
        - total_players
    """

    def format_request(self):
        self.data = self.json["total_players"]

    def format_data(self):
        df = pd.DataFrame([{"total_players": self.data}])
        return df


class ElementsLoader(BootstrapLoader):
    """
    Class for loading player element data from the Fantasy Premier League API.

    DataFrame Columns:
        - chance_of_playing_next_round
        - chance_of_playing_this_round
        - code
        - cost_change_event
        - cost_change_event_fall
        - cost_change_start
        - cost_change_start_fall
        - dreamteam_count
        - element_type
        - ep_next
        - ep_this
        - event_points
        - first_name
        - form
        - id
        - in_dreamteam
        - news
        - news_added
        - now_cost
        - photo
        - points_per_game
        - second_name
        - selected_by_percent
        - special
        - squad_number
        - status
        - team
        - team_code
        - total_points
        - transfers_in
        - transfers_in_event
        - transfers_out
        - transfers_out_event
        - value_form
        - value_season
        - web_name
        - region
        - minutes
        - goals_scored
        - assists
        - clean_sheets
        - goals_conceded
        - own_goals
        - penalties_saved
        - penalties_missed
        - yellow_cards
        - red_cards
        - saves
        - bonus
        - bps
        - influence
        - creativity
        - threat
        - ict_index
        - starts
        - expected_goals
        - expected_assists
        - expected_goal_involvements
        - expected_goals_conceded
        - influence_rank
        - influence_rank_type
        - creativity_rank
        - creativity_rank_type
        - threat_rank
        - threat_rank_type
        - ict_index_rank
        - ict_index_rank_type
        - corners_and_indirect_freekicks_order
        - corners_and_indirect_freekicks_text
        - direct_freekicks_order
        - direct_freekicks_text
        - penalties_order
        - penalties_text
        - expected_goals_per_90
        - saves_per_90
        - expected_assists_per_90
        - expected_goal_involvements_per_90
        - expected_goals_conceded_per_90
        - goals_conceded_per_90
        - now_cost_rank
        - now_cost_rank_type
        - form_rank
        - form_rank_type
        - points_per_game_rank
        - points_per_game_rank_type
        - selected_rank
        - selected_rank_type
        - starts_per_90
        - clean_sheets_per_90
    """

    def format_request(self):
        self.data = self.json["elements"]


class ElementStatsLoader(BootstrapLoader):
    """
    Class for loading element statistics data from the Fantasy Premier League API.

    DataFrame Columns:
        - label
        - name
    """

    def format_request(self):
        self.data = self.json["element_stats"]


class ElementTypesLoader(BootstrapLoader):
    """
    Class for loading element type data from the Fantasy Premier League API.

    DataFrame Columns:
        - id
        - plural_name
        - plural_name_short
        - singular_name
        - singular_name_short
        - squad_select
        - squad_min_select
        - squad_max_select
        - squad_min_play
        - squad_max_play
        - ui_shirt_specific
        - sub_positions_locked
        - element_count
    """

    def format_request(self):
        self.data = self.json["element_types"]
