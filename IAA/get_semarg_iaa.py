from IAA_SemArg_clean import prepare_df

# prepare data
foelie_df = prepare_df("team_data_2024/processed/foelie-triggers-c.tsv", list_arguments)
kruid_df = prepare_df("team_data_2024/processed/kruidnagel-triggers-c.tsv", list_arguments)
nootmuskaat_df = prepare_df("team_data_2024/processed/nootmuskaat-triggers-c.tsv", list_arguments)
kaneel_df = prepare_df("team_data_2024/processed/kaneel-triggers-c.tsv", list_arguments)