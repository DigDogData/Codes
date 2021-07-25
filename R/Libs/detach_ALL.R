#=================================================================
# FUNCTION TO DETACH ALL PACKAGES & PERSONAL ENVIROMENT VARIABLES
#=================================================================
# argument "unload" applies only to package detaching
detachAll <- function(unload = T){
  
  # detach all "other" (user-loaded) packages
  pkgs <- names(sessionInfo()$otherPkgs)
  if(!is.null(pkgs)) invisible(lapply(paste('package:', pkgs, sep = ""),
                                      detach,
                                      character.only = T,
                                      unload = unload,
                                      force = T))
  
  # detach all copies of personal environmental variable
  # (everything except GlobalEnv, base packages, tools and autoloads)
  env <- search()[-grep("Global|package|tools|Auto", search())]
  if(length(env) > 0) lapply(env, detach, character.only = T, unload = T)
}
