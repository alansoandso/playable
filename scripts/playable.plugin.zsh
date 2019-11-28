_playable() {
  local completions

  completions="$(playable --list_crids)"

  reply=(${(ps:\n:)completions})
}

# 1. If '--' then return choice between (verbose catalogue_movies)
# 2. Complete with _playable
compctl -K _playable -x 's[--]' -k '(verbose catalogue_movies)' -- playable
