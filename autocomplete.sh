_dothis_complete()
{
  local cur prev

  COMPREPLY=()
  cur=${COMP_WORDS[COMP_CWORD]}
  prev=${COMP_WORDS[COMP_CWORD-1]}

  if [ $COMP_CWORD -eq 1 ]; then
    COMPREPLY=( $(compgen -W "asadmin deploy" -- $cur) )
  elif [ $COMP_CWORD -eq 2 ]; then
    case "$prev" in
      "asadmin")
        COMPREPLY=( $(compgen -W "start-domain stop-domain" -- $cur) )
        ;;
      "deploy")
        COMPREPLY=( $(compgen -W "all current" -- $cur) )
        ;;
      *)
        ;;
    esac
  fi

  return 0
}

complete -F _dothis_complete dothis
