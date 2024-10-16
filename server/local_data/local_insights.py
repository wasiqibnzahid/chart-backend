from .local_data import (
    init,
    competition_columns,
    calculate_competition_insights,
    calculate_relevant_insights,
    azteca_columns
)


def get_insights(date_filter=None):
    print(date_filter)
    df = init()
    video_other = calculate_competition_insights(
        df, [
            col for col in competition_columns if 'Video' in col], '', date_filter)
    video_self = calculate_relevant_insights(
        df, [col for col in azteca_columns if 'Video' in col], '', date_filter)
    note_other = calculate_competition_insights(
        df, [
            col for col in competition_columns if 'Note' in col], '', date_filter)
    note_self = calculate_relevant_insights(
        df, [col for col in azteca_columns if 'Note' in col], '', date_filter)
    total_self = calculate_relevant_insights(
        df, azteca_columns, '', date_filter)
    total_competition = calculate_competition_insights(df, [
        col for col in competition_columns], '', date_filter)
    return {
        "videos": {
            "self": video_self,
            "competition": video_other
        },
        "notes": {
            "self": note_self,
            "competition": note_other
        },
        "total": {
            "self": total_self,
            "competition": total_competition
        }
    }
