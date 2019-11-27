compctl -K _playable playable

_playable() {
  local completions

  completions="$(playable --list_crids)"

  reply=(${(ps:\n:)completions})
}