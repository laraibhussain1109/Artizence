# File: matches/serializers.py
from rest_framework import serializers
from datetime import datetime

class UnixDateField(serializers.Field):
    """
    A custom field to handle Unix timestamp date input.
    
    When reading input, this field expects an integer (or string representing an
    integer) seconds since the Unix epoch and converts it to a Python date.
    
    When outputting, it converts the Python date back to a Unix timestamp (in seconds).
    """
    def to_internal_value(self, data):
        try:
            # Convert input data to integer timestamp.
            timestamp = int(data)
        except (ValueError, TypeError):
            raise serializers.ValidationError("A valid Unix timestamp is required.")
        # Return a Python date object.
        return datetime.fromtimestamp(timestamp).date()

    def to_representation(self, value):
        # value is a Python date; convert it to a Unix timestamp (seconds).
        return int(datetime.combine(value, datetime.min.time()).timestamp())


class MatchFeaturesSerializer(serializers.Serializer):
    # match_date = serializers.DateField(
    #     input_formats=['%Y-%m-%d'],
    #     help_text="Match date in YYYY-MM-DD format"
    # )
    match_date = UnixDateField(
        help_text="Match date as Unix timestamp (seconds since 1970-01-01 UTC)"
    )

    avg_runs_last5 = serializers.FloatField(
        required=True,
        help_text="Average runs scored in last 5 matches"
    )
    avg_wkts_last5 = serializers.FloatField(
        required=True,
        help_text="Average wickets taken in last 5 matches"
    )
    team_momentum = serializers.FloatField(
        required=True,
        help_text="Momentum metric for the team (e.g. between 0 and 1)"
    )
    team_home = serializers.CharField(
        required=True,
        help_text="Home team name"
    )
    team_away = serializers.CharField(
        required=True,
        help_text="Away team name"
    )

class PredictionSerializer(serializers.Serializer):
    predicted_winner = serializers.CharField(
        help_text="The predicted winning team"
    )
    predicted_score_win = serializers.FloatField(
        help_text="Predicted score of the winning team"
    )
    predicted_score_loss = serializers.FloatField(
        help_text="Predicted score of the losing team"
    )
