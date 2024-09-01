# Adding a new year

Currently, tournament regions and rankings are added manually. This is done via the following:

1. Create a file in `tournament_rankings.r<year>.py`. 
2. Determine the orientation of each region in the bracket, and add them to the "region_location" dict, following the format of previous years
3. Create 4 dictionaries with the key as the school's ranking and the value as the school's name. The dictionaries should be named `south`, `east`, `midwest`, and `west` for each region. For the play-in game, add 1 team as the actual rank, and the other as `"play_in"`. Specify the rank of the play in game with `"play_in_rank"`.
4. Run the `generate_yearly_data.py` script
