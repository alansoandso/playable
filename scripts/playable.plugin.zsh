_playable() {
  local completions

  completions="$(playable --list_crids)"

  reply=(${(ps:\n:)completions})
}

# Complete with _playable
# '--env ' then return choice of (integration production)
# '--' then return choice between (verbose collections movies)


compctl -K _playable \
        -x 'c[-1,--env]' -k '(integration production)' - \
           's[--]' -k '(env verbose collections movies)' \
        -- playable

